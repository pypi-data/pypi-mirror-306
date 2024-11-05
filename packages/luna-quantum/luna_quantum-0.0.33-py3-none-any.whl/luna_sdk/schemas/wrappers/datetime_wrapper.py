from datetime import datetime
from typing import Union

from dateutil.parser import parse
from pydantic import BeforeValidator
from typing_extensions import Annotated


def validate_datetime(date_string: Union[str, datetime]) -> datetime:
    """Validate an ISO date string and return the resulting datetime in the local timezone.

    Parameters
    ----------
    date_string : str
        The ISO date string

    Returns
    -------
    datetime
        The datetime in the user's local timezone

    Raises
    ------
    ValueError
        If `date_string` does not have a valid format.
    """
    dt = date_string if isinstance(date_string, datetime) else parse(date_string)
    return dt.astimezone()


PydanticDatetimeWrapper = Annotated[datetime, BeforeValidator(validate_datetime)]
