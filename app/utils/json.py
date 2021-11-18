import json
from datetime import date, datetime
from enum import Enum
from json import JSONEncoder
from uuid import UUID

from pydantic import BaseModel


class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, set):
            return list(o)
        if isinstance(o, BaseModel):
            return o.dict()
        if isinstance(o, UUID):
            return o.hex
        return JSONEncoder.default(self, o)


def dumps(o: object):
    return json.dumps(o, cls=CustomJsonEncoder)
