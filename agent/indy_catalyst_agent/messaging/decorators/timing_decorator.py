"""
The timing decorator (~timing).

This decorator allows the timing of agent messages to be communicated
and constrained.
"""

from datetime import datetime
from typing import Union

from marshmallow import fields

from ..models.base import BaseModel, BaseModelSchema
from ..util import datetime_to_str

DT_FORMAT = "%Y-%m-%d %H:%M:%S.%fZ"


class TimingDecorator(BaseModel):
    """Class representing the timing decorator."""

    class Meta:
        """TimingDecorator metadata."""

        schema_class = "TimingDecoratorSchema"

    def __init__(
        self,
        *,
        in_time: Union[str, datetime] = None,
        out_time: Union[str, datetime] = None,
        stale_time: Union[str, datetime] = None,
        expires_time: Union[str, datetime] = None,
        delay_milli: int = None,
        wait_until_time: Union[str, datetime] = None,
    ):
        """
        Initialize a TimingDecorator instance.

        Args:
            in_time: The time the message was received
            out_time: The time the message was dispatched
            stale_time: When the message should be considered stale
            expires_time: When the message should be considered expired
            delay_milli: The number of milliseconds to delay processing
            wait_until_time: The earliest time at which to perform processing
        """
        super(TimingDecorator, self).__init__()
        self.in_time = datetime_to_str(in_time)
        self.out_time = datetime_to_str(out_time)
        self.stale_time = datetime_to_str(stale_time)
        self.expires_time = datetime_to_str(expires_time)
        self.delay_milli = delay_milli
        self.wait_until_time = datetime_to_str(wait_until_time)


class TimingDecoratorSchema(BaseModelSchema):
    """Timing decorator schema used in serialization/deserialization."""

    class Meta:
        """TimingDecoratorSchema metadata."""

        model_class = TimingDecorator

    in_time = fields.Str(format=DT_FORMAT, required=False)
    out_time = fields.Str(format=DT_FORMAT, required=False)
    stale_time = fields.Str(format=DT_FORMAT, required=False)
    expires_time = fields.Str(format=DT_FORMAT, required=False)
    delay_milli = fields.Int(required=False)
    wait_until_time = fields.Str(format=DT_FORMAT, required=False)
