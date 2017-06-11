#Lyy的Python学习笔记

## Generator  
节省空间，一边循环一边计算：  

```python
	g = (x * x for x in range(10))	#列表生成式从[]换成()
	g.next()

```

同样，在函数遍历中，使用yield来打印，也是一个generator：  

```python
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1

```

把函数改成generator后，我们基本上从来不会用next()来调用它，而是直接使用for循环来迭代：  

```python
for n in fib(6):
	print n
```
切片斐波那契数列：  

```python
def fib(max):
    n, a, b = 0, 0, 1
    while(n < max):
        yield b
        a, b = b, a+b
        n += 1

def slfib(fr=0, to=1):
    return [x for x in fib(to) if x not in fib(fr)]
    
#同样可以使用list自带的切片

l = [x for x in fib(10)]
print l[1:3]
```

## Map & Reduce
Map: map(f,[]) 把[]中所有数据通过函数f计算  
Reduce: reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)  

利用reduce完成整数合并：

```python
def fn(x, y):
	return x * 10 + y
	
reduce(fn,['1','3','5','7','9'])

#改进，完成str2int，利用lambda

def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

def str2int(s):
    return reduce(lambda x,y: x*10+y, map(char2num, s))

```

练习可参考Code/Mapreduce_exercise.py

## Filter
埃氏筛法求素数：
首先，要理解埃氏筛法。  
自然数1到n，[1:n]，首先删除1，  
然后读取2，删除2的倍数，  
读取当前队列最小的3，删除3的倍数，  
这样每一次当前队列的最小数就一定是素数。

```python
#首先构造一个从3开始的奇数序列
def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
#然后定义一个筛选函数（是否可以整除）
def _not_divisible(n):
    return lambda x: x % n > 0
#最后定义一个generator
def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列


```

## sorted()  
sorted([], key, reverse)  
个人理解是把key规则map到[]的每一个元素上，然后根据map后的[]进行排序。  

```python
# 根据字母序降序  
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)  
```

## 返回函数  
注意函数生成不是立即执行，所以对于变量的引用，要注意即时性：  

```python
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
# 和以下程序的区别
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs
```

## 匿名函数  
直接上代码吧
```python
list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

>>> f = lambda x: x * x
>>> f
<function <lambda> at 0x101c6ef28>
>>> f(5)
25
# 把匿名函数作为返回值返回
def build(x, y):
    return lambda: x * x + y * y
```

## 装饰器
如log，不修改函数内部结构，但是每次调用函数时都执行另外的操作：

```python
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
# 利用python的@功能
@log
def now():
    print('2015-3-25')
# 显示
>>> now()
call now():
2015-3-25

```

解释：  作为装饰器，log()函数返回一个函数，原来的now()函数仍旧存在，但是同名的now现在是指向了一个*新的函数*，调用now()实际上是调用了新的函数，就是在log()中返回的wrapper()函数。 -> wrapper()函数做两件事，第一是print，第二是调用原始函数，即原来的now()函数。  

下面看一个多层嵌套的例子：  

```python
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
# 用法如下
@log('execute')
def now():
    print('2015-3-25')
# 三层嵌套的效果如下
>>> now = log('execute')(now)
```
解析：  
首先执行log('execute'), 参数是'execute', 调用返回的decorator函数, 所以执行decorator函数， 参数是now函数， 调用返回的wrapper函数， 所以这句语句最终的返回值是wrapper函数。  

但是，这里出现了一个问题，返回的是wrapper函数，那么这个函数的名字叫什么呢？叫wrapper！ 所以打印now.__name__，会出现wrapper。  
为了解决以上问题，python内置了functools.warps，把函数名字传递过去。代码如下：  

```python
import functools

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
```
  
对于廖老师教程里的思考题，参考楼下答案：  
同时支持log/log('execute')的装饰器应该使用isinstance()函数进行比较。  
代码如下：

