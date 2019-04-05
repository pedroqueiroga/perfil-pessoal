import unicodedata
import re

normform="NFC"

disciplinas_perfil = {}

with open("perfil.html",encoding="utf8") as readfile:
    periodo_regex = re.compile(">PER.ODO: (\d+).</span")
    cadeira_regex = re.compile("<div style=\"position:absolute;left:59\.81px;top:\d+\.\d+px\" class=\"cls_006\"><span class=\"cls_006\">([A-Z]{2}\d{3,}) ?- ?(.+)</span></div>")
    
    prereq_regex = re.compile("<div style=\"position:absolute;left:62.64px;top:\d+\.\d+px\" class=\"cls_007\"><span class=\"cls_007\">PR.-REQUISITO:</span></div>")
    prereq_None_regex = re.compile("<div style=\"position:absolute;left:164.41px;top:\d+\.\d+px\" class=\"cls_008\"><span class=\"cls_008\">N.o h. Pr.-Requisito para esse Componente Curricular\.</span></div>")
    coreq_regex = re.compile("<div style=\"position:absolute;left:62.64px;top:\d+\.\d+px\" class=\"cls_007\"><span class=\"cls_007\">CO-REQUISITO:</span></div>")
    coreq_None_regex = re.compile("<div style=\"position:absolute;left:164.41px;top:\d+\.\d+px\" class=\"cls_008\"><span class=\"cls_008\">N.o h. Co-Requisito para esse Componente Curricular\.</span></div>")

    precoreq_cadeira_regex = re.compile("<div style=\"position:absolute;left:62.50px;top:\d+\.\d+px\" class=\"cls_008\"><span class=\"cls_008\">([A-Z]{2}\d{3,}) ?- ?.*</span></div>")

    equiv_regex = re.compile("<div style=\"position:absolute;left:62.64px;top:\d+\.\d+px\" class=\"cls_007\"><span class=\"cls_007\">EQUIVAL.NCIA:</span></div>")

    ementa_regex = re.compile("<div style=\"position:absolute;left:62.64px;top:\d+\.\d+px\" class=\"cls_007\"><span class=\"cls_007\">EMENTA:</span></div>")

    p = None
    pp = None
    cadeira_construcao = {}

    inside_prereq = False
    inside_coreq = False
    inside_equiv = False
    
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
            cadeira_construcao["codigo"] = cadeira_match.group(1)
            cadeira_construcao["nome"] = cadeira_match.group(2)
            cadeira_construcao["prereq"] = []
            cadeira_construcao["coreq"] = []
            pp = p
            continue

        prereq_match = prereq_regex.search(line)
        if prereq_match:
            inside_prereq = True
            continue

        if inside_prereq:
            prereq_cadeira_match = precoreq_cadeira_regex.search(line)
            if prereq_cadeira_match:
                cadeira_construcao["prereq"].append(prereq_cadeira_match.group(1))
                continue
        
        coreq_match = coreq_regex.search(line)
        if coreq_match:
            inside_prereq = False
            inside_coreq = True
            continue

        if inside_coreq:
            coreq_cadeira_match = precoreq_cadeira_regex.search(line)
            if coreq_cadeira_match:
                cadeira_construcao["coreq"].append(coreq_cadeira_match.group(1))
                continue

        equiv_match = equiv_regex.search(line)
        # TODO: equivalencia importa para estes propositos?
        if equiv_match:
            inside_prereq = False
            inside_coreq = False
            continue

        ementa_match = ementa_regex.search(line)
        if ementa_match and cadeira_construcao != {}:
            # insere a cadeira naquele periodo
            disciplinas_perfil[pp].append(cadeira_construcao)
            cadeira_construcao = {}


    for p in disciplinas_perfil:
        print(p,":", sep='')
        for d in disciplinas_perfil[p]:
            print('\t',d,sep='')
        print('\n')
