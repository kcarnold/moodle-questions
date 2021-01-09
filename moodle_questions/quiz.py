from moodle_questions.questions.abstract.question import Question
from xml.etree import ElementTree as et


class Quiz:
    """
    This class represents Quiz as a set of Questions.
    """
    def __init__(self, category):
        """
        :type category: str
        :param name: category of the questions

        """
        self.category = category
        self._questions = []

    def add_question(self, question):
        """
        Adds a question to the quiz object.

        :type question: Question
        :param question: the question to add
        """
        if Question.is_instance_check(question):
            self._questions.append(question)

    def save(self, file, pretty=False):
        """
        Generates XML compatible with Moodle and saves to a file.

        :type file: str
        :param file: filename where the XML will be saved

        :type pretty: bool
        :param pretty: saves XML pretty printed
        """
        quiz = self._get_xml_tree()
        if pretty:
            root = quiz.getroot()
            self._indent(root)
        quiz.write(file, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def _get_xml_tree(self):
        """
        Converts self and all assigned questions to Moodle XML.
        """
        quiz = et.ElementTree(et.Element("quiz"))
        root = quiz.getroot()

        # Adding question which specifies the "category"
        category_question = et.Element("question")
        category_question.set("type", "category")
        category_element = et.SubElement(category_question, "category")
        text = et.SubElement(category_element, "text")
        text.text = str("$course$/top/" + self.category)
        root.append(category_question)

        for question in self._questions:
            root.append(question._to_xml_element())
        return quiz

    def _dump(self):
        quiz = self._get_xml_tree()
        root = quiz.getroot()
        self._indent(root)
        et.dump(root)

    def _indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
