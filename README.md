# interIIT Sports Website

This is the repository for interIIT Sport website for the year 2018, Currently the Schedule and Results part of the website is being developed.

## Website is deployed on Python Anywhere:
  - [link to live website](https://beingtmk.pythonanywhere.com)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- install [Django](https://pip.pypa.io/en/latest/installing/#installing-with-get-pip-py)


### Installing
1. Download the Repository

```
git clone https://github.com/swciitg/interIIT/
```
2. CD to interIIT and install requirements and runserver

```
cd interIIT
pip install -r requirements.txt
python manage.py runserver
```

3. This should open a browser tab with address **127.0.0.1:8000/**,

## Built With

* HTML/CSS
* JavaScript
* Python (Django)

## Notes

* You will have to Login to use the Forms,
  * User : staff
  * password : staff@interiit

* For **Athletics**,**WeightLifting** and **Swimming**, we have to add player individually by using "**Add Player**" button, and score will be updated individually by using "**Player Score Update**" button. 
