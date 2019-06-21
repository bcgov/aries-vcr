"""An object for containing the request pagination information."""

from marshmallow import fields

from ...models.base import BaseModel, BaseModelSchema


class Paginate(BaseModel):
    """Class representing the pagination details of a request."""

    class Meta:
        """Paginate metadata."""

        schema_class = "PaginateSchema"

    def __init__(self, *, limit: int = None, offset: int = None, **kwargs):
        """
        Initialize a Paginate instance.

        Args:
            limit: Limit the number of requested records
            offset: Set the offset of the first requested result

        """
        super(Paginate, self).__init__(**kwargs)
        self.limit = limit
        self.offset = offset


class PaginateSchema(BaseModelSchema):
    """Paginate schema."""

    class Meta:
        """PaginateSchema metadata."""

        model_class = "Paginate"

    limit = fields.Int(required=False)
    offset = fields.Int(required=False)
