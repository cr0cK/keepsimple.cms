# Makefile for KeepSimpleCMS
#
#
.PHONY: help clean serve tests docs

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  serve      to start a Pyramid sample app"
	@echo "  tests      to make tests"
	@echo "  docs       to make the documentation"

clean:
	rm -rf docs keepsimple.cms.egg-info

serve:
	pserve development.ini --reload

tests:
	nosetests --cover-package=tutorial --cover-erase --with-coverage
	@echo
	@echo "Tests finished."

docs:
	-sphinx-apidoc -F -f -o docs keepsimplecms && cd docs && make dirhtml
	@echo
	@echo "Documentation has been generated in docs/_build/dirhtml."
