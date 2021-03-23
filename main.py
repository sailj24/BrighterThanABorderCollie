from Model.docs import doc
from Model.grades import grade
from Model.subjects import subject

from flask import Flask, render_template, redirect

app = Flask(__name__)

from flask import jsonify, request, abort, json

#label: start
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ast

#Google Sheets API initialization
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)

#local variable initialization
docs_table = client.open("BS_Database").sheet1
grade_table = client.open("BS_Database").get_worksheet(1)
subject_table = client.open("BS_Database").get_worksheet(2)


data = json.dumps(docs_table.get_all_records())
doc_lists = ast.literal_eval(data)

grade_str = json.dumps(grade_table.get_all_records())
grades_maps = ast.literal_eval(grade_str)

subject_str = json.dumps(subject_table.get_all_records())
subjects_map = ast.literal_eval(subject_str)

#headers
headers = ['Download Link', 'Name of Document', 'Uploader', 'Grade', 'Subject']

#all docs from google sheet
docs = []

#subject and grade object lists
grades = []
subjects = []

#getting data ready
for d in doc_lists:
    values = [value for value in d.values()]
    input_doc = doc(values[1], values[2], values[4], values[0], values[3], values[5]) 
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
def display_all_docs():
    filtered_array = []
    for doc in docs:
        g = [g.name for g in grades if g.id == doc.gradeID][0]
        s = [s.name for s in subjects if s.id == doc.subjectID][0]
        doc_arr = [doc.doc_URL, doc.name, doc.create_user, g, s]
        filtered_array.append(doc_arr)
    return filtered_array

def filter_docs(gID, sID):
    filtered_array = []
    g = [g.name for g in grades if int(g.id) == int(gID)][0]
    s = [s.name for s in subjects if int(s.id) == int(sID)][0]
    for doc in docs:
        if doc.subjectID == int(sID) and doc.gradeID == int(gID):
            doc_arr = [doc.doc_URL, doc.name, doc.create_user, g, s]
            filtered_array.append(doc_arr)
    return filtered_array


#filter = 
#Controller
@app.route('/', methods=["GET"])
def home():
    all_docs = display_all_docs()
    return render_template('home.html', header=headers, data=all_docs, grades=grades, subjects=subjects)

@app.route('/search', methods=["GET", "POST"])
def search():
    gID = request.args.get('gID', None)
    sID = request.args.get('sID', None)
    if gID is None or sID is None:
        return redirect("/")
    filtered_docs = filter_docs(gID, sID)
    return render_template('home.html', header=headers, data=filtered_docs)

@app.route("/upload")
def upload():
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)

