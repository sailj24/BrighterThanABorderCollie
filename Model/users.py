class user:
    id = 0
    name = ''
    username = ''
    password = ''
    docs = []

    def __init__(self, id=0, name='', username='', password='', docs=[]):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.docs = docs
    
    def printName(self):
        print(self.name)