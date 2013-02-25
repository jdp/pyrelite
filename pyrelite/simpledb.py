"""
>>> d = Domain('mydomain')
>>> stmt = d.select(Star())
>>> stmt.where(d.column('city') == 'Seattle').to_sql()
'select * from mydomain where city = "Seattle"'

>>> city = d.column('city')
>>> stmt.where((city == 'Seattle') | (city == 'Portland')).to_sql()
'select * from mydomain where (city = "Seattle") or (city = "Portland")'

>>> name = d.column('name')
>>> stmt.where(name != 'John').to_sql()
'select * from mydomain where name != "John"'

>>> stmt.where((name != 'John') & (name != 'Humberto')).to_sql()
'select * from mydomain where (name != "John") and (name != "Humberto")'

>>> weight = d.column('weight')
>>> stmt.where(weight > 34).to_sql()
'select * from mydomain where weight > 34'

>>> stmt.where(weight >= 65).to_sql()
'select * from mydomain where weight >= 65'

>>> stmt.where(weight < 34).to_sql()
'select * from mydomain where weight < 34'

>>> year = d.column('Year')
>>> stmt.where(year <= 2000).to_sql()
'select * from mydomain where Year <= 2000'

>>> author = d.column('Author')
>>> stmt.where(author.like('Henry%')).to_sql()
'select * from mydomain where Author like "Henry%"'

>>> keyword = d.column('Keyword')
>>> stmt.where((keyword == 'Book') & (author.like('%Miller'))).to_sql()
'select * from mydomain where (Keyword = "Book") and (Author like "%Miller")'

>>> stmt.where(~author.like('Henry%')).to_sql()
'select * from mydomain where Author not like "Henry%"'

>>> stmt.where(year.between(1998, 2000)).to_sql()
'select * from mydomain where Year between 1998 and 2000'

>>> stmt.where(year.in_(1998, 2000, 2003)).to_sql()
'select * from mydomain where Year in (1998, 2000, 2003)'

>>> stmt.where(year.is_null()).to_sql()
'select * from mydomain where Year is null'

>>> stmt.where(~year.is_null()).to_sql()
'select * from mydomain where Year is not null'

>>> stmt.where(Every(keyword) == 'Book').to_sql()
'select * from mydomain where every(Keyword) = "Book"'

>>> title = d.column('Title')
>>> stmt.where(title == 'The Right Stuff').to_sql()
'select * from mydomain where Title = "The Right Stuff"'

>>> stmt.where(year > '1985').to_sql()
'select * from mydomain where Year > "1985"'

>>> rating = d.column('Rating')
>>> stmt.where(rating.like('****%')).to_sql()
'select * from mydomain where Rating like "****%"'

>>> pages = d.column('Pages')
>>> stmt.where(pages < '00320').to_sql()
'select * from mydomain where Pages < "00320"'

>>> year = d.column('Year')
>>> stmt.where((year > '1975') & (year < '2008')).to_sql()
'select * from mydomain where (Year > "1975") and (Year < "2008")'

>>> stmt.where(year.between('1975', '2008')).to_sql()
'select * from mydomain where Year between "1975" and "2008"'

>>> stmt.where((rating == '***') | (rating == '*****')).to_sql()
'select * from mydomain where (Rating = "***") or (Rating = "*****")'

>>> stmt.where(((year > '1950') & (year < '1960')) | year.like('193%') | (year == '2007')).to_sql()
'select * from mydomain where ((Year > "1950") and (Year < "1960")) or (Year like "193%") or (Year = "2007")'

>>> stmt.where((rating == '4 stars') | (rating == '****')).to_sql()
'select * from mydomain where (Rating = "4 stars") or (Rating = "****")'

>>> stmt.where((keyword == 'Book') & (keyword == 'Hardcover')).to_sql()
'select * from mydomain where (Keyword = "Book") and (Keyword = "Hardcover")'

>>> stmt.where(Every(keyword).in_('Book', 'Paperback')).to_sql()
'select * from mydomain where every(Keyword) in ("Book", "Paperback")'

>>> stmt.where(rating == '****').to_sql()
'select * from mydomain where Rating = "****"'

>>> stmt.where(Every(rating) == '****').to_sql()
'select * from mydomain where every(Rating) = "****"'

>>> stmt.where(intersection(keyword == 'Book', keyword == 'Hardcover')).to_sql()
'select * from mydomain where (Keyword = "Book") intersection (Keyword = "Hardcover")'

>>> stmt.where(year < '1980').order_by(year).to_sql()
'select * from mydomain where Year < "1980" order by Year'

>>> stmt.where(intersection(year == '2007', ~author.is_null())).order_by(author, desc=True).to_sql()
'select * from mydomain where (Year = "2007") intersection (Author is not null) order by Author desc'

>>> stmt.where(year < '1980').order_by(year).limit(2).to_sql()
'select * from mydomain where Year < "1980" order by Year limit 2'

>>> d = Domain('mydomain')
>>> stmt = d.select(ItemName())
>>> stmt.where(ItemName().like('B000%')).order_by(ItemName()).to_sql()
'select itemName() from mydomain where itemName() like "B000%" order by itemName()'

>>> stmt = d.select(Count())
>>> stmt.where(title == 'The Right Stuff').to_sql()
'select count(*) from mydomain where Title = "The Right Stuff"'

>>> stmt.where(year > '1985').to_sql()
'select count(*) from mydomain where Year > "1985"'

>>> stmt.limit(500).to_sql()
'select count(*) from mydomain limit 500'

>>> stmt = d.select(Star())
>>> stmt.where(d.column('abc`123') == '1').to_sql()
'select * from mydomain where `abc``123` = "1"'

>>> stmt.where(d.column('between') == '1').to_sql()
'select * from mydomain where `between` = "1"'
"""