```python
import functools
# 根据Object的情况查看是否是str或者函数调用
def log(Object):
  if isinstance(Object, str):
    def decorator(func):
    	# 函数名称传递 ?? 不太懂为什么一定要加
      @functools.wraps(func)
      def wrapper(*args, **kw):
        print('%s %s():' % (Object, func.__name__))
        return func(*args, **kw)
      return wrapper
    return decorator
    # 如果log后面不是字符也不是函数怎么办？
  elif hasattr(Object,'__call__'): # 判断Object是否为函数
    @functools.wraps(Object)
    def wrapper(*args, **kw):
      print('call %s():' % Object.__name__)
      return Object(*args, **kw)
    return wrapper
  else:
    pass  # 如果Object不是字符串也不是函数
          # 则进一步进行处理


@log
def now():
  print('2017-04-13')

print('The name of function is %s' % now.__name__)
now()

print()

@log('execute')
def now():
  print('2017-04-13')

print('The name of function is %s' % now.__name__)
now()
```
## 偏函数  
有一点函数重载的感觉。  
```python
>>> import functools
>>> int2 = functools.partial(int, base=2) # 这里的int是指int()函数，把字符串转换为int类型，base=2 是指转换成二进制。
>>> int2('1000000')
64
>>> int2('1010101')
85

当然，这个int2也接受其他base，如：
>>> int2('1000000', base=10)
1000000
```

创建偏函数时，实际上可以接收函数对象、\*args和\*\*kw这3个参数。  
理解：
参考```int2 = functools.partial(int, base=2)```这一语句，函数对象是int，传递了一个参数base=2，所以对于函数int来说，他现在的状态是这样的：  
int('待int2调用输入', \*\*kw), 而\*\*kw在这里传入了: kw = {'base':2 }这样的tuple.  
调用int2('12345')的时候，实际调用如下：  
int('12345', \*\*kw)  

又，参考偏函数```partial_max = functools.partial(max, 0)```  
调用```partial_max(2,3,4)```  
相当于调用max(0, 2, 3, 4)，会把0当作\*args加到调用参数的左边。  
实际上是```args = (0, 2, 3, 4)```，调用了max(\*args)

## 模块module
函数作用域在python中的概念：  
形如```__xxx__```这样的是特殊变量，xxx比如说name, authour, main等。  
形如```_xxx```或者```__xxx_```这样的是private变量。和Java, C++不同，Python并没有一种方法可以完全限制访问private函数或变量，但是，从编程习惯上不应该引用private函数或变量。  

###安装第三方模块  
pip3 install 模块名  

###使用第三方模块  
import 模块名  

Python会在指定的路径下搜索对应的.py文件。 默认情况下，指定路径是指当前目录、所有已安装的内置模块和第三方模块。 搜索路径在```path```变量里面，可以通过sys.path查看。  
当然，也可以添加sys.path，使用方法sys.path.append()  
但是运行完成以后，这个变量就失效了。  
另外，可以设置环境变量```PYTHOPATH```

## OOP in python  
class Student(Object)  
其中，类名一般首字母大写，后面括号内是继承，如果没有继承就用Object  
Constructor命名如下：  

```python
Class Student(Object):
	def __init__(self, name, score):
		self.name = name
		self.score = score
```
构造方法第一个参数永远是self，内部把各个属性绑定到self。有__init__方法后，创建实例需要传入与方法匹配的参数，不用传self。  
内部方法的第一个参数也是self。  
和静态语言不同，Python允许对实例变量绑定任何数据，也就是说，对于两个实例变量，虽然它们都是同一个类的不同实例，但拥有的变量名称都可能不同：  

```python
>>> bart = Student('Bart Simpson', 59)
>>> lisa = Student('Lisa Simpson', 87)
>>> bart.age = 8
>>> bart.age
8
>>> lisa.age
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute 'age'

```  

特殊变量：双下划线开头，双下划线结尾。可以直接访问。  
Private变量：用双下划线开头的变量，不能外部访问。  

### 继承和多态  
已知class Animal，衍生：  

```python
class Dog(Animal):
    pass

class Cat(Animal):
    pass
# 自动拥有父类方法
```
多态不用说，和java差不多。  

