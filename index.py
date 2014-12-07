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
from org.apache.lucene.index import IndexWriterConfig, IndexWriter, FieldInfo
from org.apache.lucene.document import Document, Field, FieldType, IntField
from org.apache.lucene.store import SimpleFSDirectory
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

def indexCranFull(path, writer):
    """
    This method reads in the cran.1400 file and creates an index out of it.

    These fields are used when storing documents:
        title: title of the document (in a line starting with .T)
        author: author of the document (in a line starting with .A)
        source: where this article has been published, not yet used (in a line starting with .B)
        content: body text of the article (in a line starting with .W)
    """
    # Title field type
    tft = FieldType()
    tft.setIndexed(True)
    tft.setStored(True)
    tft.setTokenized(TokenizeFields)
    tft.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS) #only index the document and frequency data


    # Author field type
    aft = FieldType()
    aft.setIndexed(True)
    aft.setStored(True)
    aft.setTokenized(TokenizeFields)
    aft.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS) #index the document, term frequency and position data


    # Content field type
    cft = FieldType()
    cft.setIndexed(True)
    cft.setStored(True)
    cft.setTokenized(True)
    cft.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    txt = open(path)
    """
    cran documents are listed in this order:
    .I # -> ignore
    .T -> starting on the next line, multi-line title
    .A -> on the next line, multiple authored separated by 'and'
    .B -> on the next line, ignore
    .W -> starting on the next line, multi-line body (content)
    """
    docid = 0
    debug = False
    while True: # in each iteration, read all the lines corresponding to a document
        line = txt.readline()

        if line == '':
            break

        if docid == 1400:
            debug = True

        if line.startswith('.I'):
            docid = int(line.split(' ')[1].strip())
            continue

        if line.startswith('.T'):
            title = ''
            while True:
                line = txt.readline()
                if line.startswith('.A'):
                    break
                title = ' '.join([title, line])

            line = txt.readline()
            authors = ' '.join(line.split('and'))

            #.B, its corresponding line and .W
            txt.readline()
            txt.readline()
            txt.readline()
            body = ''
            while True:
                line = txt.readline()
                if line.startswith('.I'):
                    docid = int(line.split(' ')[1].strip())
                    break
                if line == '':
                    break
                body = ' '.join([body, line])

            doc = Document()
            doc.add(Field(title_field, title, tft))
            doc.add(Field(author_field, authors, aft))
            doc.add(Field(content_field, body, cft))
            doc.add(IntField(docid_field, docid, Field.Store.YES))
            writer.addDocument(doc)


def main():
    lucene.initVM()
    print 'lucene version ', lucene.VERSION
    version = Version.LUCENE_CURRENT
    index_store = SimpleFSDirectory(File(index_path))
    analyzer = StandardAnalyzer(version)
    config = IndexWriterConfig(version, analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(index_store, config)

    start = dt.now()
    indexCranFull(document_path, writer)
    writer.commit()
    writer.close()
    end = dt.now()

    print 'elapsed time for indexing documents:'
    print end - start

if __name__ == '__main__':
	main()
