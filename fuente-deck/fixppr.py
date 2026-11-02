# Quita los <a:pPr> que pptxgenjs inserta en medio de un párrafo (después de un run)
import sys, re, zipfile, shutil, os
src = sys.argv[1]; tmp = src + ".tmp"
pat = re.compile(r'(</a:r>|<a:br/>)<a:pPr\b[^>]*?(?:/>|>.*?</a:pPr>)', re.S)
n = 0
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename.startswith("ppt/slides/slide") and it.filename.endswith(".xml"):
            t = data.decode("utf-8"); t, k = pat.subn(r'\1', t); n += k; data = t.encode("utf-8")
        zo.writestr(it, data)
shutil.move(tmp, src); print("pPr eliminados:", n)
