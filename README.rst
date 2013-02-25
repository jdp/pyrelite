--------
pyrelite
--------

.. _SimpleDB: http://aws.amazon.com/simpledb/
.. _FQL: http://developers.facebook.com/docs/technical-guides/fql/

A lightweight toolkit for generating SQL strings from simple relational expressions.

Right now only supports `SimpleDB`_ and `FQL`_.

SimpleDB Example
----------------

Here's how to build a simple query for SimpleDB, in a couple different ways::

    >>> from pyrelite import simpledb
    >>> d = simpledb.Domain('mydomain')
    >>> d.select(simpledb.Star()).where(d['city'] == 'Seattle').to_sql()
    'select * from mydomain where city = "Seattle"'

    >>> from pyrelite import project, select
    >>> expr = select(project(d, [simpledb.Star()]), d['city'] == 'Seattle')
    >>> simpledb.Compiler().compile(expr)
    'select * from mydomain where city = "Seattle"'


FQL Example
-----------

Here's how to build a simple FQL query::

    >>> from pyreqlite import fql
    >>> u = fql.Table('user')
    >>> u.select(u['name']).where(u['uid'] == fql.Me()).to_sql()
    'select name from user where uid = me()'

Running Tests
-------------

Run the tests by invoking the ``make`` task::

    $ make test
