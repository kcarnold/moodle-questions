from xml.etree import ElementTree as et


class Answer:

    def __init__(self, fraction, text, feedback):
        self.fraction = int(fraction)
        self.text = text
        self.feedback = feedback

    def _to_xml_element(self):
        answer = et.Element("answer", {"fraction": str(self.fraction), "format": "html"})
        text = et.SubElement(answer, "text")
        text.text = self.text

        feedback = et.SubElement(answer, "feedback", {"format": "html"})
        text = et.SubElement(feedback, "text")
        text.text = self.feedback

        return answer


class Choice:

    def __init__(self, text, group=1, unlimited=False):
        self.text = text
        self.group = group
        self.unlimited = unlimited

    def _to_xml_element(self):
        dragbox = et.Element("dragbox")
        text = et.SubElement(dragbox, "text")
        text.text = self.text
        group = et.SubElement(dragbox, "group")
        group.text = str(self.group)

        if self.unlimited:
            unlimited = et.SubElement(dragbox, "infinite")

        return dragbox

class NumericalAnswer(Answer):
    """
    This class represents a numerical answer.
    This inherits the Answer class and the answer is still
    a string.

    This class additionally includes tolerance, currently only
    the absolute tolerance can be specified via tol method 
    when initializing.
    """
    def __init__(self, tol=0.1, *args, **kwargs):
        super(NumericalAnswer, self).__init__(*args, **kwargs)
        self.tolerance = tol

    def _to_xml_element(self):
        answer = super(NumericalAnswer, self)._to_xml_element()
        tolerance = et.SubElement(answer, "tolerance")
        tolerance.text = str(self.tolerance)

        return answer

class CalculatedAnswer(NumericalAnswer):
    """
    This class represents a calculated numerical answer.
    Similar to NumericalAnswer but the text will include
    the formula with wildcards {x} etc and there are three
    types of tolerancetypes:
    1: relative 
    2: nominal
    3: geometric
    
    Additionally, the decimal places of correct answer is specified
    through correctanswerlength
    """
    def __init__(self, tol=0.5, tol_type=2, fmt=1, *args, **kwargs):
        super(CalculatedAnswer, self).__init__(tol, *args, **kwargs)
        self.tol_type = tol_type
        self.format = fmt

    def _to_xml_element(self):
        answer = super(CalculatedAnswer, self)._to_xml_element()
        tolerancetype = et.SubElement(answer, "tolerancetype")
        tolerancetype.text = str(self.tol_type)

        correctanswerformat = et.SubElement(answer, "correctanswerformat")
        correctanswerformat.text = str(self.format)
        correctanswerlength = et.SubElement(answer, "correctanswerlength")
        correctanswerlength.text = str(self.format)

        return answer
