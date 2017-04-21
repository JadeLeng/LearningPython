from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'March', 'Apr', 'May', 'Jun',
    'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'))

for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)
