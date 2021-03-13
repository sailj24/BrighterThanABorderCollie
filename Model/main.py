from subjects import subject
from docs import doc
from users import user
from grades import grade

s = subject(1, 'Math')
g = grade(3, 'Freshman')
p = user(2, 'Carlos Gomez', 'cgomez23', 'beast', [])

d1 = doc(201, 'calc', 'NaN', 'Osinac', g, s, p)
d2 = doc(202, 'calc', 'NaN', 'Osinac', g, s, p)
d3 = doc(203, 'calc', 'NaN', 'Osinac', g, s, p)

p.docs.append(d1)
p.docs.append(d2)
p.docs.append(d3)

print([n.id for n in p.docs])



