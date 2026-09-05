import re, pathlib, sys
D = pathlib.Path("sections-drafts")
SKIP = re.compile(r'references cited|outstanding|open rewrite|status|writing-notes wired', re.I)
print(f"{'file':<30}{'sections':>9}{'hollow':>8}{'%':>6}")
tot_h=tot_s=0; detail=[]
for f in sorted(D.glob("*.md")):
    lines=f.read_text(encoding="utf-8",errors="replace").splitlines()
    heads=[(i,l) for i,l in enumerate(lines) if re.match(r'^#{2,3} ',l)]
    secs=[]
    for n,(i,h) in enumerate(heads):
        end = heads[n+1][0] if n+1<len(heads) else len(lines)
        if SKIP.search(h): continue
        nxt = heads[n+1][1] if n+1<len(heads) else ""
        # '##' divider immediately followed by a '###' child owns no body of its own
        if h.startswith("## ") and nxt.startswith("### "): continue
        body="\n".join(lines[i+1:end]).replace("-","").replace("_","").strip()
        secs.append((h, body))
    hollow=[h for h,b in secs if len(b)<3]
    tot_h+=len(hollow); tot_s+=len(secs)
    detail += [(f.name,h) for h in hollow]
    print(f"{f.name:<30}{len(secs):>9}{len(hollow):>8}{(100*len(hollow)//max(len(secs),1)):>5}%")
print(f"\nTOTAL sections {tot_s}, hollow {tot_h}")
if "-v" in sys.argv:
    for fn,h in detail: print(f"  {fn}: {h}")
