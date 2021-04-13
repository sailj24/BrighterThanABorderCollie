
from Model.docs import doc
from Model.grades import grade
from Model.subjects import subject

from flask import Flask, render_template, redirect
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from flask import jsonify, request, abort, json
import flask
#from google import Create_Service

#label: start
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ast
import os
import threading

app = Flask(__name__)

#Google API initialization
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"])

client = gspread.authorize(credential)
drive_service = build('drive', 'v3', credentials=credential)

#globals
docs = []
grades = []
subjects = []
headers = []
docs_table = None

def start():
    #local variable initialization
    global docs_table
    docs_table = client.open("BS_Database").sheet1
    grade_table = client.open("BS_Database").get_worksheet(1)
    subject_table = client.open("BS_Database").get_worksheet(2)


    data = json.dumps(docs_table.get_all_records())
    doc_lists = ast.literal_eval(data)

    grade_str = json.dumps(grade_table.get_all_records())
    grades_maps = ast.literal_eval(grade_str)

    subject_str = json.dumps(subject_table.get_all_records())
    subjects_map = ast.literal_eval(subject_str)

    # headers
    global headers 
    headers = ['Download Link', 'Name of Document', 'Uploader', 'Grade', 'Subject']

    # doc, subject, and grade object lists
    # start off empty for refresh capabilities
    global docs
    docs = []
    global grades
    grades = []
    global subjects
    subjects = []

    #getting data ready
    for d in doc_lists:
        values = [value for value in d.values()]
        #print(values)
        input_doc = doc(values[2], values[3], values[6], values[1], values[5], values[7], values[0], values[4]) 
        docs.append(input_doc)
        

    for d in grades_maps:
        values = [value for value in d.values()]
        in_grade = grade(values[0], values[1])
        grades.append(in_grade)
        #print(values)

    for d in subjects_map:
        values = [value for value in d.values()]
        in_subject = subject(values[0], values[1])
        subjects.append(in_subject)
        #print(values)



#functions
def name_to_int(name):                      #way to jump back and forth between a name and id
    for grade in grades:
        if name == grade.name:
            return grade.id
    for subject in subjects:
        if name == subject.name:
            return subject.id

def int_to_name(int):
    for grade in grades:
        if int == grade.id:
            return grade.name
    for subject in subjects:
        if int == subject.id:
            return subject.name

def upload_doc(fileI, name, docName, prof, gID, sID):
    folder_id = ['1XxXFS8QmngAW7Jat4rgsL1G8M_jQfaCu']
    file_name, file_extension = os.path.splitext(fileI.filename)
    file_metadata = {'name': fileI.filename, 'parents' : folder_id}
    f = fileI.stream
    media = MediaIoBaseUpload(f, mimetype=fileI.mimetype, chunksize=-1, resumable = True)
    file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    id = file.get('id')
    permission1 = {
        'type': 'user',
        'role': ['writer', 'reader'],
        'emailAddress': 'BrighterSpace13@gmail.com',  # Please set your email of Google account.
    }
    permission2 = {
                'value'    : '',
                'type'     : 'anyone',
                'role'     : 'reader',
                'withLink' : 'true',
                }
    drive_service.permissions().create(fileId=id, body=permission1).execute()
    drive_service.permissions().create(fileId=id, body=permission2).execute()

    row = next_available_row(docs_table)
    docs_table.update_cell(row, 1, id)
    docs_table.update_cell(row, 2, docName)
    docs_table.update_cell(row, 4, 'N/A')
    docs_table.update_cell(row, 5, gID)
    docs_table.update_cell(row, 6, sID)
    docs_table.update_cell(row, 3, name)
    docs_table.update_cell(row, 7, file_extension.strip('.'))
    docs_table.update_cell(row, 8, prof)



def display_all_docs():                             #fills the list
    filtered_array = []
    for doc in docs:        
        g = int_to_name(doc.gradeID)
        s = int_to_name(doc.subjectID)
        doc_arr = [doc.id, doc.doc_URL, doc.name, doc.create_user, g, s]
        filtered_array.append(doc_arr)
    return filtered_array


#def filter_docs(gID, sID):
 #   filtered_array = []
  #  g = [g.name for g in grades if int(g.id) == int(gID)][0]
   # s = [s.name for s in subjects if int(s.id) == int(sID)][0]
    #for doc in docs:
     #   if doc.subjectID == int(sID) and doc.gradeID == int(gID):
      #      doc_arr = [doc.id, doc.doc_URL, doc.name, doc.create_user, g, s]
       #     filtered_array.append(doc_arr)
   # return filtered_array


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    next_available_row = len(str_list)+1
    return next_available_row

def get_doc(id):
    for d in docs:
        if d.id == id:
            return d
    #return [d for d in docs if d.id == id][0]        #built-in error message works, if you write this condition the long way around

def filter_docs(ID, array):                         #filters into new list
    new_array = []
    if ID is None:                                  #if that dropdown wasn't filled out
        return array
    for doc in array:                               #doc is a list, seen above in creation of doc_arr
        if str(name_to_int(doc[4])) == ID or str(name_to_int(doc[5])) == ID: 
            doc_arr = [doc[0], doc[1], doc[2], doc[3], doc[4], doc[5]]
            new_array.append(doc_arr)
    return new_array


start()

#Controller
@app.route('/', methods=["GET"])
def home():
    #start()
    all_docs = display_all_docs()
    return render_template('home.html', header=headers, data=all_docs, grades=grades, subjects=subjects)

@app.route('/search', methods=["GET", "POST"])
def search():
    filtered_docs = display_all_docs()                  #necessary to first fill list
    gID = request.args.get('gID', None)
    sID = request.args.get('sID', None)
    if gID is None and sID is None:
        return redirect("/")
    filtered_docs = filter_docs(gID, filtered_docs)     #filter using one category
    filtered_docs = filter_docs(sID, filtered_docs)     #filter using the other category
    return render_template('home.html', header=headers, data=filtered_docs)

@app.route("/upload")
def upload():
    return render_template("upload.html", grades=grades, subjects=subjects)

@app.route("/uploader", methods=['POST'])
def uploader():
    fileI = request.files['file']
    name = request.form['name']
    docName = request.form['docName']
    prof = request.form['prof']
    gID = request.form['gID']
    sID = request.form['sID']
    
    t = threading.Thread(target=upload_doc, args=(fileI, name, docName, prof, gID, sID))
    t2 = threading.Thread(target=start)
    t.daemon, t2.daemon = True, True
    t.start(), t2.start(), t.join(), t2.join()
    #start()

    return redirect("/")

@app.route("/doc_page", methods=["GET", "POST"])
def doc_page():
    id = request.args.get('id', None)
    docObj = get_doc(id)
    return render_template("doc.html", doc=docObj)


if __name__ == "__main__":
    app.run(debug=True)


print(filter_docs(13,1))