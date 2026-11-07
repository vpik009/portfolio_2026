"""Generate an isometric voxel duck as SVG groups."""
import json
s = 7.0
C, S30 = 0.8660254, 0.5
def P(x, y, z): return ((x - y) * C * s, (x + y) * S30 * s - z * s)
W = dict(top='#FFFFFF', left='#EDF2EE', right='#CFDAD2')
OR = dict(top='#FFB061', left='#F28C2E', right='#CF6E1B')
BLK = dict(top='#1B2420', left='#121C18', right='#0B120F')
SAGE = dict(top='#A3C0B0', left='#86A595', right='#4C6B5E')
HAT = dict(top='#8E6E4C', left='#6F5438', right='#56402A')
BAND = dict(top='#2B2018', left='#22190F', right='#1A130B')
PH = dict(top='#2C3A33', left='#1E2A25', right='#141D19')
CUP = dict(top='#6E8F7F', left='#4C6B5E', right='#3A5448')
CIG = dict(top='#FFFFFF', left='#E9ECEA', right='#C9CFCB')
TIP = dict(top='#FF9A55', left='#E8743B', right='#C95A26')
pts = []
def box(x0, x1, y0, y1, z0, z1, col, cls=''):
    def poly(ps, c):
        q = [P(*p) for p in ps]; pts.extend(q)
        return '<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % a for a in q), c)
    top = poly([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)], col['top'])
    left = poly([(x0,y1,z1),(x1,y1,z1),(x1,y1,z0),(x0,y1,z0)], col['left'])
    right = poly([(x1,y0,z1),(x1,y1,z1),(x1,y1,z0),(x1,y0,z0)], col['right'])
    return left + right + top
g = {}
g['tail'] = box(2, 5, -2, 0, 6, 8.6, W)
g['l1'] = box(2, 3, 3, 4, 0, 2.2, OR) + box(1.6, 3.4, 3, 5.6, 0, .5, OR)
g['l2'] = box(4.5, 5.5, 3, 4, 0, 2.2, OR) + box(4.1, 5.9, 3, 5.6, 0, .5, OR)
g['body'] = box(0, 7, 0, 6, 2, 7, W)
g['wing'] = box(7, 7.6, 1.2, 4.8, 3.4, 6.2, dict(top='#F4F7F4', left='#E2E9E4', right='#BFCCC3'))
g['head'] = (box(1, 5, 3, 7, 7, 11.5, W)
            + box(2.4, 3.6, 4.4, 5.6, 11.5, 12.6, SAGE)          # tuft
            + box(1.4, 4.6, 7, 9.6, 8.2, 9.2, OR))               # flat duck bill
g['eye'] = box(5, 5.05, 5.4, 6.3, 9.3, 10.3, BLK)
g['brow'] = box(5, 5.05, 5.0, 6.7, 10.7, 11.1, BLK)
g['hat'] = (box(0.2, 5.8, 2.2, 7.8, 11.5, 11.9, HAT) + box(1.1, 4.9, 3.1, 6.9, 11.9, 12.5, BAND)
            + box(1.1, 4.9, 3.1, 6.9, 12.5, 14.0, HAT))
g['headset'] = (box(0.6, 5.4, 4.6, 5.4, 11.5, 12.1, PH) + box(5.0, 5.6, 4.6, 5.4, 10.6, 12.1, PH) + box(5, 5.9, 4.1, 5.9, 8.4, 10.8, CUP)
                + box(5.9, 6.2, 4.4, 5.6, 8.8, 10.4, PH))
g['cig'] = box(3.6, 4.2, 9.6, 12.2, 8.5, 9.0, CIG) + box(3.6, 4.2, 12.2, 12.7, 8.5, 9.0, TIP)
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
pad = 10
vb = (min(xs) - pad, min(ys) - pad - 14, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad + 14)
smoke_at = P(3.9, 12.7, 9.3); note1 = P(0, 6, 15); note2 = P(5, 2, 15)
json.dump({'g': g, 'vb': vb, 'smoke': smoke_at, 'n1': note1, 'n2': note2}, open(__import__('sys').argv[1], 'w'))
print(vb)
