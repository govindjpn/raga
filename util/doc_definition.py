from dataclasses import dataclass
from datetime import datetime as dt

@dataclass
class Document : 
    doc_id : int 
    doc_name : str
    doc_pathname : str 
    doc_password : str
    doc_type : str 
    doc_page_count : int 
    doc_summary : str 
    doc_active_flg : bool 

    def __init__(self, **kwargs):
        for k in self.__dataclass_fields__:
            setattr(self, k, None)

        for k, v in kwargs.items():
            setattr(self, k, v)

@dataclass
class CaptiveDocument (Document):
    country : str
    state : str
    stage : str 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for k in self.__dataclass_fields__:
            setattr(self, k, None)

        for k, v in kwargs.items():
            setattr(self, k, v)


if __name__ == "__main__" : 
    d1 = Document(doc_id=1)
    d2 = CaptiveDocument(doc_id=2, country="US")

    print (f"{d1} \n {d2} \n{d2.country}")

