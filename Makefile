.PHONY: test
test:
	py.test test/unittests.py -vv
	py.test --pep8 src/carnes_xml2csv.py
