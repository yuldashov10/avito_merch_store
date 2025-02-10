DIRS = avito_merch

dev-pep8:
		isort $(DIRS);
		black $(DIRS);
		flake8 $(DIRS);
