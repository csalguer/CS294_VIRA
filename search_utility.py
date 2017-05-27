from __future__ import print_function
import sys
import os
from pprint import pprint
import json
from googleapiclient.discovery import build
import pandas as pd
from collections import namedtuple
from pandas import DataFrame as df_

class QueryItem(object):
    def __init__(self,dic):
        self.__dict__.update(dic)        
    def __getitem__(self,name):
        return self.__dict__[name]       
        
class QueryResult(object):
    def __init__(self,dic):
        self.__dict__.update(dic)
        self.items = [QueryItem(i) for i in self.items if type(i)==dict]        
    def __getitem__(self,name):
        return self.__dict__[name]

Config = namedtuple('Config',['developerKey','cx'])

class SearchUtility(object):
    """docstring for SearchUtility"""
    def __init__(self, configFile='customsearch.json', debug=True):
        print("DEBUG MODE: ", debug)
        super(SearchUtility, self).__init__()
        config = Config(**json.load(open(configFile,'r')))    
        self.config = config
        self.service = build("customsearch","v1",developerKey=self.config.developerKey)  
        # self.service = build("customsearch", "v1",
        # developerKey="AIzaSyDuxJeswLNDUBRzQe_FqRi6BQ_BuDkYSbw")
        self.debug = debug

    # Currently searches over IGN and GameFaqs
    # To update urls searched, update CSE at Google API Console
    # DEPRECATED VERSION BELOW:
    # ::::::::::::::::::::::::::
    # def GameInfoSearch(self, query):
    #     res = self.service.cse().list(
    #         q=query,
    #         cx='008460768433520372470:mfubc-xv4eo',
    #         ).execute()
    #     return QueryResult(res)
    #     if self.debug is True:
    #         pprint(res)
    # ::::::::::::::::::::::::::

    def searchGoogle(self, query, **kwargs):      
        res = self.service.cse().list(q=query,cx=self.config.cx,**kwargs).execute()  
        return QueryResult(res)


    def getDataFromSearch(self, query, **kwargs):
        iterator,maxIter = 0,3
        data = []
        res = self.searchGoogle(query)
        data += [df_({k: [item[k] for item in res.items] for k in ['link','title','snippet']})]
        while res.queries.has_key('nextPage') and iterator < maxIter:
            res = self.searchGoogle(query,start=res.queries['nextPage'][0]['startIndex'])    
            data += [df_({k: [item[k] for item in res.items] for k in ['link','title','snippet']})]
            iterator+=1
        data = pd.concat(data).reset_index(drop=1)
        if self.debug is True:
            pprint(data)
        return data


def main():
    #Simple test Usage to get 
    print("Enter search query: ")
    query = raw_input()
    sUtil = SearchUtility(debug=False)
    data = sUtil.getDataFromSearch(query)
    print(data)



if __name__ == '__main__':
    main()