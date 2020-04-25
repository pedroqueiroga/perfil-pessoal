import re

formula_str = '[A-Z]{2,4}\d{3,}'

formula = re.compile(formula_str)

periodo = re.compile(
    ('(?:PER.ODO:(\d).|(SEM.?PERIODIZA..O))'))

cadeira = re.compile(
    ('({}) ?- ?(.+)').format(formula_str))

prereq = re.compile(
    ('PR.-REQUISITO:'))

prereq_None = re.compile(
    ('N.oh.Pr.-RequisitoparaesseComponenteCurricular.'))

coreq = re.compile(
    ('CO-REQUISITO:'))

coreq_None = re.compile(
    ('N.oh.Co-RequisitoparaesseComponenteCurricular.'))

precoreq_cadeiras = re.compile(
    ('F.rmula:.*?((?:{}.*)+)\)?').format(formula_str))

equiv = re.compile(
    ('EQUIVAL.NCIA:'))

ementa = re.compile(
    ('EMENTA:'))

carga_horaria = re.compile(
    ('\d{1,}'))

curso = re.compile(
    ('Curso:(.*)'))
