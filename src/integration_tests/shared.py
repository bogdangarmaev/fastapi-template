from datetime import date
from functools import partial
from typing import Any, Dict, Type, Callable

from factory import Factory
from factory.base import StubObject


def generate_dict_factory(factory: Type[Factory]) -> Callable:
    """Конструктор класса конвертера Factory в dict"""

    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        d = {}
        for k, v in stub.__dict__.items():
            if isinstance(v, StubObject):
                continue
            if isinstance(v, date):
                d |= {k: v.strftime("%Y-%m-%dT%H:%M:%SZ")}
            else:
                d |= {k: v}
        return d

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)
