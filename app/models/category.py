import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Category(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(index=True)
    description = columns.Text(required=True)
    slug = columns.Text(required=False)
    created_at = columns.DateTime(default=datetime.datetime.now)

    def __repr__(self):
        return '%s %s %d' % (self.name, self.description, self.slug)
