import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardTokenizer, StandardFilter
from org.apache.lucene.analysis.core import LowerCaseFilter, StopFilter, StopAnalyzer
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.util import Version
from org.apache.pylucene.analysis import PythonAnalyzer


class PorterStemmerAnalyzer(PythonAnalyzer):
    def createComponents(self, fieldName, reader):
        source = StandardTokenizer(Version.LUCENE_CURRENT, reader)
        filter = StandardFilter(Version.LUCENE_CURRENT, source)
        filter = LowerCaseFilter(Version.LUCENE_CURRENT, filter)
        filter = PorterStemFilter(filter)
        filter = StopFilter(Version.LUCENE_CURRENT, filter, StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        return self.TokenStreamComponents(source, filter)
