class doc:
    id = 0
    name = ''
    doc_URL = ''
    professor = ''
    gradeID = 0
    subjectID = 0
    create_user = ''


    def __init__(self, id, name, doc_URL, gradeID, subjectID, user):
        self.id = id
        self.name = name
        self.doc_URL = doc_URL
        self.gradeID = gradeID
        self.subjectID = subjectID
        self.create_user = user
    
    def printName(self):
        print(self.name)