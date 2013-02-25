from .node import Field, Node

__all__ = ['Relation', 'SimpleTable',
    'Projection', 'Selection', 'Ordering', 'Limitation',
    'project', 'select', 'order', 'limit']


class Relation(object):
    pass


class Projection(Relation):
    def __init__(self, rel, fields):
        self.rel = rel
        self.fields = fields


class Selection(Relation):
    def __init__(self, rel, expr):
        self.rel = rel
        self.expr = expr


class Ordering(Relation):
    def __init__(self, rel, field, desc):
        self.rel = rel
        self.field = field
        self.desc = desc


class Limitation(Relation):
    def __init__(self, rel, amount, skip):
        self.rel = rel
        self.amount = amount
        self.skip = skip


def project(rel, fields):
    return Projection(rel, fields)


def select(rel, expr):
    return Selection(rel, expr)


def order(rel, field, desc=False):
    return Ordering(rel, field, desc)


def limit(rel, amount, skip=0):
    return Limitation(rel, amount, skip)


class SimpleTable(Relation):
    def __init__(self, name, relation=None):
        self.name = self.field_promote(name)
        self.relation = relation

    def field_promote(self, name):
        if isinstance(name, Node):
            return name
        return Field(name)

    def factory(self, name, relation=None):
        return self.__class__(name, relation=relation or self.relation)

    def select(self, *fields):
        projection = project(self.relation or self,
            map(self.field_promote, fields))
        return self.factory(self.name, relation=projection)

    def where(self, expr):
        selection = select(self.relation or self, expr)
        return self.factory(self.name, relation=selection)

    def order_by(self, field, desc=False):
        ordering = order(self.relation or self, field, desc)
        return self.factory(self.name, relation=ordering)

    def limit(self, amount):
        limitation = limit(self.relation or self, amount)
        return self.factory(self.name, relation=limitation)

    def column(self, name):
        return self.field_promote(name)

    def __getitem__(self, name):
        return self.column(name)