注意静态语言和动态语言的区别。  
对于Python这样的动态语言来说，则不一定需要传入Animal类型。我们只需要保证传入的对象有一个run()方法就可以了：  

```python
class Timer(object):
    def run(self):
        print('Start...')
```

## 判断类型
type()函数  
isinstance()函数，注意可以判断是否是某种类型中的一种  

```python
>>> isinstance([1, 2, 3], (list, tuple))
True
>>> isinstance((1, 2, 3), (list, tuple))
True
```

获得对象的所有属性和方法：  
dir()函数。如：  
```python
>>> dir('ABC')
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
```
如上面所说，__xx__是特殊属性/方法，所以调用len(a)，等同于a.__len__      
而没有__xx__的是普通方法。  
对于是否有属性，可以用hasattr()来得到，如果没有，可以setattr(), 还可以getattr()  
可以传入一个default参数，如果属性不存在，就返回默认值：  
```python
>>> getattr(obj, 'z', 404) # 获取属性'z'，如果不存在，返回默认值404
404
```
有一个例子，对类型进行检查：  
```python
def readImage(fp):
    if hasattr(fp, 'read'):
        return readData(fp)
    return None
```   
当然，有read()方法，不代表改fp就是一个文件流，可能是网络流、字节流等，不过只要返回的是有效的图像数据，就不影响这个代码的功能。（python的动态语言特性）  

## 使用__slots__  
尝试给实例绑定一个属性：  
```python
>>> s = Student()
>>> s.name = 'Michael' # 动态给实例绑定一个属性
>>> print(s.name)
Michael
```  
Student原本没有name属性，s也没有，动态绑上了name属性。  
给实例绑定一个方法：  
```python
>>> def set_age(self, age): # 定义一个函数作为实例方法
...     self.age = age
...
>>> from types import MethodType
>>> s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
>>> s.set_age(25) # 调用实例方法
>>> s.age # 测试结果
25
```  
这个方法本来不是类内部的，但是可以绑定给实例，通过此方法，该实例获得了一个age属性。但是这个方法对该类的其它实例是不适用的。  
如果要对所有实例都绑定，就对类绑定方法：  
```python
>>> def set_score(self, score):
...     self.score = score
...
>>> Student.set_score = set_score
# 所有的实例都可以用此方法
>>> s.set_score(99)
>>> s.score
99
```  
当然，这只是体现了动态语言的功能。  

### slots  
如果动态语言可以随时增加实例属性的话，那岂不是乱套了，所以为了限定实例的属性，我们可以添加一个特殊的```__slots__```变量。  
```python
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
# give a try
>>> s = Student() # 创建新的实例
>>> s.name = 'Michael' # 绑定属性'name'
>>> s.age = 25 # 绑定属性'age'
>>> s.score = 99 # 绑定属性'score'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute 'score'
```  
使用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的。如果在子类中加上__slots__，那么子类实例允许定义的属性也会从父类继承。  

但是，没有办法限制通过添加方法来添加属性。  
如：
```python
from types import MethodType
def set_score(self, score):
	sellf.score = score

class Student(Object):
	__slots__ = ('name', 'age', 'set_score')
	pass

Student.set_score = MethodType(set_score, Student) # 绑定方法到类  

s = Student()
s.set_score(99)
s.score

>>>99

```
当然，这里的前提是，我们有限制出这个方法，如果```__slots__ = ('name', 'age')```那就限制住了，不过这样Student类也没有别的方法了。  

