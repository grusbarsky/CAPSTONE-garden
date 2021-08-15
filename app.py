from flask import Flask, render_template, request, flash, redirect, session, g, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
import os

from forms import SignupForm, LoginForm, EditUserForm, SearchPlantForm, AddGardenForm, AddPlantToGardenForm
from models import db, bcrypt, connect_db, User, Garden, Plant, Garden_plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(('DATABASE_URL').replace("://", "ql://", 1), 'postgresql:///garden')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# use secret key in production or default to our dev one
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shh')
toolbar = DebugToolbarExtension(app)

connect_db(app)

# global user variable
current_user = "current_user"


# login/logout routes
@app.before_request
def add_user_to_g():
    """If user is logged in, add current user to global variable"""

    if current_user in session:
        g.user = User.query.get(session[current_user])

    else:
        g.user = None


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """User signup"""

    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                location=form.location.data,
                image_url=form.image_url.data or '/static/7100-1_1.jpg',
            )
            db.session.commit()

        except IntegrityError:
            flash("Username or email already taken", 'danger')
            return render_template('users/signup.html', form=form)

        # add current user to session
        session[current_user] = user.id

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            # add current user to session
            session[current_user] = user.id

            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid Login Information", 'danger')

    return render_template('home-login.html', form=form)


@app.route('/logout')
def logout():
    """logout user and remove current_user"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    # delete user from session
    del session[current_user]

    flash("You have been logged out")
    return redirect("/login")

# Homepage
@app.route('/', methods=['GET', 'POST'])
def homepage():
    """homepage:
            if not logged in: home-login.html
            if logged in: home.html
    """
    
    if g.user:
        if 'home-gardens' in request.form:

            gardens = (Garden
                    .query
                    .limit(100)
                    .all())
            return render_template('home.html', gardens=gardens)

        else:
            plants = (Plant
                    .query
                    .limit(100)
                    .all())
        return render_template('home.html', plants=plants)

    else:
        form = LoginForm()
        return render_template('home-login.html', form=form)

@app.route('/search', methods=['POST', 'GET'])
def searchbar():
    """handle searchbar for users, plants"""

    search = request.form.get('global-search')
 
    if request.form.get('options')== 'Users':
        return redirect (f'/users/search/{search}')

    if request.form.get('options')== 'Plants':
        return redirect (f'/plants/search/{search}')

    flash("Search Failed, please try again")
    redirect('/')

# User Routes including: profile, delete user, edit user

@app.route('/users/profile/edit', methods=["GET", "POST"])
def update_user():
    """Update profile for current user"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    user = g.user
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/unknown-image.webp"
            user.location = form.location.data

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Incorrect password, please try again")

    return render_template('users/edit.html', form=form, user_id=user.id)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete current user"""

    if not g.user:
        flash("Unauthorized Access")
        return redirect("/")

    # delete user from session
    del session[current_user]

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """Redirect to any users profile"""
    
    user = User.query.get_or_404(user_id)
    gardens = Garden.query.filter(Garden.user_id == user_id).all()
    
    print("\n\n\n gardens: " + str(gardens) + "\n\n\n")
    print("\n\n\n user: " + str(user) + "\n\n\n")

    return render_template("/users/profile.html", user=user, gardens=gardens)

@app.route('/users/search/<search>')
def search_users(search):
    """Lists users matching search or list all"""

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/list-users.html', users=users)

# Routes for plants

@app.route('/plants')
def users_plants():
    """list a users saved plants"""

    return render_template("plants/saved-plants.html")


@app.route('/plants/search/<search>', methods = ['GET', 'POST'])
def search_plants(search):
    """search for plants"""
   
    plant_results = requests.get(f'https://openfarm.cc/api/v1/crops/?filter=<{search}>').json()

        # if api_results is an empty list, it doesnt exist anywhere
    if len(plant_results['data']) == False:

        plant_results = Plant.query.all()

        return render_template("plants/search-plants.html", plant_results=plant_results)
            
    else:
        return render_template("plants/search-plants.html", plant_results=plant_results)



@app.route('/plants/<plant_name>')
def plant_details(plant_name):
    """show a single plants details"""

    # check if name in local db
    plant = Plant.query.filter(Plant.name == plant_name).first()


    # If it's not, add to local db
    if plant == None:
        plant_result = requests.get(f'https://openfarm.cc/api/v1/crops/?filter=<{plant_name}>').json()
        error_image = "/assets/baren_field_square-4a827e5f09156962937eb100e4484f87e1e788f28a7c9daefe2a9297711a562a.jpg"


        name = plant_result['data'][0]['attributes']['name']
        binomial_name = plant_result['data'][0]['attributes']['binomial_name']
        description = plant_result['data'][0]['attributes']['description']
        growing_method = plant_result['data'][0]['attributes']['sowing_method']

        if plant_result['data'][0]['attributes']['main_image_path'] == error_image:
            image = '/static/unknown-image.webp'
        else:
            image = plant_result['data'][0]['attributes']['main_image_path']


        plant = Plant(name=name, 
                    binomial_name=binomial_name, 
                    description=description, 
                    growing_method=growing_method,
                    image=image)

        db.session.add(plant)
        db.session.commit()

    form = AddPlantToGardenForm()
    form.garden.choices = [(g.id, g.name) for g in Garden.query.filter(Garden.user_id==g.user.id)]

    user = User.query.get_or_404(g.user.id)

    return render_template("plants/plant-details.html", plant=plant, user=user, form=form)

@app.route('/plants/<int:plant_id>/save', methods=['GET', 'POST'])
def save_plant(plant_id):
    """save or unsave a plant"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    plant = Plant.query.get(plant_id)

    g.user.plants.append(plant)
    db.session.commit()

    return render_template("/plants/saved-plants.html")

