import os
from teradatamlspk.converter.utils import Script, Directory, Notebook

def pyspark2teradataml(file_path):
    """Utility which analyses and produces the script/ notebook to run on Teradata Vantage. """
    if (not os.path.exists(file_path)):
        raise FileNotFoundError("Path '{}' not found.".format(file_path))
    
    if os.path.isdir(file_path):
        Directory(file_path).process()
    elif os.path.splitext(file_path)[1] == '.ipynb':
        Notebook(file_path).process()
    else:
        Script(file_path).process()
