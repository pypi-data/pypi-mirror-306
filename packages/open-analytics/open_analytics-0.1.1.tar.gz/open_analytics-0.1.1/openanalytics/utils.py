from decimal import Decimal
from datetime import date, datetime
from enum import Enum
import numbers
from collections.abc import MutableMapping
import pandas as pd


def require(name, field, data_type):
    """Require that the named `field` has the right `data_type`"""
    if not isinstance(field, data_type):
        msg = "{0} must have {1}, got: {2}".format(name, data_type, field)
        raise AssertionError(msg)


def stringify_id(val):
    if val is None:
        return None
    if isinstance(val, str):
        return val
    return str(val)


def clean(item):
    if isinstance(item, Decimal):
        return float(item)
    elif isinstance(item, (str, bool, numbers.Number, datetime, date, type(None))):
        return item
    elif isinstance(item, (set, list, tuple)):
        return _clean_list(item)
    elif isinstance(item, dict):
        return _clean_dict(item)
    elif isinstance(item, Enum):
        return clean(item.value)
    else:
        return _coerce_unicode(item)


def flatten_dict(d: MutableMapping, sep: str = ".") -> MutableMapping:
    [flat_dict] = pd.json_normalize(d, sep=sep).to_dict(orient="records")
    return flat_dict


# private methods


def _clean_list(list_):
    return [clean(item) for item in list_]


def _clean_dict(dict_):
    data = {}
    for k, v in dict_.items():
        try:
            data[k] = clean(v)
        except TypeError:
            pass
            # log.warning(
            #     "Dictionary values must be serializeable to "
            #     'JSON "%s" value %s of type %s is unsupported.',
            #     k,
            #     v,
            #     type(v),
            # )
    return data


def _coerce_unicode(cmplx):
    try:
        item = cmplx.decode("utf-8", "strict")
    except AttributeError as exception:
        item = ":".join(exception)
        item.decode("utf-8", "strict")
        # log.warning("Error decoding: %s", item)
        return None
    return item
