# Setup - scrapper

## Create venv (if not created)

    $ python -m venv venv

## Activate

    $ source venv/bin/activate

## Install dependencies

    (venv)$ pip install -r requirements.txt

# Run scrapper

From project root directory

    $ python -m scrapper

By default, 1 page is scrapped. To get more:

    $ python -m scrapper --pages 10
