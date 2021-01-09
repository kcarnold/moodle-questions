from moodle_questions.questions.abstract import Question
from moodle_questions.answer import CalculatedAnswer
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
                                         )
            dataset_definitions.append(dataset)
        
        return question

    def add_answer(self, fraction, text, tol=0.5, tol_type=2, fmt=1, feedback=None):
        self.answers.append(CalculatedAnswer(tol, tol_type, fmt, fraction, text, feedback))

    def add_variables(self, variable, minimum, maximum, decimals=1):
        self.variables.append(variable)
        self.minimums.append(minimum)
        self.maximums.append(maximum)
        self.decimals.append(decimals)


class dataset_definition:
    """
    This class defines the name, type, distribution etc of the
    dataset along with max, min, ndata etc.

    There is also a method to generate itemcount dataset_items
    for each variable specified.

    The user has to make sure that the names of these variables
    are the same as the moodle formula prescribed.
    """

    def __init__(self, variable, itemcount, dist, minimum, maximum, decimals):
        self.itemcount = itemcount
        self.minimum = minimum
        self.maximum = maximum
        self.distribution = dist
        self.variable = variable
        self.decimals = decimals

    def _to_xml_element(self, st="private"):
        dataset_definition = et.Element("dataset_definition")
        status = et.SubElement(dataset_definition, "status")
        text = et.SubElement(status, "text")
        text.text = st   # shared or private 

        name = et.SubElement(dataset_definition, "name")
        text = et.SubElement(name, "text")
        text.text = self.variable

        #type=calculated?

        distribution = et.SubElement(dataset_definition, "distribution")
        text = et.SubElement(distribution, "text")
        text.text = self.distribution

        minimum = et.SubElement(dataset_definition, "minimum")
        text = et.SubElement(minimum, "text")
        text.text = str(self.minimum)

        maximum = et.SubElement(dataset_definition, "maximum")
        text = et.SubElement(maximum, "text")
        text.text = str(self.maximum)

        decimals = et.SubElement(dataset_definition, "decimals")
        text = et.SubElement(decimals, "text")
        text.text = str(self.decimals)

        itemcount = et.SubElement(dataset_definition, "itemcount")
        itemcount.text = str(self.itemcount)

        dataset_items = et.SubElement(dataset_definition, "dataset_items")

        for i in range(1, self.itemcount+1):
            dataset_item = et.SubElement(dataset_items, "dataset_item")
            number = et.SubElement(dataset_item, "number")
            number.text = str(i)

            value = et.SubElement(dataset_item, "value")
            value.text = str(round(uniform(self.minimum, self.maximum), self.decimals))

        number_of_items = et.SubElement(dataset_definition, "number_of_items")
        number_of_items.text = str(self.itemcount)

        return dataset_definition            