@app.route('/plants/<int:plant_id>/delete', methods=['GET', 'POST'])
def delete_plant(plant_id):
    """delete a plant from saved"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    plant = Plant.query.get(plant_id)

    g.user.plants.remove(plant)
    db.session.commit()

    return render_template("/plants/saved-plants.html")

@app.route('/plants/<int:plant_id>/add-plant', methods=['GET', 'POST'])
def add_plant_to_garden(plant_id):
    """add a plant to a garden using a dropdown menu"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    plant = Plant.query.get_or_404(plant_id)
    plant_name = plant.name
    form = AddPlantToGardenForm()


    if form.validate_on_submit():

        garden_id = form.garden.data
        garden = Garden.query.get_or_404(garden_id)
        garden.plants.append(plant)
        db.session.commit()

        return redirect(f"/gardens/{garden_id}")

    else:
        return redirect(f'/plants/{plant_name}')

@app.route('/plants/<int:plant_id>/<int:garden_id>/delete-plant', methods=['GET', 'POST'])
def delete_plant_from_garden(plant_id, garden_id):
    """delete a plant from a garden"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    garden = Garden.query.get(garden_id)
    plant = Plant.query.get(plant_id)
    garden.plants.remove(plant)
    db.session.commit()

    return redirect(f"/gardens/{garden_id}")

# routes for gardens

@app.route('/gardens', methods=['GET', 'POST'])
def users_gardens():
    """list a users created gardens and handle adding a new garden"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    form = AddGardenForm()

    if form.validate_on_submit():
        name = request.form['name']
        description = request.form['description']
        user_id = g.user.id

        garden = Garden(name=name, description=description, user_id=user_id)

        db.session.add(garden)
        db.session.commit()
        gardens = Garden.query.filter(Garden.user_id == g.user.id)

        return redirect("/gardens")

    gardens = Garden.query.filter(Garden.user_id == g.user.id)
    return render_template("gardens/my-gardens.html", form=form, gardens=gardens)


@app.route('/gardens/<int:garden_id>')
def garden_details(garden_id):
    """view the details of a garden and its plants"""

    garden = Garden.query.get_or_404(garden_id)

    return render_template("gardens/garden-details.html", garden=garden)

@app.route('/gardens/<int:garden_id>/delete', methods=["GET", "POST"])
def delete_garden(garden_id):
    """delete a users saved garden"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    user = Garden.query.get_or_404(garden_id).user_id

    if g.user == None or g.user.id != user:
        flash("Access unauthorized", "danger")
        return redirect("/")

    else:
        garden = Garden.query.get(garden_id)
        db.session.delete(garden)
        db.session.commit()
    
    return redirect("/gardens")

@app.route('/gardens/<int:garden_id>/save')
def save_gardens(garden_id):
    """save another users garden for later inspiration"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    garden = Garden.query.get_or_404(garden_id)
    g.user.gardens.append(garden)
    db.session.commit()

    return render_template("gardens/inspirations.html")

@app.route('/gardens/<int:garden_id>/delete-save')
def delete_saved_gardens(garden_id):
    """save another users garden for later inspiration"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    garden = Garden.query.get_or_404(garden_id)
    g.user.gardens.remove(garden)
    db.session.commit()

    return render_template("gardens/inspirations.html")

@app.route('/gardens/save/show')
def show_saved_gardens():
    """shows a list of saved gardens"""

    return render_template ("gardens/inspirations.html")

# follows routes

@app.route('/follows/<int:user_id>')
def show_follows(user_id):
    """shows a list of follows a user has"""

    user = User.query.get_or_404(user_id)
    follows = user.followed_users

    return render_template("/users/list-follows.html", follows=follows, user=user)

@app.route('/follows/add/<int:user_id>', methods=['POST'])
def add_follow(user_id):
    """follow another user"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    followed_user = User.query.get_or_404(user_id)
    g.user.followed_users.append(followed_user)
    db.session.commit()

    return redirect(f"/follows/{g.user.id}")

@app.route('/follows/remove/<int:user_id>', methods=['POST'])
def remove_follow(user_id):
    """unfollow another user"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    followed_user = User.query.get(user_id)
    g.user.followed_users.remove(followed_user)
    db.session.commit()

    return redirect(f"/follows/{g.user.id}")

# Routes for weather

@app.route('/weather')
def weather_page():
    """Show page for weather prediction"""

    if not g.user:
        flash("Access Unauthorized")
        return redirect("/")

    zipcode = g.user.location

    api_results = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key=1db06177940b420fa9c140429212707&q={zipcode}&days=5&aqi=no&alerts=no').json()

    # if api_results['error'] == True:
    #     return('Invalid zipcode. Please change zipcode in Edit User')

    return render_template("weather.html", api_results=api_results)



