import re
from .universidades import Universidades


class UniversidadeRegexes():
    def __init__(self, universidade):
        self.universidade = universidade

        if self.universidade == Universidades.UFPE:
            self.formula_str = '[A-Z]{2,4}\d{3,}'
        elif self.universidade == Universidades.UFRPE:
            self.formula_str = '(?:\d{5}|[A-Z]{4}\d{3,})'

        self.formula = re.compile(self.formula_str)
        self.periodo = re.compile(
            ('(?:PER.ODO: *(\d).|(SEM ?PERIODIZA..O))'))
        self.cadeira = re.compile(
            ('({}) *?- *(.+)').format(self.formula_str))
        self.prereq = re.compile(
            ('PR.-REQUISITO:'))
        self.prereq_None = re.compile(
            ('N.o ?h. ?Pr.-Requisito ?para ?esse ?Componente ?Curricular.'))
        self.coreq = re.compile(
            ('CO-REQUISITO:'))
        self.coreq_None = re.compile(
            ('N.o ?h. ?Co-Requisito ?para ?esse ?Componente ?Curricular.'))
        self.precoreq_cadeiras = re.compile(
            ('F.rmula: *?\(?((?:{}(?: ?E ?| ?OU ?| ?e ?| ?ou ?|.*))+)\)?')
            .format(self.formula_str))
        self.get_cadeiras = re.compile(
            (' ?(?:e|E|ou|OU)? ?({})').format(self.formula_str))
        self.equiv = re.compile(
            ('EQUIVAL.NCIA:'))
        self.ementa = re.compile(
            ('EMENTA:'))
        self.carga_horaria = re.compile(
            ('\d{1,}'))
        self.curso = re.compile(
            ('Curso: *(.*)'))
        self.perfil = re.compile(
            ('Perfil: *(.*)'))
        self.observacao_perfil = re.compile(
            ('OBSERVA..O PERFIL:'))
