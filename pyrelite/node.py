class Node(object):
    pass


class Expr(Node):
    def __eq__(self, other):
        return EqualsOp(self, other)

    def __ne__(self, other):
        return NotEqualsOp(self, other)

    def __gt__(self, other):
        return GreaterThanOp(self, other)

    def __ge__(self, other):
        return GreaterThanOrEqualsOp(self, other)

    def __lt__(self, other):
        return LessThanOp(self, other)

    def __le__(self, other):
        return LessThanOrEqualsOp(self, other)

    def __or__(self, other):
        return OrOp(self, other)

    def __and__(self, other):
        return AndOp(self, other)

    def __invert__(self):
        raise NotImplementedError

    def like(self, other):
        return LikeOp(self, other)

    def in_(self, *terms):
        return InOp(self, terms)

    def is_null(self):
        return IsOp(self, Literal('null'))


class Field(Expr):
    def __init__(self, name):
        self.name = name


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Op(Expr):
    pass


class BinaryOp(Op):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class EqualsOp(BinaryOp):
    def __invert__(self):
        return NotEqualsOp(self.left, self.right)


class NotEqualsOp(BinaryOp):
    pass


class GreaterThanOp(BinaryOp):
    pass


class GreaterThanOrEqualsOp(BinaryOp):
    pass


class LessThanOp(BinaryOp):
    pass


class LessThanOrEqualsOp(BinaryOp):
    pass


class LikeOp(BinaryOp):
    def __invert__(self):
        return NotLikeOp(self.left, self.right)


class NotLikeOp(BinaryOp):
    def __invert__(self):
        return LikeOp(self.left, self.right)


class IsOp(BinaryOp):
    def __invert__(self):
        return IsNotOp(self.left, self.right)


class IsNotOp(BinaryOp):
    def __invert__(self):
        return IsOp(self.left, self.right)


class InOp(BinaryOp):
    pass


class AssociativeOp(Op):
    def __init__(self, *terms):
        self.terms = list(terms)


class OrOp(AssociativeOp):
    def __or__(self, other):
        self.terms.append(other)
        return self


class AndOp(AssociativeOp):
    def __and__(self, other):
        self.terms.append(other)
        return self
