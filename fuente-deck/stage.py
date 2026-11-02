# Paso 1: duplica láminas del template maestro en el orden de la propuesta y descarta el resto.
import os, re, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = "/root/.claude/skills/synced/dce9a52a-1689-4ec5-925a-864a6d708050_1286b7b6-a582-46b0-b30e-3be5f35deb77/pptx"
TEMPLATE = os.path.join(HERE, "template.pptx")
WORK = os.path.join(HERE, "work")
OUT = os.path.join(HERE, "stage.pptx")

# Lámina del template que se usa como base para cada lámina de la propuesta, en orden
ORDER = [1, 6, 16, 16, 53, 9, 16, 32, 23, 31, 54, 16, 30, 16, 27, 29, 10, 16, 48,
         60, 26, 34, 35, 16, 39, 16, 40, 84, 16, 16, 69, 16, 74, 16, 83]

shutil.rmtree(WORK, ignore_errors=True)
with zipfile.ZipFile(TEMPLATE) as z:
    z.extractall(WORK)

created = []
for src in ORDER:
    r = subprocess.run([sys.executable, f"{SKILL}/scripts/add_slide.py", WORK, f"slide{src}.xml"],
                       capture_output=True, text=True, check=True)
    m = re.search(r"Created (ppt/slides/slide\d+\.xml)", r.stdout + r.stderr)
    created.append(os.path.basename(m.group(1)))

rels = open(f"{WORK}/ppt/_rels/presentation.xml.rels", encoding="utf-8").read()
rid = {t: i for i, t in re.findall(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels)}
rid.update({t: i for t, i in re.findall(r'Target="slides/(slide\d+\.xml)"[^>]*Id="(rId\d+)"', rels)})

pres = open(f"{WORK}/ppt/presentation.xml", encoding="utf-8").read()
ids = "".join(f'<p:sldId id="{1000 + n}" r:id="{rid[f]}"/>' for n, f in enumerate(created))
pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{ids}</p:sldIdLst>", pres, flags=re.S)
open(f"{WORK}/ppt/presentation.xml", "w", encoding="utf-8").write(pres)

subprocess.run([sys.executable, f"{SKILL}/scripts/clean.py", WORK], check=True, capture_output=True)
if os.path.exists(OUT):
    os.remove(OUT)
subprocess.run(["zip", "-Xqr", OUT, "."], cwd=WORK, check=True)
print("stage listo:", len(created), "láminas")
