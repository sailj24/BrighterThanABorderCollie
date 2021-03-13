from subjects import subject
from grades import grade
from users import user

class doc:
    id = 0
    name = ''
    doc_URL = ''
    professor = ''
    current_grade = grade()
    current_subject = subject()
    create_user = user()


    def __init__(self, id, name, doc_URL, professor, grade, subject, user):
        self.id = id
        self.name = name
        self.doc_URL = doc_URL
        self.professor = professor
        self.current_grade = grade
        self.curretn_subject = subject
        self.create_user = user
    
    def printName(self):
        print(self.name)