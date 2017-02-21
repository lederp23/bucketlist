from app import db
from api.models import BucketList, Item

db.session.create_all()
