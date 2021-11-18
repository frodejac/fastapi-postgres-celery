from dataclasses import dataclass
from typing import Any, cast, Dict, Optional, Type, TypeVar

from pydantic import BaseConfig, ValidationError
from pydantic.class_validators import Validator
from pydantic.fields import FieldInfo, ModelField


@dataclass
class OrderParams:
    """Common parameters for list operations."""

    order_by: str
    order_dir: str
    limit: int
    page: int


ReturnClass = TypeVar("ReturnClass")


def cast_and_validate(
    type_: Type[ReturnClass],
    v: Any,
    model: Optional[ModelField] = None,
    class_validators: Optional[Dict[str, Validator]] = None,
    field_info: Optional[FieldInfo] = None,
    model_config: Type[BaseConfig] = BaseConfig,
) -> ReturnClass:
    """
    Utiltity that allows casting and validating a list of SQLAlchemy models to arbitrary collection types defined
    by typing.

    Example: Convert a list of User(Base) returned from the database layer to List[UserResponse(BaseModel)]
        >>> cast_and_validate(List[UserResponse], user_repository.get_users())

    """
    if model is None:
        model = ModelField(
            name="_",
            type_=type_,
            class_validators=class_validators or {},
            field_info=field_info or FieldInfo(None),
            model_config=model_config,
        )
    ret, err = model.validate(v, {}, loc="return")
    if err:
        raise ValidationError([err], model.type_)
    return cast(ReturnClass, ret)
