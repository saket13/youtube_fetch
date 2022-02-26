from project import es

def push_data_to_es(index_name, doc_type, record):
    """
        Push data records to Elastic Search index with doc_type
    """
    try:
        outcome = es.index(index=index_name, doc_type=doc_type, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))

def query_data_from_es(index_name, search):
    """
        Query Elastic Search index with json search object
    """
    res = es.search(index=index_name, body=search)
    return res