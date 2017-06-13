from __future__ import print_function
import sys
import os
from pprint import pprint
import json
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import urllib2
import pandas as pd
from collections import namedtuple, defaultdict, Counter
import re
import math
import subprocess
from pandas import DataFrame as df_
from voice_util import VoiceUtility

class _QueryItem(object):
    def __init__(self,dic):
        self.__dict__.update(dic)        
    def __getitem__(self,name):
        return self.__dict__[name]       
        
class _QueryResult(object):
    def __init__(self,dic):
        self.__dict__.update(dic)
        self.items = [_QueryItem(i) for i in self.items if type(i)==dict]        
    def __getitem__(self,name):
        return self.__dict__[name]

Config = namedtuple('Config',['developerKey','cx'])

class SearchUtility(object):
    """USES set up CSE on Google Cloud Api to make Search Calls"""
    def __init__(self, similarityFunction=None, functionWeight=0, configFile='vira/customsearch.json', debug=True):
        # print("DEBUG MODE: ", debug)
        # Asserts to checks that validity of sim func and weight
        if similarityFunction is not None:
            assert 0 < functionWeight <= 1.0
        if functionWeight is not 0:
            assert similarityFunction is not None

        self.similarityFunction = similarityFunction
        self.functionWeight = functionWeight
        super(SearchUtility, self).__init__()
        config = Config(**json.load(open(configFile,'r')))    
        self.config = config
        self.service = build("customsearch","v1",developerKey=self.config.developerKey)
        self.debug = debug
        self.WORD = re.compile(r'\w+')

    # Currently searches over IGN and GameFaqs
    # To update urls searched, update CSE at Google API Console
    # DEPRECATED VERSION BELOW:
    # ::::::::::::::::::::::::::
    # def GameInfoSearch(self, query):
    #     res = self.service.cse().list(
    #         q=query,
    #         cx='008460768433520372470:mfubc-xv4eo',
    #         ).execute()
    #     return _QueryResult(res)
    #     if self.debug is True:
    #         pprint(res)
    # ::::::::::::::::::::::::::

    def searchGoogle(self, query, **kwargs):      
        res = self.service.cse().list(q=query,cx=self.config.cx,**kwargs).execute()  
        return _QueryResult(res)


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


    # Rn only returns the indices of the top 5 most similar
    # Must be extended to "slice" the results array 
    # inlcuding both the _QueryResults structure
    # and it's 3 associated Dict's : Link, Title, Snippet
    def top5ResultsForQuery(self, query, searchResult):
        links = searchResult["link"]
        snippets = searchResult["snippet"]
        titles = searchResult["title"]
        similarities = []
        if self.debug is True:
            print("Links: ", links)
            print("Snippets: ", snippets)
            print("Titles: ", titles)
        for (i, title) in enumerate(titles):
            similarities.append((self.similarityEvaluation(query, title), i))
        ranked = sorted(similarities, key=lambda tup: tup[0])
        return [tup[1] for tup in ranked[:5]]


    # Specialized method that performs an extra similarity comparison 
    # utlizing
    def top5WalkthroughsForQuery(self, query, searchResult):
        if "walkthrough" not in query or "guide" not in query:
            query += " walkthrough"
        links = searchResult["link"]
        snippets = searchResult["snippet"]
        titles = searchResult["title"]
        similarities = []
        if self.debug is True:
            print("Links: ", links)
            print("Snippets: ", snippets)
            print("Titles: ", titles)
        for (i, title) in enumerate(titles):
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib2.Request(links[i],headers=hdr)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            texts = soup.findAll('p', text=True)
            def visible(element):
                if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                    return False
                elif re.match('<!--.*-->', element.encode('utf-8')):
                    return False
                return True 

            visible_texts = filter(visible, texts)
            clean_text = [tag.text for tag in visible_texts]
            # print(clean_text)
            textbody = " ".join(clean_text)
            titleSim = self.similarityEvaluation(query, title)
            bodySim = self.similarityEvaluation(query, textbody)
            snippetSim = self.similarityEvaluation(query, snippets[i])
            combSim = titleSim + bodySim + snippetSim
            similarities.append((combSim, i))
        ranked = sorted(similarities, key=lambda tup: tup[0])
        return [tup[1] for tup in ranked[:5]]

    def getRelevantSnippets(self, query, searchResult, top5Indices):
        links = searchResult["link"]
        snippets = searchResult["snippet"]
        titles = searchResult["title"]
        containing = []
        for i in top5Indices:
            url = links[i]
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib2.Request(url,headers=hdr)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            
            # response = requests.get(url)
            # soup = BeautifulSoup(response.content, "html.parser")
            # textbody = soup.get_text()
            texts = soup.findAll('p', text=True)
            def visible(element):
                if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                    return False
                elif re.match('<!--.*-->', element.encode('utf-8')):
                    return False
                return True 

            visible_texts = filter(visible, texts)
            clean_text = [tag.text for tag in visible_texts]
            # print(clean_text)
            textbody = " ".join(clean_text)
            if self.debug is True:
                print(visible_texts)
                print(clean_text)
                print(textbody)
            sentences = clean_text
            containing.append(sentences)
        return containing

    # Returns a weighted metric for similarity evaluation
    # based on Jaccard and Cosine similarities
    def similarityEvaluation(self, query, document):
        jSim = self._getJaccard(query, document)
        cosSim = self._getCosine(query, document)
        externalSim = 0
        if self.similarityFunction is not None:
            externalSim = self.similarityFunction(query, document)
        internalMetric = (jSim*0.4) + (cosSim*0.6)
        internalWeight = 1 - self.functionWeight
        return self.functionWeight*externalSim + internalMetric*internalWeight 

    def spawnBroswerWindow(self, url):
        if sys.platform=='win32':
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                print('Please open a browser on: '+url)

    def _getJaccard(self, source, target):
        tgt_words = re.sub("[^\w]", " ", target).split()
        src_words = re.sub("[^\w]", " ", source).split()
        tgt_word_set = set(tgt_words)
        src_word_set = set(src_words)
        jSim = self._jaccard(tgt_word_set, src_word_set)
        return jSim

    def _jaccard(self, a, b):
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    def _getCosine(self, source, target):
        src_vec = self._text2vec(source)
        tgt_vec = self._text2vec(target)
        cSim = self._cosine(src_vec, tgt_vec)
        return cSim
        


    def _text2vec(self, text):
        words = self.WORD.findall(text)
        return Counter(words)

    def _cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

def main():
    #Simple test Usage of the utility
    print("Enter search query: ")
    query = raw_input()
    sUtil = SearchUtility(debug=False)
    data = sUtil.getDataFromSearch(query)
    print(data)


    #Ordered array of indices with the best matches
    #By default can utilize first index for best results

    # top5 = sUtil.top5ResultsForQuery(query, data)
    # top5Walkthru = sUtil.top5WalkthroughsForQuery(query, data)

    links = data["link"]
    # bestURL = links[top5[0]]

    # bestWalkthru = links[top5Walkthru[0]]
    # sUtil.spawnBroswerWindow(bestURL)
    # sUtil.spawnBroswerWindow(bestWalkthru)
    #Extract sentences containing the query terms, array of len(top5)
    totalMentions = sUtil.getRelevantSnippets(query, data, [0])
    snipsToVoice = totalMentions[0]
    print(snipsToVoice)
    for i in xrange(min(len(snipsToVoice), 3)):
        voice_util = VoiceUtility('voice_files/output.mp3')
        voice_util.utter_phrase(snipsToVoice[i])
    



if __name__ == '__main__':
    main()