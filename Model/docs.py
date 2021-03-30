class doc:
    id = ''
    name = ''
    doc_URL = ''
    professor = ''
    gradeID = 0
    subjectID = 0
    create_user = ''
    extension = ''


    def __init__(self, id, name, doc_URL, gradeID, subjectID, user, extension, professor):
        self.id = id
        self.name = name
        self.doc_URL = doc_URL
        self.gradeID = gradeID
        self.subjectID = subjectID
        self.create_user = user
        self.extension = extension
        self.professor = professor
    
    def printName(self):
        print(self.name)