import re

from .compiler import SimpleCompiler
from .core import *
from .node import *


class Every(Field):
    def __init__(self, field):
        self.field = field


class ItemName(Field, Literal):
    def __init__(self):
        Field.__init__(self, 'itemName()')
        Literal.__init__(self, 'itemName()')


class Star(Literal):
    def __init__(self):
        self.value = '*'


class Count(Field, Literal):
    def __init__(self):
        Field.__init__(self, 'count(*)')
        Literal.__init__(self, 'count(*)')


class BetweenOp(BinaryOp):
    pass


class IntersectionOp(BinaryOp):
    pass


def intersection(lhs, rhs):
    return IntersectionOp(lhs, rhs)


class SimpleDBField(Field):
    def between(self, lower, upper):
        return BetweenOp(self, (lower, upper))


class Compiler(SimpleCompiler):
    reserved_words = [
        'or', 'and', 'not', 'from', 'where', 'select', 'like', 'null', 'is',
        'order', 'by', 'asc', 'desc', 'in', 'between', 'intersection', 'limit',
        'every'
    ]

    def __init__(self):
        super(Compiler, self).__init__()
        operators = [
            (LikeOp, 'like'),
            (NotLikeOp, 'not like'),
            (IsOp, 'is'),
            (IsNotOp, 'is not'),
            (IntersectionOp, 'intersection')
        ]
        for op in operators:
            self.operators[op[0]] = op[1]

    def quote_field(self, field):
        FIELD_RE = re.compile(r'^[a-z0-9_$]+$', re.I)
        if not FIELD_RE.match(field.name) or field.name in self.reserved_words:
            return "`{}`".format(field.name.replace('`', '``'))
        else:
            return super(Compiler, self).quote_field(field)

    def quote_string(self, expr):
        return expr.replace('"', '""')

    def compile_field(self, field):
        if isinstance(field, Every):
            return "every({})".format(self.compile_field(field.field))
        return super(Compiler, self).compile_field(field)

    def compile_binary_op(self, op, depth=0):
        if isinstance(op, BetweenOp):
            return "{} between {} and {}".format(
                self.compile_expr(op.left, depth + 1),
                self.compile_expr(op.right[0], depth + 1),
                self.compile_expr(op.right[1], depth + 1)
            )

        return super(Compiler, self).compile_binary_op(op, depth)


class Domain(SimpleTable):
    def field_promote(self, name):
        if isinstance(name, Node):
            return name
        return SimpleDBField(name)

    def to_sql(self):
        compiler = Compiler()
        return compiler.compile(self)

    def column(self, name):
        return self.field_promote(name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
