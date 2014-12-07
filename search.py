import numpy as np
import scipy as sc
import pandas as pd
import matplotlib.pyplot as plt
import re, os, sys
import tarfile
from datetime import datetime as dt

import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

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

def search(searcher, analyzer):
	query = QueryParser(Version.LUCENE_CURRENT, content_field, analyzer).parse('temperature and velocity')
	scoreDocs = searcher.search(query, 20).scoreDocs

	print 'total matching docs: ', len(scoreDocs)

	for scoreDoc in scoreDocs:
		doc = searcher.doc(scoreDoc.doc)
		print 'docid ', doc.get(docid_field)
		print '%s\n' % doc.get(title_field)
		print 'by %s\n' % doc.get(author_field)
		print '%s \n' % doc.get(content_field)

		print '#######################'


def main():
	lucene.initVM()
	print 'lucene version ', lucene.VERSION
	version = Version.LUCENE_CURRENT
	directory = SimpleFSDirectory(File(index_path))
	searcher = IndexSearcher(DirectoryReader.open(directory))
	analyzer = StandardAnalyzer(version)

	start = dt.now()
	search(searcher, analyzer)
	end = dt.now()
	del searcher

	print 'elapsed time searching:'
	print end - start



if __name__ == '__main__':
	main()
