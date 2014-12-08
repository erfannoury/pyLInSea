import numpy as np
from prettyprint import pp

queryRootPath = 'Data/Queries/Q'
relevanceFile = 'Data/RelevancyJudgments/relevance'

def queryRelevance():
    """
    this method will parse the query relevance judgement file and
    corresponding queries and will return a list of dictionaries
    containing the query and a list of relevant documents

    Returns
    -------
    queryRel: list
              a list of pairs of queries and lists of relevant document
              list({'query', list('reldocs')})
    """
    queryRel = []
    rel = open(relevanceFile)
    while True:
        line = rel.readline()
        if line == '':
            break
        tokens = line.strip().split(' ')
        qid = tokens[0]
        tokens = tokens[1:]
        query_text = open(queryRootPath+qid).read()
        qr = {'query':query_text, 'reldocs': tokens}
        queryRel.append(qr)

    return queryRel



#Code copied from https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/average_precision.py
def apk(actual, predicted, k=10):
    """
    Computes the average precision at k.

    This function computes the average precision at k between two lists of
    items.

    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The average precision at k over the input lists

    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 1.0

    return score / min(len(actual), k)

def mapk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.

    This function computes the mean average prescision at k between two lists
    of lists of items.

    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The mean average precision at k over the input lists

    """
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])

def elevenPointAP(precision, recall):
    """
    Computes the 11-point interpolated average precision for a list of corresponding precision and recall values.

    Parameters
    ----------
    precision: list
               A list of precision values computed for the retrieved documents against the ground-truth relevant documents
    recall: list
            A list of recall values computed for the retrieved documents against the ground-truth relevant documents

    Returns
    -------
    epap: list
          a list of interpolated average precision at predefined recall values (at [0.0..0.1..1.0])
    """
    epap = []
    start_idx = 0
    for r in np.arange(0,1.1, 0.1):
        for i in range(start_idx, len(precision)):
            if recall[i] == r:
                epap.append(max(precision[i:]))
                start_idx = i+1
                break
            elif (i < len(precision) - 1) and recall[i] < r and recall[i+1] > r:
                epap.append(max(precision[i+1:]))
                start_idx = i+2
                break

    return epap

def precision(actual, predicted):
    """
    Computes the precision values for all sublists of predicted elements starting from the first element.

    Parameters
    ----------
    actual: list
            a list of relevant documents
            (doesn't need to be ordered)
    predicted: list
               an ordered list of predicted documents
               (should be ordered)

    Returns
    -------
    p: list
       a list of precision values for every sublist of predicted documents in predicted[:i]
    """
    p = []

    for i in range(len(predicted)):
        tp = [doc for doc in predicted[:i+1] if doc in actual]
        p.append(len(tp) * 1.0 / (i+1))

    return p

def recall(actual, predicted):
    """
    Computes the recall value of all sublists of predicted elements starting from the first element.

    Parameters
    ----------
    actual: list
            a list of relevant documents
            (doesn't need to be ordered)
    predicted: list
               an ordered list of predicted documents
               (should be ordered)

    Returns
    -------
    r: list
       a list of recal values for every sublist of predicted documents in predicted[:i]
    """
    la = len(actual)
    r = []

    for i in range(len(predicted)):
        tp = [doc for doc in predicted[:i+1] if doc in actual]
        r.append(len(tp) * 1.0 / la)

    return r
