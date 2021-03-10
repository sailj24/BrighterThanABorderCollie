import sys
from datetime import date
import urllib.request


class DocBuilder:

    def DocBuilder():
        self.pdf = with urllib.request.urlopen('http://www.python.org/') #placeholder URL, need to find initial PDF link
        self.name = "MyDoc"                                                #doc name
        self.id = date.today().strftime() + "UPLOADER Name"                #uploader name and upload date
        self.subject_id = with urllib.request.urlopen('http://www.python.org/') 
        self.grade_id = with urllib.request.urlopen('http://www.python.org/') 
        #placeholder URL, still determining whether subject)id and grade_id should point to a class object, URL, or string
        #want to hash the id to include uploader's name and date to reduce concerrency redundancy

  
#Implementation of Builder: Within the main stack, we initialize a DocBuilder my_doc_builder 
#  call each of its parameters separately to change them (the normal way you call parameters! No special methods needed, 
#               unless we want to do heavy-duty stuff for the params)
#  then call Doc constructor with my_doc_builder, and it will all take care of itself :) One design pattern down!

class Doc:

    def __init__(DocBuilder:builder):
        self.pdf = builder.pdf
        self.name = builder.name
        self.id = builder.id
        self.subject_id = builder.subject_id
        self.grade_id = builder.grade_id
    
    


