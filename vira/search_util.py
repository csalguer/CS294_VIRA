#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""SearchUtility

A module that allows VIRA to search for walkthroughs for video games.

Authored by Ikechi Akujobi, Matthew Chen, Chris Salguero.
CS294W, Spring 2016-2017.
© Stanford University.
"""

from __future__ import print_function
from collections import namedtuple, Counter
import json
import math
import os
import pprint
import re
import subprocess
import sys
import urllib2

from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import pandas as pd
from pandas import DataFrame as df_


class _QueryItem(object):
    def __init__(self, dic):
        self.__dict__.update(dic)

    def __getitem__(self, name):
        return self.__dict__[name]


class _QueryResult(object):
    def __init__(self, dic):
        self.__dict__.update(dic)
        self.items = [_QueryItem(i) for i in self.items if isinstance(i, dict)]

    def __getitem__(self, name):
        return self.__dict__[name]


Config = namedtuple('Config', ['developerKey', 'cx'])


class SearchUtility(object):
    """USES set up CSE on Google Cloud Api to make Search Calls"""
    def __init__(self, similarity_function=None, function_weight=0,
                 configFile=None, debug=False):
        # print("DEBUG MODE: ", debug)
        # Asserts to checks that validity of sim func and weight
        if similarity_function is not None:
            assert 0 < function_weight <= 1.0
        if function_weight is not 0:
            assert similarity_function is not None

        self.similarity_function = similarity_function
        self.function_weight = function_weight
        super(SearchUtility, self).__init__()
        config = Config(**json.load(open(configFile, 'r')))
        self.config = config
        self.service = build("customsearch", "v1",
                             developerKey=self.config.developerKey)
        self.debug = debug
        self.WORD = re.compile(r'\w+')

    def search_google(self, query, **kwargs):
        res = self.service.cse().list(q=query, cx=self.config.cx,
                                      **kwargs).execute()
        return _QueryResult(res)

    def get_data_from_search(self, query):
        iterator, max_iter = 0, 3
        data = []
        res = self.search_google(query)
        data += [df_({k: [item[k] for item in res.items]
                      for k in ['link', 'title', 'snippet']})]
        while 'nextPage' in res.queries and iterator < max_iter:
            start_loc = res.queries['nextPage'][0]['startIndex']
            res = self.search_google(query, start=start_loc)
            data += [df_({k: [item[k] for item in res.items]
                          for k in ['link', 'title', 'snippet']})]
            iterator += 1
        data = pd.concat(data).reset_index(drop=1)
        if self.debug is True:
            pprint.pprint(data)
        return data

    # Rn only returns the indices of the top 5 most similar
    # Must be extended to "slice" the results array
    # including both the _QueryResults structure
    # and it's 3 associated Dict's : Link, Title, Snippet
    def top_results_for_query(self, query, search_result, return_count=5):
        links = search_result["link"]
        snippets = search_result["snippet"]
        titles = search_result["title"]
        similarities = []
        if self.debug is True:
            print("Links: ", links)
            print("Snippets: ", snippets)
            print("Titles: ", titles)
        for (i, title) in enumerate(titles):
            similarities.append((self.get_sim_score(query, title), i))
        ranked = sorted(similarities, key=lambda tup: tup[0])
        return [tup[1] for tup in ranked[:return_count]]

    # Specialized method that performs an extra similarity comparison
    def top_guides_for_query(self, query, search_result, return_count=5):
        if "walkthrough" not in query or "guide" not in query:
            query += " walkthrough"
        links = search_result["link"]
        snippets = search_result["snippet"]
        titles = search_result["title"]
        similarities = []
        if self.debug is True:
            print("Links: ", links)
            print("Snippets: ", snippets)
            print("Titles: ", titles)
        for (i, title) in enumerate(titles):
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib2.Request(links[i], headers=hdr)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            texts = soup.findAll('p', text=True)

            def visible(element):
                if element.parent.name in ['style', 'script', '[document]',
                                           'head', 'title']:
                    return False
                elif re.match('<!--.*-->', element.encode('utf-8')):
                    return False
                return True

            visible_texts = filter(visible, texts)
            clean_text = [tag.text for tag in visible_texts]
            textbody = " ".join(clean_text)
            title_sim = self.get_sim_score(query, title)
            body_sim = self.get_sim_score(query, textbody)
            snippet_sim = self.get_sim_score(query, snippets[i])
            comb_sim = title_sim + body_sim + snippet_sim
            similarities.append((comb_sim, i))
        ranked = sorted(similarities, key=lambda tup: tup[0])
        return [tup[1] for tup in ranked[:return_count]]

    def get_relevant_snippets(self, search_result, top_5_indices):
        links = search_result["link"]
        containing = []
        for i in top_5_indices:
            url = links[i]
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib2.Request(url, headers=hdr)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            texts = soup.findAll('p', text=True)

            def visible(element):
                if element.parent.name in ['style', 'script', '[document]',
                                           'head', 'title']:
                    return False
                elif re.match('<!--.*-->', element.encode('utf-8')):
                    return False
                return True

            visible_texts = filter(visible, texts)
            clean_text = [tag.text for tag in visible_texts]
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
    def get_sim_score(self, query, document):
        jacc_sim = self._get_jaccard(query, document)
        cos_sim = self._get_cosine(query, document)
        ext_sim = 0
        if self.similarity_function is not None:
            ext_sim = self.similarity_function(query, document)
        int_sim = (jacc_sim * 0.4) + (cos_sim * 0.6)
        int_weight = 1 - self.function_weight
        return self.function_weight * ext_sim + int_sim * int_weight

    def spawn_browser_window(self, url):
        if sys.platform == 'win32':
            os.startfile(url)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                print('Please open a browser on: ' + url)

    def _get_jaccard(self, source, target):
        tgt_words = re.sub(r"[^\w]", " ", target).split()
        src_words = re.sub(r"[^\w]", " ", source).split()
        tgt_word_set = set(tgt_words)
        src_word_set = set(src_words)
        return self._jaccard(tgt_word_set, src_word_set)

    def _jaccard(self, set_a, set_b):
        set_c = set_a.intersection(set_b)
        return float(len(set_c)) / (len(set_a) + len(set_b) - len(set_c))

    def _get_cosine(self, source, target):
        src_vec = self._text2vec(source)
        tgt_vec = self._text2vec(target)
        return self._cosine(src_vec, tgt_vec)

    def _text2vec(self, text):
        words = self.WORD.findall(text)
        return Counter(words)

    def _cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if denominator:
            return float(numerator) / denominator
        return 0.0


def main():
    """Simple test usage of the search utility."""
    import voice_util
    print("Enter search query: ")
    query = raw_input()
    config_file_path = os.path.join("config_files", "search.json")
    search_util = SearchUtility(configFile=config_file_path)
    data = search_util.get_data_from_search(query)
    total_mentions = search_util.get_relevant_snippets(data, [0])
    snips_to_voice = total_mentions[0]
    for i in xrange(min(len(snips_to_voice), 3)):
        voice_output_path = os.path.join("voice_files", "output.mp3")
        voice_utility = voice_util.VoiceUtility(voice_output_path)
        voice_utility.utter_phrase(snips_to_voice[i])


if __name__ == '__main__':
    main()
