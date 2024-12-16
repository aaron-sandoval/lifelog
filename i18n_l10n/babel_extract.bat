pybabel extract --mapping-file=babel.cfg --output-file=locale/timesheet.pot --input-dirs=babel_intermediate.txt
:: ../utils/Visualize.py
:: pybabel update --domain=timesheet --input-file=locale/timesheet.pot --output-dir=locale
:: pybabel compile --domain=timesheet --directory=locale --use-fuzzy