
# # run these tests like:
# #python -m unittest test_app.py


# import os
# from unittest import TestCase
# from sqlalchemy import exc

# from models import db, User, Message, Follows, Likes

# os.environ['DATABASE_URL'] = "postgresql:///garden-test"


# from app import app

# db.create_all()

# class UserModelTestCase(TestCase):
#     """Test views for messages."""

#     def setUp(self):
#         """Create two test users"""
#         db.drop_all()
#         db.create_all()

#         u1 = User.signup("testing1", "password1", "test1@test.com", "location1" None)
#         uid1 = 1111
#         u1.id = uid1

#         u2 = User.signup("testing2", "password2", "test2@test.com", "location2" None)
#         uid2 = 2222
#         u2.id = uid2

#         db.session.commit()

#         u1 = User.query.get(uid1)
#         u2 = User.query.get(uid2)

#         self.u1 = u1
#         self.uid1 = uid1

#         self.u2 = u2
#         self.uid2 = uid2

#         self.client = app.test_client()


#     def tearDown(self):
#         res = super().tearDown()
#         db.session.rollback()
#         return res

#     def test_user_model(self):
#         """Does basic model work?"""

#         user = User(
#             username='test',
#             password='password',
#             email='test@test.com',
#             location='test'
#             image_url= None,
#         )

#         db.session.add(user)
#         db.session.commit()

#         # User should have no plants, no gardens, no follows
#         self.assertEqual(len(user.plants), 0)
#         self.assertEqual(len(user.gardens), 0)
#         self.assertEqual(len(user.followed_users), 0)

# # test adding a garding

#     def test_add_garden(self):
#         """Tests if liking a message works"""
#         g1 = Garden(
#             user_id = self.uid1
#             username = 'test'
#             name = 'test'
#             description = 'test'
#             plants = None
#         )

#         g2 = Message(
#             user_id = self.uid1
#             username = 'test'
#             name = 'test'
#             description = 'test'
#             plants = None
#         )

#         u = User.signup("testing", "password", "test@test.com", "location" None)
#         uid = 000
#         u.id = uid
#         db.session.add_all([g1, g2, u])
#         db.session.commit()

#         u.gardens.append(g1)

#         db.session.commit()

#         l = Gardens.query.filter(Gardens.user_id == uid).all()
#         self.assertEqual(len(l), 1)
    
#     # following tests

#    def test_user_follows(self):
#         self.u1.followed_users.append(self.u2)
#         db.session.commit()

#         self.assertEqual(len(self.u2.followed_users), 0)
#         self.assertEqual(len(self.u1.followed_users), 1)

#         self.assertEqual(self.u1.followed_users[0].id, self.u2.id)

#     def test_is_following(self):
#         self.u1.following.append(self.u2)
#         db.session.commit()

#         self.assertTrue(self.u1.is_following(self.u2))
#         self.assertFalse(self.u2.is_following(self.u1))
    
#     # sign up tests

#     def test_signup(self):
#         u_test = User.signup("test", "password", "test@test.com", "location" None)
#         uid = 99999
#         u_test.id = uid
#         db.session.commit()

#         u_test = User.query.get(uid)
#         self.assertIsNotNone(u_test)
#         self.assertEqual(u_test.username, "test")
#         self.assertEqual(u_test.email, "test@test.com")
#         self.assertEqual(u_test.location, "location")
#         self.assertNotEqual(u_test.password, "password")
#         # Bcrypt always starts with $2b$
#         self.assertTrue(u_test.password.startswith("$2b$"))


        