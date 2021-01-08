from moodle_questions.questions.abstract import Question
from moodle_questions.answer import CalculatedAnswer

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

    def __init__(self, *args, **kwargs):
        super(CalculatedQuestion, self).__init__(*args, **kwargs)
        self.answers = []

    def _to_xml_element(self):
        question = super(CalculatedQuestion, self)._to_xml_element()

        for answer in self.answers:
            question.append(answer._to_xml_element())

        return question

    def add_answer(self, fraction, text, tol=0.5, tol_type=2, fmt=1, feedback=None):
        self.answers.append(CalculatedAnswer(tol, tol_type, fmt, fraction, text, feedback))

    def generate_data(self, min=0, max=100, distribution="uniform", count=10):
        """
        generate dataset items to include in the dataset_definition
        make sure to define a function that does the calculations
        """


class CalculatedFormula:
    """
    This class contains the variables and formula for the CalculatedQuestion.

    In addition limits for the randomly generated datasets and function to 
    generate the data are also implemented here.
    """

    def __init__(self):
        self.variables = []
        self.