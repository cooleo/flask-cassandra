import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqltypes import UserType


class FeedPhoto(UserType):
    photo_id = columns.UUID()
    path = columns.Text()
    url = columns.Text()
    filename = columns.Text()


class Feed(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    category_id = columns.UUID()
    title = columns.Text(required=True)
    description = columns.Text()
    url = columns.Text(required=True)
    content = columns.Text()
    from_source = columns.Text()
    logo_source = columns.Text()
    name_source = columns.Text()
    url_source = columns.Text()
    type = columns.Integer()
    owner = columns.UUID()
    bucket = columns.Text()
    thumb = columns.Text()
    likes = columns.BigInt()
    shares = columns.BigInt()
    pins = columns.BigInt()
    comments = columns.BigInt()
    pins = columns.BigInt()
    views = columns.BigInt()
    popular = columns.BigInt()
    tags = columns.Set(columns.Text())
    status = columns.Integer()
    video = columns.UUID()
    images = columns.Set(FeedPhoto)
    photo = columns.UUID()
    news = columns.UUID()
    created_at = columns.DateTime(default=datetime.datetime.now)
    updated_at = columns.DateTime(default=datetime.datetime.now)

    def __repr__(self):
        return '%s %s %d' % (self.title, self.description, self.url)
