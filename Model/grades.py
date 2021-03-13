class grade:
    id = 0
    name = ''

    def __init__(self, id=0, name=''):
        self.id = id
        self.name = name
    
    def printName(self):
        print(self.name)

# g = grade(1, 'Freshman')

# g.printName()
