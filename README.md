# Virtual Garden

My completed Capstone Project

### Live on Heroku
### https://virtual-garden-project.herokuapp.com/

## Description

Virtual Garden is a web application that allows a user access to useful information for growing a variety of plants (description, growing conditions, sowing method) via the OpenFarm API. A User can save these planta for later use or add them to a "Garden" of their creation. A user may also save other users' gardens as inspiration for their own. A local weather tab provides weather to the user to plan when they can garden!

### Plants

<img width="1440" alt="Screen Shot 2021-09-28 at 11 49 07 AM" src="https://user-images.githubusercontent.com/62483491/135122281-aa216916-f8c9-4d9d-84f4-4dd321d8b8ce.png">

<img width="1440" alt="Screen Shot 2021-09-28 at 11 49 20 AM" src="https://user-images.githubusercontent.com/62483491/135122304-7d9d46b7-ab75-457d-8afd-d964e987b218.png">

### Gardens

<img width="1440" alt="Screen Shot 2021-09-28 at 11 50 37 AM" src="https://user-images.githubusercontent.com/62483491/135122252-d169ce3f-32be-487d-ac8c-c33e4549a353.png">

### Weather

<img width="1439" alt="Screen Shot 2021-09-28 at 11 49 44 AM" src="https://user-images.githubusercontent.com/62483491/135122138-5e885529-491f-49de-94e7-68f8aed7d75c.png">

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
