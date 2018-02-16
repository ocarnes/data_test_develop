'''
Unit tests for Booj xml to csv assessment.
Usage: from main assessment directory: make test
'''
import unittest as unittest
import pandas as pd
import requests
from bs4 import BeautifulSoup
from itertools import chain
import re
from src import carnes_xml2csv as c

url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'

class TestCode(unittest.TestCase):

    def test_get_data(self):
        result = c.get_data(url)
        self.assertTrue('0 Castro Peak Mountainway' in result.StreetAddress.text)

    def test_field_transform(self):
        field = 'Title'
        x = c.get_data(url).select('Listing')[5]
        result = c.field_transform(x, field)
        self.assertEqual(result, '27061 SEA VISTA DR')

    def test_build_df(self):
        fields = ['BrokerageName', 'BrokerPhone']
        init_field = 'Listing'
        soup = c.get_data(url)
        result = c.build_df(soup, fields, init_field)
        self.assertIsInstance(result, pd.core.frame.DataFrame)

    def test_apply_filters(self):
        fields = ['BrokerageName', 'BrokerPhone']
        init_field = 'Listing'
        soup = c.get_data(url)
        fields = ['Description']
        df = c.build_df(soup, fields, init_field)
        filters = {'include': ['and', 'beautiful']}
        result = c.apply_filters(df, filters)
        self.assertIsInstance(result, pd.core.frame.DataFrame)

if __name__ == '__main__':
    unittest.main()