另外，对于类属性和实例属性，要分清楚情况。如以下代码：  
```python
def set_age(self,age):
    self.age=age

class Stu(object):
    pass

s=Stu()
a=Stu()

from types import MethodType
# 这里添加的是针对类的方法，所以修改的应该是类的属性
Stu.set_age=MethodType(set_age,Stu)

a.set_age(15) \\通过set_age方法，设置的类属性age的值
s.set_age(11) \\也是设置类属性age的值，并把上个值覆盖掉
print(s.age,a.age) \\由于a和s自身没有age属性，所以打印的是类属性age的值

a.age = 10  \\给实例a添加一个属性age并赋值为10
s.age = 20  \\给实例b添加一个属性age并赋值为20
\\这两个分别是实例a和s自身的属性，仅仅是与类属性age同名，并没有任何关系

print(s.age,a.age)  \\打印的是a和s自身的age属性值，不是类age属性值	
```
```__slots__```的实质是限制```__dict__```的加入  
如上一段代码，查看s.__dict__，是空的，当加入s.age = 20之后，s.__dict__变成了 {'age': 20}  
对__slots__的约束，如Stu的约束为age, name, 那么就无法再在dict里面添加score这样的组队。注意，如果类的成员变量与slots中的变量同名，目前的实现是该变量被设置为readonly。  

## @property  
关于property，个人感觉就是一个可以直接通过赋值号来完成赋值操作，而不需要调用方法的方法。在教程中，提到可以做类型检查。个人没有看出来有什么很大的区别，可能还需要继续实践理解吧。  
基本用法就是这样：  
```python
class Screen(object):
	@property
	def width(self):
		return self.width
	@width.setter
	def width(self, width):
		self.width = width
	
	@property
	def height(self):
		return self.height
	@height.setter
	def height(self, height):
		self.height = height
	# 只读属性resolution
	@property
	def resolution(self):
		return self.resolution
# test:
s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)
assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution
```  

## 多重继承  
和c++类似的思想。使用方法就是：
```python
class Hello(object, saying):
```  
这种额外混合的设计模式叫做MixIn。  
为了更好地看出继承关系，我们把Runnable和Flyable改为RunnableMixIn和FlyableMixIn。类似的，你还可以定义出肉食动物CarnivorousMixIn和植食动物HerbivoresMixIn，让某个动物同时拥有好几个MixIn：  
```python
class Dog(Mammal, RunnableMixIn, CarnivorousMixIn):
    pass
```
下面评论有一个扎心的解释：  
第一个继承是生父，后边的都是继父，所以，父类有重复地方法，首先继承生父的。  

## 定制类、定制方法
删除-呃，感觉就是为了让系统回复更好看一点？-  
太他妈可怕了这一章！
从python的内部实现上来说，个人猜测，当我们需要显示类名等信息时，python会解释为调用一些特殊函数。如网站上对于__str__的改写：  
```python
>>> class Student(object):
...     def __init__(self, name):
...         self.name = name
...     def __str__(self):
...         return 'Student object (name: %s)' % self.name
...
>>> print(Student('Michael'))
Student object (name: Michael)
# 否则会出现
# <__main__.Student object at 0x109afb190>
# 但是如果直接打
# >>> s = Student('Michael')
# >>> s
# <__main__.Student object at 0x109afb310>
# 所以还要改写一下__repr__()函数，为了省力我们会这样：  
__repr__ = __str__
```
还有一些奇妙的用法，如iter迭代：  
以Fib为例。  
```python
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值
>>> for n in Fib():
...     print(n)
...
1
1
2
3
5
...
46368
75025        
```  
就很完美！ 
不过这样，没办法取元素！所以继续改。  
```python
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
        
>>> f = Fib()
>>> f[0]
1
>>> f[1]
1
>>> f[2]
2
>>> f[3]
3
>>> f[10]
89
>>> f[100]
573147844013817084101
```
然后继续改进，能够接受切片：
```python
class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
```  
反正可以大改特改，加上step也可以。  

### 利用__getattr__增进完全动态调用体验
诚然，我们可以通过添加类属性来避免调用不存在属性时候的错误。在python的检查中，针对已经有的属性调用，python会直接调用。如果没有的话，则会调用__getattr__函数来对类内部的属性进行检查，是否出现，怎样报错。那么只要我们重写这个函数，就可以对不存在的类型/容易调用错误的类型进行提醒了。  
代码如下：
```python
class Student(object):
	def __init__(self):
		self.name = 'stu'
	def __getattr__(self, attr):
		if attr == 'nmae'
			print ('Do you mean name?')
			return
# 同样，也可以返回函数
		if attr == 'age'
			return lambda 18
# 默认返回值为none
# 调用
>>> s = Student()
>>> s.age()
18
>>> s.nmae
'Do you mean name?'

```  
如果我们经常要对类进行修改，这里有一个链式调用的例子：  
```python
class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__
# try
>>> Chain().status.user.timeline.list
'/status/user/timeline/list'
```

