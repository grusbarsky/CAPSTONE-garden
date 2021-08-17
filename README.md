# Virtual Garden

My completed Capstone Project

### Live on Heroku
### https://virtual-garden-project.herokuapp.com/

## Description

Virtual Garden is a web application that allows a user access to useful information for growing a variety of plants (description, growing conditions, sowing method) via the OpenFarm API. A User can save these planta for later use or add them to a "Garden" of their creation. A user may also save other users' gardens as inspiration for their own. A local weather tab provides weather to the user to plan when they can garden!

### Plants

<img width="1440" alt="Screen Shot 2021-08-17 at 9 14 15 AM" src="https://user-images.githubusercontent.com/62483491/129747382-71f7585c-f59f-44b2-966f-6711bfdade94.png">

<img width="1440" alt="Screen Shot 2021-08-17 at 9 37 59 AM" src="https://user-images.githubusercontent.com/62483491/129747279-4ce27ec5-92e0-4331-a81e-6bade4fa5b5d.png">


### Gardens

<img width="1440" alt="Screen Shot 2021-08-17 at 9 38 55 AM" src="https://user-images.githubusercontent.com/62483491/129747202-3cf8746b-cfba-498d-8652-156eff18d561.png">

### Weather

<img width="1440" alt="Screen Shot 2021-08-17 at 9 40 19 AM" src="https://user-images.githubusercontent.com/62483491/129747485-4f631e4b-db03-47d4-b58f-16f6158c8576.png">

## How to download and use locally
### Create a virtual environment and activate
$ python3 -m venv venv
$ source venv/bin/activate

### Install Dependencies
(venv) $ pip install -r requirements.txt

### Create a database using postgreSQL
(venv) $ createdb garden

## APIs used
  * https://www.weatherapi.com/
  * https://github.com/openfarmcc/OpenFarm
