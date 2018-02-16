import requests
import pandas as pd
from bs4 import BeautifulSoup
from itertools import chain
import re


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
    rmv_duplicate: finds duplicate fields such as Description and StreetAddress
    that have different parent node names and selects the option appearing 1st

    nodes: Takes each node and extracts relevant info. Regular expressions are
    used in order to include items such as Bathrooms because the string
    'Bathrooms' is a part of FullBathrooms, HalfBathrooms, and
    ThreeQuarterBathrooms. Chain is used to recombine items into single list

    node_clean: Once the nodes are extracted into a list the list is cleaned to
    return integers or strings depending on the nature of the list.

    node_result: Either sums result of integer values (as in the case of
    Bathrooms), or creates string from list of strings. Returns string.
    '''
    rmv_duplicate = [item.parent.name for item in x.select(field)]
    nodes = list(chain(*[list(item.stripped_strings) for item in
                 x.findAll(re.compile(field)) if (item.parent.name) and
                 (item.parent.name == rmv_duplicate[0])]))
    node_clean = [item if not item.isdigit() else int(item) for item in nodes]
    node_result = str(sum(node_clean)) if (node_clean != []) and \
        (type(node_clean[0]) == int) else ', '.join(node_clean)
    return node_result


def build_df(soup, fields, init_field):
    '''
    Builds dataframe from soup object based on fields specified by user. Also
    transforms datetime objects where relevant.
    '''
    df = pd.DataFrame(columns=fields)
    df[init_field] = soup.select(init_field)
    for field in fields:
        df[field] = pd.to_datetime(df[init_field].transform(field_transform,
                                   field=field), errors='ignore')
    df.drop([init_field], axis=1, inplace=True)
    return df


def apply_filters(df, filters=None):
    '''
    Applies user specified filters. Takes both single and lists of words for
    inclusion.
    Date can be easily modified to gave max and min value rather than
    year for filter.
    '''
    if filters:
        if 'include' in filters:
            if type(filters['include']) == str:
                df = df[df['Description'].transform(lambda x:
                        x.lower().find(filters['include'])) != -1]
            else:
                for include in filters['include']:
                    df = df[df['Description'].transform(lambda x:
                            x.lower().find(include)) != -1]
        if 'limit' in filters:
            df.loc[:, ('Description')] = df['Description'].apply(lambda x:
                                                                 x[:filters
                                                                   ['limit']])
        if 'year' in filters:
            df = df[df['DateListed'].transform(lambda x: x.year) ==
                    filters['year']]
        if 'ascending' in filters:
            df = df.sort_values(by='DateListed',
                                ascending=filters['ascending'])
            df = df.reset_index()
    return df


def df2csv(df, filepath):
    '''
    Creates csv file from dataframe
    '''
    df.to_csv(filepath, index=False)


def main():
    '''
    url, fields, filters, filepath, and init_field are are user defined. Code
    should work on different xml files if these values are changed to suit the
    needs of different files.
    '''
    url = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    fields = ['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price',
              'Bedrooms', 'Bathrooms', 'Appliances', 'Rooms', 'Description']
    filters = {'include': 'and', 'limit': 200, 'year': 2016, 'ascending': True}
    filepath = '../data/carnes_results.csv'
    init_field = 'Listing'

    soup = get_data(url)
    df = build_df(soup, fields, init_field)
    df_filtered = apply_filters(df, filters)
    df2csv(df_filtered, filepath)


if __name__ == '__main__':
    main()
