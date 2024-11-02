import random
import typing
import uuid
from datetime import date, datetime, time
from enum import Enum
from string import ascii_letters
from typing import Any, Dict, Type, Union, get_args, get_origin
from uuid import UUID

from pydantic import BaseModel, ConstrainedInt, NonNegativeInt, PositiveInt
from pydantic.fields import FieldInfo

MAX_NUMBER = 1_000_000
MIN_NUMBER = -1_000_000
STRING_MAX_LENGTH = 25
LIST_MAX_LENGTH = 15
DICT_MAX_LENGTH = 15


class ModelObjectGenerator:
    simple_types = (str, float, int, bool, list, dict, UUID, datetime.date, datetime, date, time)
    container_types = (list, dict)
    pre_defined: Dict = None

    # TODO Add data generation that considers pydantic validators
    def generate(self, model: Type[BaseModel], **pre_defined) -> BaseModel:
        data = {}
        if self.pre_defined is None:
            self.pre_defined = pre_defined
        for name, type_ in typing.get_type_hints(model).items():
            if self.pre_defined.get(name, "pre_defined_is_absent") == "pre_defined_is_absent":
                data[name] = self.generate_field_value(type_=type_, field_info=model.__fields__[name].field_info)
            else:
                data[name] = self.pre_defined.pop(name)
        return model(**data)

    def generate_field_value(self, type_: Type, field_info: FieldInfo, child: Type = None) -> Any:
        if isinstance(type_, typing._GenericAlias):
            # List[str] -> list + str, Optional[int] -> Union[int, None] -> Union + int or None
            return self.generate_field_value(get_origin(type_), field_info, random.choice(get_args(type_)))
        elif isinstance(type_, typing._SpecialForm):
            # Union + int or None -> int or None
            return self.generate_field_value(child, field_info)
        elif type_ in self.simple_types:
            return self.generate_simple_value(type_, field_info, child)
        elif issubclass(type_, BaseModel):
            return self.generate(type_)
        elif issubclass(type_, Enum):
            return random.choice(list(type_))
        elif issubclass(type_, ConstrainedInt):
            return self.generate_pydantic_int(type_)
        elif type_ == type(None):  # noqa E721
            return None
        else:
            raise Exception(type_)

    def generate_simple_value(
        self,
        type_: Type,
        field_info: FieldInfo,
        child: Type = None,
    ) -> Union[str, float, int, bool, list, dict]:
        if type_ == str:
            return "".join(random.choice(ascii_letters) for _ in range(random.randint(1, STRING_MAX_LENGTH)))
        elif type_ in (int, float):
            return self.generate_numeric(type_, field_info)
        elif type_ == bool:
            return random.getrandbits(1)
        elif type_ == list:
            return [
                self.generate_field_value(child or random.choice(self.simple_types), field_info)
                for _ in range(random.randint(1, LIST_MAX_LENGTH))
            ]
        elif type_ == dict:
            return {
                self.generate_simple_value(str, field_info): self.generate_field_value(
                    child or random.choice(tuple(set(self.simple_types) - set(self.container_types))), field_info
                )
                for _ in range(random.randint(1, DICT_MAX_LENGTH))
            }
        elif type_ == UUID:
            return uuid.uuid4()
        elif type_ in (datetime.date, date):
            return datetime.now().date()
        elif type_ in (datetime, datetime.now, time):
            return datetime.now()
        else:
            raise Exception(type_.__name__)

    def generate_numeric(self, type_: Type[Union[int, float]], field_info: FieldInfo) -> Union[int, float]:
        def get_step_value():
            return 1 if type_ == int else 0.001

        min = MIN_NUMBER
        max = MAX_NUMBER

        if field_info.lt is not None:
            max = field_info.lt - get_step_value()
        elif field_info.le is not None:
            max = field_info.le

        if field_info.gt is not None:
            min = field_info.gt + get_step_value()
        elif field_info.ge is not None:
            min = field_info.ge

        return round(random.uniform(min, max), 3) if type_ == float else random.randint(min, max)

    def generate_pydantic_int(self, type_: Type) -> int:
        if type_ == PositiveInt:
            return random.randint(1, MAX_NUMBER)
        elif type_ == NonNegativeInt:
            return random.randint(0, MAX_NUMBER)
