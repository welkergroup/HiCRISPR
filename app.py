#!/usr/bin/env python3

import re
import os

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import calculator
from forms import SequenceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

bootstrap = Bootstrap(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute", "5 per second"],
)

calculator.init()


def render_csv(details):
    csv = "sequence,hi-crispr-a,hi-crispr-b,hi-crispr-c\n"
    for item in details:
        csv += "%s,%.2f,%.2f,%.2f\n" % (
        item['sequence'], item['scores']['hi_crispr_a'], item['scores']['hi_crispr_b'], item['scores']['hi_crispr_c'])
    return Response(csv, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename="nuccom.csv"'})


@app.route('/', methods=("GET", "POST"))
def index():
    form = SequenceForm()
    details = []

    if form.validate_on_submit():
        for seq in re.findall(r'[ACGT]{23}', form.sequence.data.upper()):
            scores = calculator.calculate_sequence(seq)
            details.append({"sequence": seq, "scores": scores})

        if form.csv.data:
            return render_csv(details)

    return render_template('index.html', form=form, details=details)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
