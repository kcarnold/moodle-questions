from moodle_questions.questions.abstract import Question
from moodle_questions.dataset import dataset_definition

class CalculatedMultichoiceQuestion(Question):
    """
    This class represents a calculated multiple choice Moodle question
    type that is related to both `multichoice` and `calculated` types.

    Different answers with different fraction of points awards 
    are added using `add_answer` as multiple choices.

    The text in the answer use wildcard notation similar to the 
    calculated question type, and also datasets for the variables.
    See: https://docs.moodle.org/310/en/Calculated_multichoice_question_type

    Currently, it is upto the user to specify the answer texts correctly
    with the wildcards.

    The wrong answers can also have wrong formula with wildcards.
    """

    _type = "calculatedmultichoice"
    _allow_combined_feedback = True
    _allow_multiple_tries = False

    _answer_numbering = [
        "none",
        "abc",
        "ABCD",
        "123",
        "iii",
        "IIII"
    ]

    def __init__(self, itemcount=10, *args, **kwargs):
        super(CalculatedMultichoiceQuestion, self).__init__(*args, **kwargs)
        self._answer_numbering = answer_numbering
        self.answers = []
        self.variables = []
        self.minimums = []
        self.maximums = []
        self.decimals = []
        self.itemcount = itemcount

    def _to_xml_element(self):
        question = super(CalculatedMultichoiceQuestion, self)._to_xml_element()

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
    
    def add_variables(self, variable, minimum, maximum, decimals=1):
        self.variables.append(variable)
        self.minimums.append(minimum)
        self.maximums.append(maximum)
        self.decimals.append(decimals)
        