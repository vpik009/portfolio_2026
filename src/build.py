"""Fill the ASCII placeholders in template.html and write ../index.html."""
import json, html, pathlib
here = pathlib.Path(__file__).parent
a = json.loads((here / 'assets.json').read_text())
t = (here / 'template.html').read_text()
t = t.replace('%%ASCII%%', html.escape(a['ascii'])).replace('%%MAP%%', html.escape(a['map'])).replace('%%ORION%%', a['orion'])
(here.parent / 'index.html').write_text(t)
print('wrote index.html')
