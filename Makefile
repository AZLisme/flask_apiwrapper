test:
	@coverage run --source=flask_apiwrapper -m pytest test.py
	@coverage report

coverage:
	@coverage report