[![Build Status](https://travis-ci.org/Ogollah/WeConnect.svg?branch=develop)](https://travis-ci.org/Ogollah/WeConnect)

[![Maintainability](https://api.codeclimate.com/v1/badges/d26d3f22320cf60e59ce/maintainability)](https://codeclimate.com/github/Ogollah/WeConnect/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/d26d3f22320cf60e59ce/test_coverage)](https://codeclimate.com/github/Ogollah/WeConnect/test_coverage)
# WeConnect
An App that help connect people and businesses

## About

WeConnect is an app that connects businesses and individuals together by creating awareness of the business and provides oppotunity for users to write reviews about the business.

## Features

  1. User can create create a new account
  2. User can log in and out of the account
  3. Authenticated user can create a business for users to review
  4. Authenticated user can post a review for a business
  5. Business owner can read reviews about their business
  6. Account owner with business can edit business profile and delete business

  | EndPoint                                             | Functionality                                    |
| ---------------------------------------------------- | ------------------------------------------------ |
| POST   /app/v1/user/auth/register                   | Creates a user account                          |
| POST   /app/v1/user/auth/login                       | Logs in a user                                 |
| POST   /app/v1/user/auth/logout                      | Logs out a user                                |
| POST   /app/v1/user/auth/resetPassword              | Password reset                                 |
| POST   /app/v1/businesses/registration                       | Register a business                            |

## Technologies

* Python 3.6 or 2.7

## Requirements

* Install [Python](https://www.python.org/downloads/)
* Run `pip install virtualenv` on command prompt
* Run `pip install virtualenvwrapper-win` on command prompt

## Setup

* Run `git clone` this repository and `cd WeConnect` .
* Run `python3 -m venv env` on command prompt
* Run `source env/bin/activate` on command prompt
* Run `pip install -r requirements.txt` on command prompt
* Run `set FLASK_APP=run.py` on command prompt
* Run `flask run` on command prompt
* View the app on `http://127.0.0.1:5000/`

## Use endpoints

* You can proceed with the above url or run `python run.py` on command prompt

## Unittests

* Run `nosetests` on command prompt

## Framework and Language

 1. HTML
 2. CSS
 3. Bootstrap
 4. JavaScript/ES6/Reactjs
 5. Python/Flask

## GitHub pages

Go to [WeConnect](https://ogollah.github.io/WeConnect/)