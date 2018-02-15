.PHONY: test
test:
	py.test test/unittests.py -vv
	py.test src/carnes_xml2csv.py
