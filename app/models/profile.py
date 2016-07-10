import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Profile(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    email = columns.Text(index=True)
    username = columns.Text(index=True)
    password = columns.Text(required=True)
    created_at = columns.DateTime(default=datetime.datetime.now)
    updated_at = columns.DateTime(default=datetime.datetime.now)

    def __repr__(self):
        return '%s %s %d' % (self.email, self.username, self.createdAt)
