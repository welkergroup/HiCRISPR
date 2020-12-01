import re

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Regexp, InputRequired


class SequenceForm(FlaskForm):
    sequence = TextAreaField(
        label='Sequences',
        validators=[
            InputRequired(message="At least one sequence must be provided!"),
            Regexp("^(?:[ACGT]{23})(?:(?:\\s*\n\\s*)+(?:[ACGT]{23})){0,50}$", re.IGNORECASE,
                           message="Invalid sequence")
        ],
        default="GGACAAGGGTGCATGCGAAGGGG\nGCAGAGAATAATGCTCGGAAGGG",
        render_kw={"rows": 5, "class": "text-monospace"}
    )
    submit = SubmitField('Submit')
    csv = SubmitField('CSV Download', render_kw={'class': 'btn-info'})
