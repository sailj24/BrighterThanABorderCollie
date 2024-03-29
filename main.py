####################################
# App: BrighterThanABorderCollie
# Authors: Carlos Gomez, Kathleen Blute, Clarissa Skipworth, Sri Harini
# Date of Final Draft: 5/4/21
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

# Google API initialization
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"])
# sheets
client = gspread.authorize(credential)
# drive
drive_service = build('drive', 'v3', credentials=credential)

#globals
docs = []
grades = []
subjects = []
headers = []
docs_table = None

def start():
    global docs_table
    docs_table = client.open("BS_Database").sheet1
    grade_table = client.open("BS_Database").get_worksheet(1)
    subject_table = client.open("BS_Database").get_worksheet(2)

    # converting sheet info to lists of lists.
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
    # start off empty for refresh capabilities.
    global docs
    docs = []
    global grades
    grades = []
    global subjects
    subjects = []

    # getting data ready by putting each row from 
    # each sheet into a doc, grade, or subject object.
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



# functions

# function to jump back and forth between a name and id.
# params: string name
# return: int subject/grade id
def name_to_int(name):
    for grade in grades:
        if name == grade.name:
            return grade.id
    for subject in subjects:
        if name == subject.name:
            return subject.id

# function to jump back and forth between a id and name.
# params: int subject/grade id
# return: int subject/grade name
def int_to_name(int):
    for grade in grades:
        if int == grade.id:
            return grade.name
    for subject in subjects:
        if int == subject.id:
            return subject.name

# function to upload document information to the google spread sheet database and
# the actual document to google drive.
# params: fileInput IO, string username, string documentName, string gradeID, string subjectID 
# return: string idOfDocInDrive, docExtension
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
    
    # permissions to give read access to our actual
    # account and to give read access to any user on
    # the website.
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

    return id, file_extension

# function to get all information on all docs in database.
# return: list of lists with limited doc information for each doc
def display_all_docs():
    filtered_array = []
    for doc in docs:        
        g = [g.name for g in grades if int(g.id) == int(doc.gradeID)][0] # grabs names of grades
        s = [s.name for s in subjects if int(s.id) == int(doc.subjectID)][0] # grabs names of subjects
        doc_arr = [doc.id, doc.doc_URL, doc.name, doc.create_user, g, s]
        filtered_array.append(doc_arr)
    return filtered_array

#backup filter function
#def filter_docs(gID, sID):
 #   filtered_array = []
  #  g = [g.name for g in grades if int(g.id) == int(gID)][0]
   # s = [s.name for s in subjects if int(s.id) == int(sID)][0]
    #for doc in docs:
     #   if doc.subjectID == int(sID) and doc.gradeID == int(gID):
      #      doc_arr = [doc.id, doc.doc_URL, doc.name, doc.create_user, g, s]
       #     filtered_array.append(doc_arr)
   # return filtered_array

# function to return the next available row in 
# google sheets for appending doc metadata.
# params: worksheet object
# return: int next_available_row
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    next_available_row = len(str_list)+1
    return next_available_row


#doc.html gets doc field information from being given it here
def get_doc(id):
    for d in docs:
        if d.id == id:
            return d
    #return [d for d in docs if d.id == id][0]      # built-in error message works, 
                                                    # if you write this condition the long way around

# function to filter doc view down by grade or subject id.
# params: subject/grade id, docView array
# return: filtered_doc array
def filter_docs(ID, array):
    new_array = []
    if ID is None:                                  #if that dropdown wasn't filled out
        return array
    for doc in array:                               #doc is a list, seen above in creation of doc_arr
        if str(name_to_int(doc[4])) == ID or str(name_to_int(doc[5])) == ID: 
            doc_arr = [doc[0], doc[1], doc[2], doc[3], doc[4], doc[5]]
            new_array.append(doc_arr)
    return new_array

# initiates the data for the view
start()

#Controller

# displays the home page with all available docs
@app.route('/', methods=["GET"])
def home():
    #start()
    all_docs = display_all_docs()
    return render_template('home.html', header=headers, data=all_docs, grades=grades, subjects=subjects)

# search API and diplays filtered doc 
# list based on grade and subject id.
@app.route('/search', methods=["GET", "POST"])
def search():
    filtered_docs = display_all_docs()                  #necessary to first fill list
    gID = request.args.get('gID', None)                 #gets id's from URL
    sID = request.args.get('sID', None)
    if gID is None and sID is None:
        return redirect("/")
    filtered_docs = filter_docs(gID, filtered_docs)     #filter using one category
    filtered_docs = filter_docs(sID, filtered_docs)     #filter using the other category
    return render_template('home.html', header=headers, data=filtered_docs)

@app.route("/upload")
def upload():
    return render_template("upload.html", grades=grades, subjects=subjects)

# post API to upload doc and metadata on 
# doc to google sheets and drive.
@app.route("/uploader", methods=['POST'])
def uploader():
    fileI = request.files['file']
    name = request.form['name']
    docName = request.form['docName']
    prof = request.form['prof']
    gID = request.form['gID']
    sID = request.form['sID']
    
    id, mimetype = upload_doc(fileI, name, docName, prof, gID, sID)
    d = doc(id, docName, 'N/A', gID, sID, name, mimetype, prof)
    docs.append(d)
    #start()
    return redirect ("/upload_successful")

# based on doc id, displays a document page
# with informaiton on one document
@app.route("/doc_page", methods=["GET", "POST"])
def doc_page():
    id = request.args.get('id', None)
    docObj = get_doc(id)
    docObjGrade = int_to_name(docObj.gradeID)
    docObjSubject = int_to_name(docObj.subjectID)

    return render_template("doc.html", doc=docObj, grade=docObjGrade, subject=docObjSubject)

# displays confimation page that document was
# successfully uploaded 
@app.route("/upload_successful", methods=["Get"])
def upload_successful():
    return render_template("upload_successful.html")

if __name__ == "__main__":
    app.run(debug=True, TEMPLATES_AUTO_RELOAD=True)

