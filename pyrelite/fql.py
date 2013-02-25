"""
>>> u = Table('user')
>>> name = u.column('name')
>>> uid = u.column('uid')
>>> u.select(name).where(uid == Me()).to_sql()
'select name from user where uid = me()'

>>> pic_square = u.column('pic_square')
>>> f = Table('friend')
>>> uid1 = f.column('uid1')
>>> uid2 = f.column('uid2')
>>> u.select(uid, name, pic_square).where((uid == Me()) | (uid.in_(f.select(uid2).where(uid1 == Me())))).to_sql()
'select uid, name, pic_square from user where (uid = me()) or (uid in (select uid2 from friend where uid1 = me()))'
"""

from .compiler import SimpleCompiler
from .core import *
from .node import *


class Me(Literal):
    def __init__(self):
        self.value = 'me()'


class Compiler(SimpleCompiler):
    pass


class Table(SimpleTable):
    def to_sql(self):
        compiler = Compiler()
        return compiler.compile(self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
