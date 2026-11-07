import sys, numpy as np
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session
src, out_path, prev = sys.argv[1], sys.argv[2], sys.argv[3]
im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
box = (148, 420, 852, 1300)            # waist up, 4:5 (704x880), body centred
crop = im.crop(box)
soft = remove(crop, session=new_session('birefnet-portrait'), only_mask=True, post_process_mask=False)
fg = np.asarray(crop, dtype=np.float32) / 255
alpha = np.asarray(soft, dtype=np.float32) / 255
alpha = np.clip((alpha - 0.08) / 0.92, 0, 1)
# centre the body: shift subject 50px left (the backdrop is generated, so the gap is just more backdrop)
SH = 0
if SH:
    fg = np.concatenate([fg[:, SH:], np.repeat(fg[:, -1:], SH, axis=1)], axis=1)
    alpha = np.concatenate([alpha[:, SH:], np.zeros((alpha.shape[0], SH), np.float32)], axis=1)
h, w = alpha.shape
def blur(a, r):
    return np.asarray(Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), dtype=np.float32) / 255
def blur3(a, r): return np.stack([blur(a[..., i], r) for i in range(3)], -1)
pa = alpha[..., None]
est = blur3(fg * pa, 4) / np.maximum(blur(alpha, 4)[..., None], 1e-3)
k = np.clip(pa ** 1.5, 0, 1)
fg = est * (1 - k) + fg * k                      # edge colour decontamination
fg = np.clip((fg - 0.5) * 1.03 + 0.5, 0, 1)
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
d = np.sqrt(((xx - w * 0.58) / (w * 0.8)) ** 2 + ((yy - h * 0.3) / (h * 0.85)) ** 2)
t = np.clip(d, 0, 1) ** 1.3
inner, outer = np.array([0.86, 0.865, 0.855]), np.array([0.52, 0.54, 0.535])
bg = inner * (1 - t[..., None]) + outer * t[..., None]
sh0 = blur(alpha, 32); sh = np.zeros_like(sh0); sh[10:, 20:] = sh0[:-10, :-20]   # shift without wrapping around
bg = bg * (1 - 0.22 * sh[..., None])
bgb = blur3(bg, 16); edge = blur(1 - alpha, 3) * alpha
fg = fg + (bgb - fg) * (edge[..., None] * 0.12)
out = fg * pa + bg * (1 - pa)
rng = np.random.default_rng(3)
out = out + rng.normal(0, 0.010, (h, w, 1))
v = 1 - 0.14 * np.clip(np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) - 0.6, 0, 1)
out = np.clip(out * v[..., None], 0, 1)
img = Image.fromarray((out * 255).astype(np.uint8), 'RGB').resize((640, 800), Image.LANCZOS)
img.save(out_path, quality=90); img.save(prev)
