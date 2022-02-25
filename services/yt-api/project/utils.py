from datetime import datetime
from project import es

def convert_iso_to_python(iso_date_time):
    """
        Converts ISO formatted time to Python DateTime object 
    """
    timestamp = datetime.fromisoformat(iso_date_time[:-1] + '+00:00')
    return timestamp


def convert_python_to_iso(python_date_time):
    """
        Converts Python DateTime object to ISO formatted time
    """
    timestamp = python_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return timestamp

def store_record(index_name, doc_type, record):
    try:
        outcome = es.index(index=index_name, doc_type=doc_type, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))

def search(index_name, search):
    res = es.search(index=index_name, body=search)
    print(res)