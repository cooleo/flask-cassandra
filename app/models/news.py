import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqltypes import UserType


class NewsPhoto(UserType):
    path = columns.Text
    url = columns.Text
    filename = columns.Text
    id = columns.UUID


class News(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    title = columns.Text(required=True)
    description = columns.Text(required=True)
    summary = columns.Text(required=False)
    body = columns.Text()
    bucket = columns.Text()
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
    created_at = columns.DateTime(default=datetime.datetime.now)
    updated_at = columns.DateTime(default=datetime.datetime.now)
    photos = columns.List(NewsPhoto)
    author = columns.UUID


def __repr__(self):
    return '%s %s %d' % (self.name, self.description, self.slug)
