import numpy as np
import scipy as sc
import pandas as pd
import matplotlib.pyplot as plt
import re, os, sys
import tarfile
from datetime import datetime as dt

from util import *

import lucene
from java.io import File
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

from customAnalyzer import PorterStemmerAnalyzer

document_folder = 'cran/'
document_name = 'cran.all.1400'
document_path = os.path.join(document_folder, document_name)

index_folder = '.'
index_name = 'cran.index'
index_path = os.path.join(index_folder, index_name)

# Options
TokenizeFields = True

#field names:
title_field = 'title'
author_field = 'author'
content_field = 'content'
docid_field = 'docid'

#total number of documents
total_docs = 1400

def search(searcher, analyzer, query_text):
	"""
	searches the index for the query_text and returns an sorted list of documents as a result of the query

	Parameters
	----------
	searcher: pyLucene Search object
			  an object that will perform a search for a query in a given index
	analyzer: pyLucene Analyzer object
			  an object for performing textual analysis on the query text and transforming
			  input text to the format in which index over documents have been made
	query_text: str
			  query text for which searcher will provide a sorted list of document in order of relevance

	Returns:
	rel_docs: list
			  a sorted list of document IDs in order of relevance
	"""
	query = QueryParser(Version.LUCENE_CURRENT, content_field, analyzer).parse(query_text)
	scoreDocs = searcher.search(query, total_docs).scoreDocs

	print 'total matching docs: ', len(scoreDocs)

	# for scoreDoc in scoreDocs:
	# 	doc = searcher.doc(scoreDoc.doc)
	# 	print 'docid ', doc.get(docid_field)
	# 	print '%s\n' % doc.get(title_field)
	# 	print 'by %s\n' % doc.get(author_field)
	# 	print '%s \n' % doc.get(content_field)
	#
	# 	print '#######################'
	rel_docs = []
	for scoreDoc in scoreDocs:
		doc = searcher.doc(scoreDoc.doc)
		rel_docs.append(doc.get(docid_field))
	return rel_docs

def main():
	lucene.initVM()
	print 'lucene version ', lucene.VERSION
	version = Version.LUCENE_CURRENT
	directory = SimpleFSDirectory(File(index_path))
	searcher = IndexSearcher(DirectoryReader.open(directory))
	analyzer = PorterStemmerAnalyzer()

	queryRels = queryRelevance()

	start = dt.now()
	for qr in queryRels[:50]:
		query = qr["query"]
		reldocs = qr["reldocs"]

		predicted = search(searcher, analyzer, query)
		p = precision(reldocs, predicted)
		r = recall(reldocs, predicted)
		plt.plot(r, p)
		# plt.show()
		print 'max recall'
		print max(r)
		print 'max precision'
		print max(p)
		elevenPAP = elevenPointAP(p, r)
		print len(elevenPAP), '-point interpolated average precision'
		print elevenPAP
		meanAP = mapk(reldocs, predicted, len(r))
		print 'mean average precision'
		print meanAP
		print ''
	plt.show()
	end = dt.now()
	del searcher

	print 'elapsed time'
	print end - start



if __name__ == '__main__':
	main()
