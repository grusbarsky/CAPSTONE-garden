# run tests like: python -m unittest test_routes.py


import os
from unittest import TestCase
from flask import session

from models import db, User, Plant, Garden

os.environ['DATABASE_URL'] = "postgresql:///garden-test"

from app import app

app.config['WTF_CSRF_ENABLED'] = False

class RoutesTestCase(TestCase):
    """integration tests: testing Flask app."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    location='Test',
                                    image_url=None)
        self.testuser_id = 0000
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("test1", "test1@test.com", "password", None, 'Baltimore',)
        self.u1_id = 1111
        self.u1.id = self.u1_id
        self.u2 = User.signup("test2", "test2@test.com", "password", None, 'location',)
        self.u2_id = 2222
        self.u2.id = self.u2_id
        self.u3 = User.signup("test3", "test3@test.com", "password", None, 'location',)
        self.u4 = User.signup("test4", "test4@test.com", "password", None, 'location',)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_homepage(self):
        """tests homepage loads"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Virtual Garden</h1>', html)


# search function tests

    def test_search_bar_users(self):
        with app.test_client() as client:
            resp = client.post('/search',
                           data={'options':'Users', 'global-search': 'Plum'})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users/search/Plum")

    def test_search_bar_plants(self):
        with app.test_client() as client:
            resp = client.post('/search',
                           data={'options':'Plants', 'global-search': 'Plum'})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/plants/search/Plum")
    
    #user routes

    def test_login(self):
        """testing user login"""
        with app.test_client() as client:
            resp = client.post('/login',
                            data={'username': 'test1', 'password': 'password'})
            self.assertEqual(session['current_user'], 1111)
            self.assertEqual(resp.status_code, 302)


    def test_logout(self):
        """testing user logout"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = 1111
            
            resp = client.get('/logout')

            self.assertNotIn('current_user', session)
            self.assertEqual(resp.status_code, 302)
    
    def test_edit_user(self):
        """testing edit user"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = 1111
            
            resp = client.post('/users/profile/edit',
                            data={"username": "newname",
                                "email": "newemail@test.com",
                                "image_url": "newurl",
                                "location": "newlocation",
                                "password": "password"
                            })
            
            user = User.query.filter(User.id==1111).one()

            self.assertEqual(session['current_user'], 1111)
            self.assertEqual(user.username, "newname")
            self.assertEqual(user.email, "newemail@test.com")
            self.assertEqual(user.image_url, "newurl")
            self.assertEqual(user.location, "newlocation")

    def test_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("testuser", str(resp.data))


#follow tests
    def test_add_follow(self):
        """testing add follow"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id

            resp = client.post('/follows/add/2222')

            user = User.query.filter(User.id==1111).one()
            
            self.assertEqual(len(user.followed_users), 1)
            self.assertEqual(user.followed_users[0].id, 2222)

#test unfollow user
    def test_remove_follow(self):
        """testing remove follow"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id

            user = User.query.filter(User.id==1111).one()

            user.followed_users.append(self.u2)


            db.session.add(user)
            db.session.commit()
            
            resp = client.post('/follows/remove/2222')

            self.assertEqual(len(user.followed_users), 0)


# plant tests

    def test_save_plant(self):
        """testing save plant"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id

            plant = Plant(name='Sunflower', id=1234)
            db.session.add(plant)
            db.session.commit()

            user = User.query.filter(User.id==1111).one()

            resp = client.post('/plants/1234/save')

            self.assertEqual(len(user.plants), 1)
            self.assertEqual(user.plants[0].id, 1234)

    def test_delete_plant(self):
        """testing deleting a saved plant"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id

            plant = Plant(name='Sunflower', id=1234)
            db.session.add(plant)

            user = User.query.filter(User.id==1111).one()

            user.plants.append(plant)
            db.session.add(user)
            
            db.session.commit()


            resp = client.post('/plants/1234/delete')

            self.assertEqual(len(user.plants), 0)
    
    # garden tests

    def test_save_inspiration(self):
        """testing save a garden from another user for inspiration"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id

            garden = Garden(user_id=2222, username='test2',name='mygarden', id=1234)
            db.session.add(garden)
            db.session.commit()

            resp = client.get('/gardens/1234/save')

            user = User.query.filter(User.id==1111).one()

            self.assertEqual(len(user.gardens), 1)
            self.assertEqual(user.gardens[0].id, 1234)

    def test_delete_inspiration(self):
        """testing deleting a saved garden from another user"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id

            garden = Garden(user_id=2222, username='test2',name='mygarden', id=1234)
            db.session.add(garden)
            db.session.commit()

            user = User.query.filter(User.id==1111).one()


            resp = client.post('/gardens/1234/delete-save')

            self.assertEqual(len(user.gardens), 0)


    def test_create_garden(self):
        """"testing create a garden"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id
            

            resp = client.post('/gardens', data={
                                "user_id": 1111,
                                "username": "test1",
                                "name": "name",
                                "description": "description"
                            })
            
            
            gardens = Garden.query.filter(Garden.user_id==1111).all()

            self.assertEqual(len(gardens), 1)
            self.assertEqual(gardens[0].name, 'name')



#test delete garden

    def test_delete_garden(self):
        """delete a users garden"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id
            

            garden = Garden(user_id=1111, username='test1',name='mygarden', id=1234)
            db.session.add(garden)
            db.session.commit()

            resp = client.post('/gardens/1234/delete')
            
            
            gardens = Garden.query.filter(Garden.user_id==1111).all()

            self.assertEqual(len(gardens), 0)


    def test_add_plant_to_garden(self):
        "test adding a plant to a garden"

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id
        
        garden = Garden(user_id=1111, username='test1',name='mygarden', id=1234)
        db.session.add(garden)
        
        plant = Plant(name='Sunflower', id=9999)
        db.session.add(plant)

        db.session.commit()

        resp = client.post('/plants/9999/add-plant', data={"garden_id": 1234})

        test_garden = Garden.query.filter(Garden.user_id==1111).one()

        self.assertEqual(len(test_garden.plants), 1)
        self.assertEqual(test_garden[0].id, 1234)
        

#test delete plant

def test_delete_plant_from_garden(self):
        """test deleting a plant from a garden"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id

        plant = Plant(name='Sunflower', id=9999)
        db.session.add(plant)
        
        garden = Garden(user_id=1111, username='test1',name='mygarden', id=1234, plants=plant)
        db.session.add(garden)

        db.session.commit()

        resp = client.post('/plants/9999/1234/delete-plant')

        test_garden = Garden.query.filter(Garden.user_id==1111).one()

        self.assertEqual(len(test_garden.plants), 0)

#weather tests

def test_weather(self):
    """test weather page"""

    with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_user'] = self.u1.id
    
    resp = client.get('/weather')

    html = resp.get_data(as_text=True)

    self.assertEqual(resp.status_code, 200)
    self.assertIn('<h1>Weather for Baltimore, Maryland</h1>', html)
    

        