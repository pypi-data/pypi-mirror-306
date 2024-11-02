#!/usr/bin/env python3
"""
Query the Uppsala University Library search service
"""
from uppsala_pyub.soup import make_soup
import re




def format_date_string(datestring, startdate=True):
    pat = re.compile(r'\d{4}-\d{2}-\d{2}')
    if pat.search(datestring) is not None:
        return datestring
    try:
        _ = int(datestring[:4])
        if startdate:
            formatted_datestring = f"{datestring[:4]}-01-01"
        else:
            formatted_datestring = f"{datestring[:4]}-12-31"
        return formatted_datestring
    except:
        ValueError(f"Bad datestring: I don't know how to format your datestring entry {datestring}.")


def format_creator_names(names):
    formatted_names = []
    pat = re.compile(r'(,|and|&)')
    formatted_names.extend([_.strip() for _ in pat.split(names) if _.strip() != ''])
    return formatted_names


def search_url(**kwargs):
    base_url = "https://uub.primo.exlibrisgroup.com/discovery/search?"
    tabscope = f"tab=Everything&search_scope=MyInst_and_CI&vid=46LIBRIS_UUB:UUB&lang={kwargs.get("language")}&mode=advanced&offset=0"
    filters = []

    if kwargs.get("query") is None:
        queries = []
        if kwargs.get("creator") is not None:
            creators = format_creator_names(kwargs.get("creator"))
            for c in creators:
                queries.append("query=creator," + kwargs.get('creator_precision') + "," + c)
        if kwargs.get("title") is not None:
            queries.append("query=title," + title_precision + "," + kwargs.get("title"))
        query = f",{kwargs.get('join_by')}&".join(queries)
    else:
        query = kwargs.get("query")
    if kwargs.get("resource_type") is not None:
        filters.append("pfilter=rtype,exact," + kwargs.get("resource_type"))
    if kwargs.get("creation_from") is not None:
        filters.append(f"pfilter=dr_s,exact,{format_date_string(kwargs.get('creation_from'))}")
        if kwargs.get("creation_to") is None:
            filters.append(f"pfilter=dr_e,exact,{format_date_string(kwargs.get('creation_from'), startdate=False)}")
        else:
            filters.append(f"pfilter=dr_e,exact,{format_date_string(kwargs.get('creation_to'), startdate=False)}")
    url = base_url + query
    if filters is not None and len(filters) > 0:
        url = url + ",AND&" + ",AND&".join(filters)
    url = url + ",AND&" + tabscope
    return url


def run_search(**kwargs):
    url = search_url(**kwargs)
    print("\n\n", url, "\n\n")
    soup = make_soup(url)
    return soup, url

