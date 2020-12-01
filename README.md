Hi-CRISPR
=========

Provides on-target cleavage efficiency prediction for SpCas9-HF1.

Calculates an efficiency score for 23 base pair long spacer sequence(s) (with PAM) on separate lines.
A Python 3 application that may be used as [web application](#web) or a [command line tool](#cli).

Running the application
-----------------------

### Requirements

The requirements for running the application are documented in the [Pipfile](./Pipfile).
 * Python 3.7
 * dm-sonnet 1.11
 * tensorflow 1.13.1

To install the dependencies [Pipenv](https://github.com/pypa/pipenv) is required:
```
pipenv install
```

### Web Application

The application may be run locally, which will then be available at http://localhost:5000/

```
pipenv run app
```

### Command Line Tool

Scores for multiple spacer sequences may be calculated in a batch:

To calculate a few sequences:
```
pipenv run calculator GCACGCCAAAGTACGCACGAGGG ...
```

Multiple sequences may be calculated at a time by reading from standard input:
```
echo GCACGCCAAAGTACGCACGAGGG | pipenv run calculator
```

References
----------

The application makes use of:
 * [DeepActiveCRISPR](https://github.com/bm2-lab/DeepActiveCRISPR)
 * [DeepCas9](https://github.com/MyungjaeSong/Paired-Library/tree/DeepCRISPR.info/DeepCas9)
