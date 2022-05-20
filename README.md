# Python Flask Backend for Unisoft CRM System

## Heroku link
https://unisoft-crm.herokuapp.com <br/><br/>

## Backend API socket
https://unisoft-back.herokuapp.com <br/><br/>

## Backend Api Docs
* [Authenication](https://documenter.getpostman.com/view/9959702/UUxzBnzt)
* [Contacts](https://documenter.getpostman.com/view/9959702/UUxzCULr)
* [Activities](https://documenter.getpostman.com/view/9959702/UV5Rkf8K) <br/><br/>

## Install requirements to run the server
* ```pip install -r requirements.txt```<br/><br/>
__Virtural environment:__
* ```source venv/bin/activate``` on Unix
* ```source venv/scripts/activate``` or  ```venv/scripts/activate``` on Windows <br/><br/>

## Start backend server
Run ```flask run```

## Deploy app on Heroku
* Create Heroku account
* Create requirements.txt file and record down all external library
* Create Procfile file and add line ```web: gunicorn app:app``` (since we are using gunicorn to deploy)
* Create a new app on heroku by clicking new on heroku dashboard
* Decide a app name and chose which server you want to use
* Connect heroku to github and ask authentication on github
* Enable automatic deploy below and wait for CI to pass
* Click on Deploy branch
