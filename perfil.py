import operator
import unicodedata
import re

normform="NFC"

print(sorted(disciplinas_cursadas.items(), key=operator.itemgetter(1)))

disciplinas_perfil = {}

with open("perfil.html",encoding="utf8") as readfile:
    p = None
    
    periodo_regex = re.compile(">PER.ODO: (\d+).</span")
    cadeira_regex = re.compile("<div style=\"position:absolute;left:59\.81px;top:\d+\.\d+px\" class=\"cls_006\"><span class=\"cls_006\">([A-Z]{2}\d{3,}) ?- ?(.+)</span></div>")
    coreq_regex = re.compile("<div style=\"position:absolute;left:62.64px;top:\d+\.\d+px\" class=\"cls_007\"><span class=\"cls_007\">CO-REQUISITO:</span></div>")
    prereq_regex = re.compile("<div style=\"position:absolute;left:62.64px;top:\d+\.\d+px\" class=\"cls_007\"><span class=\"cls_007\">PR.-REQUISITO:</span></div>")
    equiv_regex = re.compile("<div style=\"position:absolute;left:62.64px;top:\d+\.\d+px\" class=\"cls_007\"><span class=\"cls_007\">EQUIVAL.NCIA:</span></div>")
    
    for line in readfile:
        periodo_match = periodo_regex.search(line)

        if periodo_match:
            p = int(periodo_match.group(1))
            # se não tem uma entrada para aquele periodo ainda, criar
            if not (p in disciplinas_perfil.keys()):
                disciplinas_perfil[p] = []

            continue

        cadeira_match = cadeira_regex.search(line)
        if cadeira_match:
            codigo = cadeira_match.group(1)
            nome = cadeira_match.group(2)

            disciplinas_perfil[p].append((codigo,nome))

    print(disciplinas_perfil)
                               
