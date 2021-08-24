from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Follows(db.Model):
    """a join table for a users garden and all the plants the garden has"""

    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    user_followed = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_following = db.Column(db.Integer, db.ForeignKey("users.id"))

class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    location = db.Column(db.String, nullable=False)
    image_url = db.Column(db.Text, default="/static/7100-1_1.jpg")

    gardens = db.relationship('Garden', secondary='saved_gardens', backref='users')
    plants = db.relationship('Plant', secondary='user_plants', backref='users')
    followed_users = db.relationship('User', secondary='follows' ,
                                        primaryjoin=Follows.user_followed == id, 
                                        secondaryjoin=Follows.user_following == id)
    
    def is_saved(self, plant_id):
        """does this user have this plant saved?"""

        found_plant_list = [plant for plant in self.plants if plant.id == plant_id]
        return len(found_plant_list) == 1
    
    def is_saved_garden(self, garden_id):
        """does this user have this plant saved?"""

        found_garden_list = [garden for garden in self.gardens if garden.id == garden_id]
        return len(found_garden_list) == 1

    def is_following(self, user_id):
        """does this user follow this user?"""

        followed_user = [user for user in self.followed_users if user == user_id]
        return len(followed_user) == 1


    @classmethod
    def signup(cls, username, email, password, image_url, location):
        """Hashes password and saves user"""

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            image_url=image_url,
            location= location,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`. call on class not individual"""

        user = cls.query.filter_by(username=username).first()

        if user:
            user_exist = bcrypt.check_password_hash(user.password, password)
            if user_exist:
                return user
        return False

class Plant(db.Model):
    """Plant"""

    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    binomial_name = db.Column(db.Text, nullable=True, unique=False)
    image = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    sun_requirements = db.Column(db.Text, nullable=True)
    growing_method = db.Column(db.Text, nullable=True)

class Garden(db.Model):
    """Garden"""

    __tablename__ = 'gardens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    username = db.Column(db.Text, db.ForeignKey("users.username"))
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    plants = db.relationship('Plant', secondary='garden_plants', backref='gardens')


class User_plant(db.Model):
    """join table for a user and all of their plants"""

    __tablename__ = 'user_plants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id", ondelete="cascade"))

class Garden_plant(db.Model):
    """a join table for a users garden and all the plants the garden has"""

    __tablename__ = 'garden_plants'

    id = db.Column(db.Integer, primary_key=True)
    garden_id = db.Column(db.Integer, db.ForeignKey("gardens.id", ondelete="cascade"))
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.id", ondelete="cascade"))

class Saved_gardens(db.Model):
    """a join table for a user and gardens they saved belonging to other users"""

    __tablename__ = 'saved_gardens'

    id = db.Column(db.Integer, primary_key=True)
    garden_id = db.Column(db.Integer, db.ForeignKey("gardens.id", ondelete="cascade"))
    user_saved = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)