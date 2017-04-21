from types import MethodType

def set_score(self, score):
    self.score = score

class Student(object):
    __slot__ = ('name', 'age')
    name = 'Student'
    pass

Student.name = 'Student'
Student.set_score = MethodType(set_score, Student)

s = Student()
#s.setscore(99)

print (Student.__dict__)
