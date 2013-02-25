from .core import *
from .node import *


class SimpleCompiler(object):
    operators = {
        EqualsOp: '=',
        NotEqualsOp: '!=',
        GreaterThanOp: '>',
        GreaterThanOrEqualsOp: '>=',
        LessThanOp: '<',
        LessThanOrEqualsOp: '<=',
        OrOp: 'or',
        AndOp: 'and',
    }

    def __init__(self):
        self.nodes = {
            Projection: self.compile_projection,
            Selection: self.compile_selection,
            Ordering: self.compile_ordering,
            Limitation: self.compile_limitation,
            SimpleTable: self.compile_expr
        }

    def quote_field(self, field):
        return field.name

    def compile_field(self, field):
        return self.quote_field(field)

    def compile_binary_op(self, op, depth=0):
        if isinstance(op, InOp):
            return "{} in ({})".format(
                self.compile_expr(op.left, depth + 1),
                ', '.join([self.compile_expr(t, depth + 1) for t in op.right])
            )

        return "{} {} {}".format(
            self.compile_expr(op.left, depth + 1),
            self.operators.get(op.__class__),
            self.compile_expr(op.right, depth + 1)
        )

    def compile_associative_op(self, expr, depth=0):
        token = self.operators.get(expr.__class__)
        terms = [self.compile_expr(t, depth + 1) for t in expr.terms]
        fmt = ' {} '.format(token).join(terms)
        return fmt

    def compile_op(self, expr, depth=0):
        if isinstance(expr, BinaryOp):
            fragment = self.compile_binary_op(expr, depth)
        elif isinstance(expr, AssociativeOp):
            fragment = self.compile_associative_op(expr, depth)
        else:
            raise ValueError(expr)

        if depth > 0:
            return "(" + fragment + ")"
        else:
            return fragment

    def compile_expr(self, expr, depth=0):
        if isinstance(expr, basestring):
            return self.compile_string(expr)
        elif isinstance(expr, (int, float)):
            return self.compile_number(expr)
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Field):
            return self.compile_field(expr)
        elif isinstance(expr, Op):
            return self.compile_op(expr, depth)
        elif isinstance(expr, SimpleTable):
            return self.compile_table(expr)
        else:
            raise ValueError(expr)

    def quote_string(self, expr):
        return expr

    def compile_string(self, expr):
        return '"' + self.quote_string(expr) + '"'

    def compile_number(self, expr):
        return str(expr)

    def compile_projection(self, projection):
        return "select {} from {}".format(
            ', '.join(map(self.compile, projection.fields)),
            self.compile(projection.rel))

    def compile_selection(self, selection):
        return "{} where {}".format(self.compile(selection.rel),
            self.compile(selection.expr))

    def compile_ordering(self, ordering):
        fragment = "{} order by {}".format(self.compile(ordering.rel),
            self.compile(ordering.field))
        if ordering.desc:
            fragment += " desc"
        return fragment

    def compile_limitation(self, limitation):
        if limitation.skip:
            fragment = "{}, {}".format(
                self.compile(limitation.skip),
                self.compile(limitation.amount))
        else:
            fragment = self.compile(limitation.amount)
        return "{} limit {}".format(self.compile(limitation.rel), fragment)

    def compile_table(self, table):
        if table.relation:
            return self.compile(table.relation)
        else:
            return self.compile(table.name)

    def compile(self, node):
        for rel_type, compile_func in self.nodes.iteritems():
            if isinstance(node, rel_type):
                return compile_func(node)
        return self.compile_expr(node)
