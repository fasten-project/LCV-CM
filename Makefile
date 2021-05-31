# define the name of the virtual environment directory
# default target, when make executed without arguments
.PHONY: install
install:
	pip3 install -r requirements.txt
# venv is a shortcut target

#.PHONY: tests
#tests:
#	pytest

#run:
#	python3 server.py
#.PHONY: run
