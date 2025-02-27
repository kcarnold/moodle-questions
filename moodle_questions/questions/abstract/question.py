from abc import ABCMeta, abstractmethod
from xml.etree import ElementTree as et

from moodle_questions.utils import cdata_str, estr, truefalse
import os
from base64 import b64encode

class Question(metaclass=ABCMeta):
    """
    This is an abstract class Question used as a parent for specific types of Questions.
    """

    def __init__(self, name, question_text, default_mark, image_name=None, general_feedback=None, id_number=None, shuffle=False, usecase=False, *args,
                 **kwargs):
        """
        :type name: str
        :param name: name of the question

        :type question_text: str
        :param question_text: text of the question
        
        :type image_name:str
        :param image_name: name/path of optional image aside the text of the question
    
        :type default_mark: float
        :param default_mark: the default mark

        :type general_feedback: str
        :param general_feedback: (optional) general feedback

        :type id_number: int
        :param id_number: (optional) id number

        :type shuffle: bool
        :param shuffle: (optional) shuffle answers

        :type usecase: bool
        :param usecase: (optional) does case of answer text matter. Set to 'True' if case matters.
        """
        self.name = name
        self.question_text = question_text
        self.image_name = image_name
        self.default_mark = float(default_mark)
        self.general_feedback = general_feedback
        self.id_number = id_number
        self.shuffle = shuffle
        self.usecase = usecase
        self.set_combined_feedback(*args, **kwargs)
        self.set_multiple_tries(*args, **kwargs)

    @property
    def allow_combined_feedback(self):
        """
        This property represents if the question can have combined feedback.
        """
        return self._allow_combined_feedback

    @property
    def allow_multiple_tries(self):
        """
        This property defines if the question can be answered multiple times.
        """
        return self._allow_multiple_tries

    def set_combined_feedback(self, correct_feedback=None, partially_correct_feedback=None, incorrect_feedback=None,
                              show_number_of_correct=False,
                              *args,
                              **kwargs):
        """
        Sets optional combined feedback.

        :type correct_feedback: str
        :param correct_feedback: Feedback if the answer is correct.

        :type partially_correct_feedback: str
        :param partially_correct_feedback: Feedback if the answer is partially correct.

        :type incorrect_feedback: str
        :param incorrect_feedback: Feedback if the answer is incorrect.

        :type show_number_of_correct: bool
        :param show_number_of_correct: show number of correct answers
        """
        if self.allow_combined_feedback:
            self.correct_feedback = correct_feedback
            self.partially_correct_feedback = partially_correct_feedback
            self.incorrect_feedback = incorrect_feedback
            self.show_number_of_correct = show_number_of_correct

    def set_multiple_tries(self, penalty=0.0, hints=None, *args, **kwargs):
        """
        Allows to set penalty and hints if multiple tries are allowed.

        :type penalty: float
        :param penalty: penalty for incorrect answer

        :type hints: list
        :param hints: hints to display.
        """
        if self.allow_multiple_tries:
            self.penalty = penalty
            if hints and isinstance(hints, list):
                self.hints = hints
            else:
                self.hints = []

    # TODO tags

    @abstractmethod
    def _to_xml_element(self):
        """
        This method converts current object to Moodle XML.
        """
        question = et.Element("question")
        question.set("type", self._type)
        name = et.SubElement(question, "name")
        text = et.SubElement(name, "text")
        text.text = str(self.name)

        questiontext = et.SubElement(question, "questiontext", {"format": "html"})
        text = et.SubElement(questiontext, "text")
        if self.image_name:
            self.question_text = self.question_text+'<p><img src="@@PLUGINFILE@@/' + self.image_name.split(os.sep)[-1]+'"></p>'
        text.text = cdata_str(self.question_text)
    
        if self.image_name:
            file = et.SubElement(questiontext, "file", {"name": self.image_name.split(os.sep)[-1], "path": "/","encoding": "base64"})
            with open(self.image_name, "rb") as f:
                file.text = str(b64encode(f.read()), "utf-8")
        
        defaultgrade = et.SubElement(question, "defaultgrade")
        defaultgrade.text = str(self.default_mark)

        generalfeedback = et.SubElement(question, "generalfeedback", {"format": "html"})
        text = et.SubElement(generalfeedback, "text")
        text.text = cdata_str(self.general_feedback)

        hidden = et.SubElement(question, "hidden")
        hidden.text = "0"

        idnumber = et.SubElement(question, "idnumber")
        idnumber.text = estr(self.id_number)
                
        shuffleanswers = et.SubElement(question, "shuffleanswers")
        shuffleanswers.text = truefalse(self.shuffle)

        penalty = et.SubElement(question, "penalty")
        penalty.text = estr(self.penalty)

        usecase = et.SubElement(question, "usecase")
        usecase.text = truefalse(self.usecase)

        return question

    @classmethod
    def is_instance_check(cls, obj):
        """
        Checks if object is of class, raises TypeError otherwise.
        """
        if isinstance(obj, cls):
            return True
        else:
            raise TypeError(f"must be subclass of Question, not {obj.__class__.__name__}")


