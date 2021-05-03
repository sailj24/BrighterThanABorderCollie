# BrighterThanABorderCollie
All the work for Spring 2021 Software Engineering group project - student solidarity account. <br />
Project Goal: A Document Repository for students to share and access study resources. <br />
How it works: <br />
-HTML templates provide the user experience (see "templates"). <br />
-Home page is a grid showing identification information for each document the students upload. It is open to the public. Each row on the grid includes a download button for that row's document. Also included on this page is an upload button that redirects to the upload.html page <br />
-Upload page is a form with an upload button. This feeds information to the main, which creates a document in Google Docs and stores information in the Excel Spreadsheet. Upon completion of uploading, redirects to upload_successful, which has a redirect option to the Home Page <br />
-data comes from documents stored on Google Docs, with identification information stored in an Excel Spreadsheet. HTML templates provide a view of data <br />
-filter method within main allows students to narrow down their options when seeking a specific document. First, it creates the grid with every document available, then filters by whichever characteristics (class subject or class grade) the student chooses to narrow down his/her options.

Technologies used: <br />
-Python for logic <br />
-Flask for HTML interfacing <br />
-Heroku for deployment <br />