### __call__函数
完成实例本身的调用。  
参考代码：  
```python
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)
# try
>>> s = Student('Michael')
>>> s() # self参数不要传入
My name is Michael.

```
可以通过callable()函数判断一个对象是不是可调用的对象。  
比如callable('abc') == False
callable(Student()) == True

这样，无论API怎么变，SDK都可以根据URL实现完全动态的调用，而且，不随API的增加而改变！  

那么如果API中间带有参数怎么办呢？  
如：  
Chain().users('michael').repos  
那么代码应该这样实现：  
```python
class Chain(object):
	def __init__(self, path = 'GET'):
		self._path = path
	def __getattr__(self, path):
		return Chain('%s/%s' % (self._path, path))
	def __call__(self, path):
		return Chain('%s/%s' % (self._path, path))
	def __str__(self):
		retrun self._path
	__restr__ = __str__
	
```
我们来看一段典型的调用：  
Chain().user('Michael').group('student').repos  
执行流程如下，首先执行Chain()，进入__init__函数，假设创建了实例A，默认path为GET。结束。  
然后我们接收了一个attr叫做.user，这是个方法。由于没有在类内定义有这个方法，我们就调用__getattr__函数，这时候传入的对象是A, path = user, A的类内属性_path为'GET'。然后这个方法返回了一个新的类实例创建，于是我们进入第二次__init__，假设通过这次__init__创建的实例为B，传入的path是GET/user，那么B._path = GET/user.  
于是我们继续往下看，下一步，解释器看到了一个调用参数Michael，怎么调用呢？于是解释器选择让python进入该类的__call__函数。此时传入的参数是B，path = Michael， __call__函数也同样的，进行了一个新的类实例创建，我们假设通过这一次创建的实例叫做C，C获得的path就叫：GET/user/Michael。以此类推，直到打印出最后的结果。  

## 枚举类  
没啥好说的，看代码吧。  
```python
from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)
    
# Print
Jan => Month.Jan , 1
Feb => Month.Feb , 2
March => Month.March , 3
Apr => Month.Apr , 4
May => Month.May , 5
Jun => Month.Jun , 6
July => Month.July , 7
Aug => Month.Aug , 8
Sept => Month.Sept , 9
Oct => Month.Oct , 10
Nov => Month.Nov , 11
Dec => Month.Dec , 12

```

自定义，通过继承的方法。  
```python
from enum import Enum, unique

@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
# running
>>> day1 = Weekday.Mon
>>> print(day1)
Weekday.Mon
>>> print(Weekday.Tue)
Weekday.Tue
>>> print(Weekday['Tue'])
Weekday.Tue
>>> print(Weekday.Tue.value)
2
>>> print(day1 == Weekday.Mon)
True
>>> print(day1 == Weekday.Tue)
False
>>> print(Weekday(1))
Weekday.Mon
>>> print(day1 == Weekday(1))
True
>>> Weekday(7)
Traceback (most recent call last):
  ...
ValueError: 7 is not a valid Weekday
>>> for name, member in Weekday.__members__.items():
...     print(name, '=>', member)
...
Sun => Weekday.Sun
Mon => Weekday.Mon
Tue => Weekday.Tue
Wed => Weekday.Wed
Thu => Weekday.Thu
Fri => Weekday.Fri
Sat => Weekday.Sat
```
## 元类  
type()函数可以返回一个对象的类型。
也可以使用type()函数创建新的类型。  
```python
>>> def fn(self, name='world'): # 先定义函数
...     print('Hello, %s.' % name)
...
# type(classname, 继承父类集合, )
>>> Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
>>> h = Hello()
>>> h.hello()
Hello, world.
>>> print(type(Hello))
<class 'type'>
>>> print(type(h))
<class '__main__.Hello'>
```  


