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

class TestCode(unittest.TestCase):

    def test_get_data(self):
        url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
        self.soup = c.get_data(url)
        self.assertEqual(self.soup.StreetAddress.text, '0 Castro Peak Mountainway')

    # def test_field_transform(self, x, field):
    #     field = 'Title'
    #     x = self.result.select('Listing')
    #      = c.field_transform(x, field)
    #     self.assertEqual(result.StreetAddress.text, '0 Castro Peak Mountainway')
    #
    #     nodes = list(chain(*[list(item.stripped_strings) for item in x.findAll(re.compile(field))]))
    #     node_clean = [item if not item.isdigit() else int(item) for item in nodes]
    #     node_result = str(sum(node_clean)) if (node_clean != []) and (type(node_clean[0]) == int) else ', '.join(node_clean)
    #     return node_result
    #
    # def test_build_df(self, soup, fields, init_field):
    #     df = pd.DataFrame(columns = fields)
    #     df[init_field] = soup.select(init_field)
    #     for field in fields:
    #         df[field] = pd.to_datetime(df[init_field].transform(field_transform, field=field), errors='ignore')
    #     df.drop([init_field], axis=1, inplace=True)
    #     return df
    #
    # def test_apply_filters(self, df, filters=None):
    #     if filters:
    #         if 'include' in filters:
    #             if type(filters['include']) == str:
    #                 df = df[df['Description'].transform(lambda x: x.lower().find(filters['include'])) != -1]
    #             else:
    #                 for include in filters['include']:
    #                     df = df[df['Description'].transform(lambda x: x.lower().find(include)) != -1]
    #         if 'limit' in filters:
    #             df.loc[:,('Description')] = df['Description'].apply(lambda x: x[:filters['limit']])
    #         if 'year' in filters:
    #             df = df[df['DateListed'].transform(lambda x: x.year) == filters['year']]
    #         if 'ascending' in filters:
    #             df = df.sort_values(by='DateListed', ascending=filters['ascending'])
    #             df =  df.reset_index()
    #     return df
    #
    # def test_df2csv(self, df, filepath):
    #     df.to_csv(filepath, index=False)
if __name__ == '__main__':
    unittest.main()
