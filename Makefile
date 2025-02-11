DIRS = src locustfile.py init_merch.py

dev-pep8:
		isort $(DIRS);
		black $(DIRS);
		flake8 $(DIRS);
