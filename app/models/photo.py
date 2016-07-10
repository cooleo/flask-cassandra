
import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Photo(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    title = columns.Text(required=True)
    description = columns.Text(required=True)
    bucket = columns.Text(required=True)
    filename = columns.Text(required=True)
    embed = columns.Text()
    source_id = columns.Text()
    duration = columns.Text()
    url = columns.Text()
    length = columns.Text()
    thumb = columns.Text()
    type = columns.Integer
    width = columns.Integer
    height = columns.Integer
    from_source = columns.Text(index=True)
    logo_source = columns.Text(index=True)
    name_source = columns.Text(index=True)
    url_source = columns.Text(index=True)
    path = columns.Text(nullable=True)
    version = columns.Text(index=True)
    ext = columns.Text(required=False)
    created_at = columns.DateTime(default=datetime.datetime.now)
    updated_at = columns.DateTime(default=datetime.datetime.now)

    def __repr__(self):
        return '%s %s %d' % (self.title, self.description, self.slug)
