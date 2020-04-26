#!/usr/bin/python3

import unidecode
from itertools import zip_longest
import pdftotext
from graphviz import Digraph

from . import regexes

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def do_everything(pdf_file):
    disciplinas_perfil = {}

    # pdf_file_obj = open(pdf_file, 'rb')
    pdf = pdftotext.PDF(pdf_file)

    curso = None

    p = None
    pp = None
    cadeira_construcao = {}


    inside_prereq = False
    inside_coreq = False
    inside_equiv = False

    last_cadeira_match = None

    matches_to_go = 0

    # o nome da universidade é a primeira linha
    first_page = pdf[0].split('\n')
    universidade = unidecode.unidecode(first_page[0].strip())
    for page_n in range(len(pdf)):
        page = [ j.strip() for i in pdf[page_n].split('\n') for j in i.split('   ') if j ]
        i = 0
        while i < len(page):
            line = page[i]
            i += 1
            curso_match = regexes.curso.search(line)
            if curso_match and not curso:
                curso = curso_match.group(1)
                continue

            periodo_match = regexes.periodo.search(line)

            if periodo_match:
                p = periodo_match.group(1) or periodo_match.group(2)
                p = unidecode.unidecode(p)
                # se não tem uma entrada para aquele periodo ainda, criar
                if not (p in disciplinas_perfil.keys()):
                    disciplinas_perfil[p] = []

                continue

            cadeira_match = regexes.cadeira.search(line)
            if cadeira_match:
                matches_to_go -= 1
                last_cadeira_match = cadeira_match
                # este loop eh util para pular matches
                # em cadeiras do coreq, prereq, equivalencia
                # eh um safeguard, levemente redundante, salva em alguns
                # casos estranhos dos perfis curriculares
                while matches_to_go > 0:
                    line = page[i]
                    i += 1
                    cadeira_match = regexes.cadeira.search(line)
                    if cadeira_match:
                        matches_to_go -= 1
                        last_cadeira_match = cadeira_match
                    else:
                        break

                if matches_to_go > -1:
                    continue

                if cadeira_construcao != {}:
                    # insere a cadeira naquele periodo
                    disciplinas_perfil[pp].append(cadeira_construcao)
                    cadeira_construcao = {}

                    # reseta flags
                    inside_prereq = False
                    inside_coreq = False
                    inside_equiv = False


                # comeca nova cadeira
                cadeira_construcao['codigo'] = last_cadeira_match.group(1)
                cadeira_construcao['nome'] = unidecode.unidecode(last_cadeira_match.group(2))
                cadeira_construcao['prereq'] = []
                cadeira_construcao['coreq'] = []
                cadeira_construcao['equiv'] = []
                pp = p
                continue

            prereq_match = regexes.prereq.search(line)
            if prereq_match:
                inside_prereq = True
                inside_coreq = False
                inside_equiv = False
                continue

            if inside_prereq:
                prereq_cadeiras_match = regexes.precoreq_cadeiras.search(line)
                if prereq_cadeiras_match:
                    cadeiras_group = prereq_cadeiras_match.group(1)
                    cadeiras = regexes.get_cadeiras.findall(cadeiras_group)
                    cadeira_construcao['prereq'].extend(cadeiras)
                    matches_to_go = len(cadeiras)
                    continue
                elif regexes.prereq_None.search(line):
                    inside_prereq = False
                    continue

            coreq_match = regexes.coreq.search(line)
            if coreq_match:
                inside_coreq = True
                inside_prereq = False
                inside_equiv = False
                continue

            if inside_coreq:
                coreq_cadeiras_match = regexes.precoreq_cadeiras.search(line)
                if coreq_cadeiras_match:
                    cadeiras_group = coreq_cadeiras_match.group(1)
                    cadeiras = regexes.get_cadeiras.findall(cadeiras_group)
                    cadeira_construcao['coreq'].extend(cadeiras)
                    matches_to_go = len(cadeiras)
                    continue
                elif regexes.coreq_None.search(line):
                    inside_coreq = False
                    continue

            equiv_match = regexes.equiv.search(line)
            if equiv_match:
                inside_equiv = True
                inside_coreq = False
                inside_prereq = False

            if inside_equiv:
                equiv_cadeiras_match = regexes.precoreq_cadeiras.search(line)
                if equiv_cadeiras_match:
                    cadeiras_group = equiv_cadeiras_match.group(0)
                    cadeiras = regexes.get_cadeiras.findall(cadeiras_group)
                    cadeira_construcao['equiv'].extend(cadeiras)
                    matches_to_go = len(cadeiras)
                    continue

            ementa_match = regexes.ementa.search(line)
            if ementa_match:
                inside_equiv = False
                inside_coreq = False
                inside_prereq = False


    if cadeira_construcao != {}:
        # insere a última cadeira naquele periodo
        disciplinas_perfil[pp].append(cadeira_construcao)
        cadeira_construcao = {}


    for p in disciplinas_perfil:
        print(p,':', sep='')
        for d in disciplinas_perfil[p]:
            print('\t',d,sep='')
        print('\n')

    n_horizontal = 0
    max_horizontal = 1;
    last_level = None
    test_switch = True
    if disciplinas_perfil:
        curso = unidecode.unidecode(curso)
        g = Digraph(curso, filename='perfil_curricular.gv', engine='dot', format='svg')

        for p in disciplinas_perfil:
            n_horizontal = 0
            with g.subgraph(name='cluster_'+p) as c:
                c.attr(style='filled')
                c.attr(color='blue')
                c.attr(fillcolor='bisque')
                c.attr(label='periodo ' + p)
                c.attr(tooltip='periodo ' + p)
                c.attr(shape='box')
                c.node_attr['style'] = 'filled'
                n_disciplinas = len(disciplinas_perfil[p])
                grouped_disciplinas = grouper(disciplinas_perfil[p], max_horizontal)
                group_leader = None
                group_receiver = None
                for group in grouped_disciplinas:
                    with c.subgraph() as gr:
                        gr.attr(rank='same')
                        group_receiver = group[0]['codigo']
                        for d in group:
                            if not d:
                                continue
                            gr.node(d['codigo'], label=d['codigo'], tooltip=d['nome'])

                            for prereq in d['prereq']:
                                gr.edge(prereq, d['codigo'])
                            for coreq in d['coreq']:
                                gr.edge(coreq, d['codigo'], dir='both')

                    if group_leader:
                        c.edge(group_leader, group_receiver, style='invis')
                    group_leader = group[0]['codigo']

        g.viewport='0,0,1,100,100'
        return g
    else:
        return None

