#!/usr/bin/python3

import unicodedata
import re

disciplinas_perfil = {}

with open('ciencia_computacao_perfil_2002-html.html',encoding='utf8') as readfile:

    formula_regex_str = '[A-Z]{2}\d{3,}'

    formula_regex = re.compile(formula_regex_str)
        
    periodo_regex = re.compile(
        ('<p style="position:absolute;top:\d{3,}px;left:90px;white-space'
         ':nowrap" class="ft\d+0"><i><b>PER.ODO:&#160;(\d).</b></i></p>'))
    
    cadeira_regex = re.compile(
        ('<p style="position:absolute;top:\d{{3,}}px;left:90px;'
         'white-space:nowrap" class="ft\d+1"><b>'
         '({}) ?- ?(.+)</b></p>').format(formula_regex_str))
    
    prereq_regex = re.compile(
        ('<p style="position:absolute;top:\d{3,}px;left:94px;white-space:'
         'nowrap" class="ft\d+2"><b>PR.-REQUISITO:</b></p>'))
    
    prereq_None_regex = re.compile(
        ('<p style="position:absolute;top:\d{3,}px;left:247px;white-space:'
         'nowrap" class="ft\d+3">N.o&#160;h.&#160;Pr.-Requisito&#160;para&#160'
         ';esse&#160;Componente&#160;Curricular.</p>'))
    
    coreq_regex = re.compile(
        ('<p style="position:absolute;top:\d{3,}px;left:94px;white-space:'
         'nowrap" class="ft\d+2"><b>CO-REQUISITO:</b></p>'))
    
    coreq_None_regex = re.compile(
        ('<p style="position:absolute;top:\d{3,}px;left:247px;white-space:'
         'nowrap" class="ft\d+3">N.o&#160;h.&#160;Co-Requisito&#160;para&#160;'
         'esse&#160;Componente&#160;Curricular.</p>'))

    precoreq_cadeiras_regex = re.compile(
        ('<p style="position:absolute;top:\d{{3,}}px;'
         'left:247px;white-space:nowrap" class="ft\d+3">'
         'F.rmula:&#160;.*?((?:{}.*?)+)'
         '\)?</p>').format(formula_regex_str))

    equiv_regex = re.compile(
        ('<p style="position:absolute;top:\d{3,}px;left:94px;white-space:'
         'nowrap" class="ft\d+2"><b>EQUIVAL.NCIA:</b></p>'))

    ementa_regex = re.compile(
        ('<p style="position:absolute;top:\d{3,}px;left:94px;white-space:'
         'nowrap" class="ft\d+2"><b>EMENTA:</b></p>'))

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

            if cadeira_construcao != {}:
                # insere a cadeira naquele periodo
                disciplinas_perfil[pp].append(cadeira_construcao)
                cadeira_construcao = {}

                # reseta flags
                inside_prereq = False
                inside_coreq = False
                inside_equiv = False
                    

            # comeca nova cadeira
            cadeira_construcao['codigo'] = cadeira_match.group(1)
            cadeira_construcao['nome'] = cadeira_match.group(2).replace(
                '&#160;', ' ')
            cadeira_construcao['prereq'] = []
            cadeira_construcao['coreq'] = []
            cadeira_construcao['equiv'] = []
            pp = p
            continue

        prereq_match = prereq_regex.search(line)
        if prereq_match:
            inside_prereq = True
            continue

        if inside_prereq:
            prereq_cadeiras_match = precoreq_cadeiras_regex.search(line)
            if prereq_cadeiras_match:
                cadeiras_group = prereq_cadeiras_match.group(1)
                cadeiras = formula_regex.findall(cadeiras_group)
                cadeira_construcao['prereq'].extend(cadeiras)
                inside_prereq = False
                continue
            elif prereq_None_regex.search(line):
                inside_prereq = False
                continue
        
        coreq_match = coreq_regex.search(line)
        if coreq_match:
            inside_coreq = True
            continue

        if inside_coreq:
            coreq_cadeiras_match = precoreq_cadeiras_regex.search(line)
            if coreq_cadeiras_match:
                cadeiras_group = coreq_cadeiras_match.group(1)
                cadeiras = formula_regex.findall(cadeiras_group)
                cadeira_construcao['coreq'].extend(cadeiras)
                inside_coreq = False
                continue
            elif coreq_None_regex.search(line):
                inside_coreq = False
                continue

        equiv_match = equiv_regex.search(line)
        if equiv_match:
            inside_equiv = True

        if inside_equiv:
            equiv_cadeiras_match = precoreq_cadeiras_regex.search(line)
            if equiv_cadeiras_match:
                cadeiras_group = equiv_cadeiras_match.group(1)
                cadeiras = formula_regex.findall(cadeiras_group)
                cadeira_construcao['equiv'].extend(cadeiras)
                inside_equiv = False
                continue

        ementa_match = ementa_regex.search(line)
        if ementa_match:
            inside_equiv = False


    if cadeira_construcao != {}:
        # insere a última cadeira naquele periodo
        disciplinas_perfil[pp].append(cadeira_construcao)
        cadeira_construcao = {}


    for p in disciplinas_perfil:
        print(p,':', sep='')
        for d in disciplinas_perfil[p]:
            print('\t',d,sep='')
        print('\n')
