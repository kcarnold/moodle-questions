# Moodle Question Types

## Numerical

The numerical question type requires that you add a correct answer and also specify a tolerance. See an example below.

```python
from moodle_questions import Quiz, NumericalQuestion

quiz = Quiz()
q1 = NumericalQuestion(name = "F to C Conversion",
                       question_text = "Convert 40 degrees in F to C. Only enter the numerical value.",
                       default_mark = 1,
                       )
q1.add_answer(tol = 0.1,
              fraction = 100,
              text = "4.44",
              feedback = None)

quiz.add_question(q1)

quiz.save("numerical_export_example.xml")
```

In the example above, a `NumericalQuestion` is added to `quiz = Quiz()`, which is then saved to a moodle `xml` format using the `.save()` method.