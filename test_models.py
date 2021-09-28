# run these tests like: python -m unittest test_models.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Plant, Garden

os.environ['DATABASE_URL'] = "postgresql:///garden-test"


from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create two test users"""
        db.drop_all()
        db.create_all()

        u1 = User.signup("testing1", "test1@test.com", "password1", None, "location1")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("testing2", "test2@test.com", "password2", None, "location2")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        user = User(
            username='test',
            password='password',
            email='test@test.com',
            location='test',
            image_url= None,
        )

        db.session.add(user)
        db.session.commit()

        # User should have no plants, no gardens, no follows
        self.assertEqual(len(user.plants), 0)
        self.assertEqual(len(user.gardens), 0)
        self.assertEqual(len(user.followed_users), 0)

#sign up tests

    def test_signup(self):
        """test new user signup"""

        u_test = User.signup("test", "test@test.com", "password", None, "location")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "test")
        self.assertEqual(u_test.email, "test@test.com")
        self.assertEqual(u_test.location, "location")
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt always starts with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com", "password", None, "location")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("test", None, "password", None, "location")
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("test", "test@email.com", '', None, "location",)
        
        with self.assertRaises(ValueError) as context:
            User.signup("test", "test@email.com", None, None, "location",)

#authentication test
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password1")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
        self.assertTrue(u)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password1"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))


    def test_add_garden(self):
        """Tests if user adding a garden works"""
        g = Garden(
            user_id=self.uid1,
            username='testing1',
            name='test',
            description='test',
            plants=[],
        )

        db.session.add_all([g])
        db.session.commit()

        l = Garden.query.filter(Garden.user_id == self.uid1).all()
        l2 = Garden.query.filter(Garden.user_id == self.uid2).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(len(l2), 0)

    
    # following tests

    def test_user_follows(self):
        self.u1.followed_users.append(self.u2)
        db.session.commit()

        

    def test_is_following(self):
        self.u1.followed_users.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))



        