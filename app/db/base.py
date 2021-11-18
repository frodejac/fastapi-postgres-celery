from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    pass


# noinspection PyUnresolvedReferences
from .tables import *
