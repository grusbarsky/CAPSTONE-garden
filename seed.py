"""Seed file to drop and create all db"""

from models import db, Follows, User, Plant, Garden, User_plant, Garden_plant, Saved_gardens
from app import app

db.drop_all()
db.create_all()