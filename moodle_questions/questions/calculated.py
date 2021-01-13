from moodle_questions.questions.abstract import Question
from moodle_questions.answer import CalculatedAnswer
from moodle_questions.dataset import dataset_definition
from xml.etree import ElementTree as et

from random import uniform

class CalculatedQuestion(Question):
    """
    This class represents a calculated moodle question type
    i.e. the answer text consists of a mathematical formula with
    wild cards e.g. {x}.

    Moodle is then able to calculate the answer based on the formula
    and the dataset specified for the variable(s)
    """

    _type = "calculated"
    _allow_combined_feedback = True
    _allow_multiple_tries = False

    def __init__(self, itemcount = 10, *args, **kwargs):
        super(CalculatedQuestion, self).__init__(*args, **kwargs)
        self.answers = []
        self.variables = []
        self.minimums = []
        self.maximums = []
        self.decimals = []
        self.itemcount = itemcount


    def _to_xml_element(self):
        question = super(CalculatedQuestion, self)._to_xml_element()

        for answer in self.answers:
            question.append(answer._to_xml_element())

        dataset_definitions = et.SubElement(question, "dataset_definitions")

        for i in range(len(self.variables)):
            dataset = dataset_definition(self.variables[i],
                                         self.itemcount,
                                         "uniform",
                                         self.minimums[i],
                                         self.maximums[i],
                                         self.decimals[i]
                                         )._to_xml_element()
            dataset_definitions.append(dataset)
        
        return question

    def add_answer(self, fraction, text, tol=0.5, tol_type=2, fmt=1, feedback=None):
        self.answers.append(CalculatedAnswer(tol, tol_type, fmt, fraction, text, feedback))

    def add_variables(self, variable, minimum, maximum, decimals=1):
        self.variables.append(variable)
        self.minimums.append(minimum)
        self.maximums.append(maximum)
        self.decimals.append(decimals)
