import os
from flask import jsonify, request, abort, json
from flask import Flask, render_template
import requests
import pandas
import ast

app = Flask(__name__)

# Google Sheets API Setup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
gsheet = client.open("BS_Database").sheet1


#Controller
@app.route('/', methods=["GET"])
def home():
    data = json.dumps(gsheet.get_all_records())
    lists = ast.literal_eval(data)
    return render_template('home.html', result=lists)

@app.route("/upload")
def upload():
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)

