pybabel extract --mapping-file=babel.cfg --output-file=locale/timesheet.pot --input-dirs=babel_intermediate.txt
:: ../utils/Visualize.py
::  _a and _b are used in i18n.py as translation functions for secondary and tertiary languages
:: pybabel update --domain=timesheet --input-file=locale/timesheet.pot --output-dir=locale
:: pybabel compile --domain=timesheet --directory=locale --use-fuzzy