import requests
import pandas as pd
from bs4 import BeautifulSoup
from itertools import chain
import re

    # Contains only properties listed from 2016 [DateListed]
    # Contains only properties that contain the word "and" in the Description field
    # CSV ordered by DateListed
    # Required fields:
    #     MlsId
    #     MlsName
    #     DateListed
    #     StreetAddress
    #     Price
    #     Bedrooms
    #     Bathrooms
    #     Appliances (all sub-nodes comma joined)
    #     Rooms (all sub-nodes comma joined)
    #     Description (the first 200 characters)

def get_data(url):
    '''
    Imports xml file, checks if the file is valid, and turns the file into a
    a BeautifulSoup object using the lxml python plugin.
    '''
    data = requests.get(url)
    if data.status_code == 200:
        soup = BeautifulSoup(data.content, 'lxml-xml')
        return soup
    else:
        print 'Invalid xml'

def field_transform(x, field):
    '''
    Nodes: Takes each node and extracts relevant info. Regular expressions are
    used in order to include items such as Bathrooms because the string
    'Bathrooms' is a part of FullBathrooms, HalfBathrooms, and
    ThreeQuarterBathrooms. Chain is used to recombine items into single list

    Node_clean: Once the nodes are extracted into a list the list is cleaned to
    return integers or strings depending on the nature of the list.

    Node_result: Either sums result of integer values (as in the case of
    Bathrooms), or creates string from list of strings. Returns string.
    '''
    nodes = list(chain(*[list(item.stripped_strings) for item in x.findAll(re.compile(field))]))
    node_clean = [item if not item.isdigit() else int(item) for item in nodes]
    node_result = str(sum(node_clean)) if (node_clean != []) and (type(node_clean[0]) == int) else ', '.join(node_clean)
    return node_result

def build_df(soup, fields, init_field):
    '''
    '''
    df = pd.DataFrame(columns = fields)
    df[init_field] = soup.select(init_field)
    for field in fields:
        df[field] = pd.to_datetime(df[init_field].transform(field_transform, field=field), errors='ignore')
    df.drop([init_field], axis=1, inplace=True)
    return df

def apply_filters(df, filters=None):
    if filters:
        if 'include' in filters:
            if type(filters['include']) == str:
                df = df[df['Description'].transform(lambda x: x.lower().find(filters['include'])) != -1]
            else:
                for include in filters['include']:
                    df = df[df['Description'].transform(lambda x: x.lower().find(include)) != -1]
        if 'limit' in filters:
            df.loc[:,('Description')] = df['Description'].apply(lambda x: x[:filters['limit']])
        if 'year' in filters:
            df = df[df['DateListed'].transform(lambda x: x.year) == filters['year']]
        if 'ascending' in filters:
            df = df.sort_values(by='DateListed', ascending=filters['ascending'])
            df =  df.reset_index()
    return df

def df2csv(df, filepath):
    df.to_csv(filepath, index=False)

def main():
    url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    fields = ['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price',
            'Bedrooms', 'Bathrooms', 'Appliances', 'Rooms', 'Description']
    filters = {'include':'and', 'limit':200, 'year':2016, 'ascending':True}
    filepath = 'carnes_results.csv'

    soup = get_data(url)
    soup = get_data(url)
    df = build_df(soup, fields)
    df_filtered = apply_filters(df, filters)
    df2csv(df_filtered, filepath)

if __name__ == '__main__':
    # main()
    url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    fields = ['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price',
            'Bedrooms', 'Bathrooms', 'Appliances', 'Rooms', 'Description']
    filters = {'include':'and', 'limit':200, 'year':2016, 'ascending':True}
    filepath = 'carnes_results.csv'
    init_field = 'Listing'

    soup = get_data(url)
    df = build_df(soup, fields, init_field)
    df_filtered = apply_filters(df, filters)
    # df2csv(df_filtered, filepath)
