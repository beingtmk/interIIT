# interIIT Sports Live Score Backend 

This repo is for maintaining live score of all matches held during InterIIT Sports 2018.

## Important links:

  - [Test API backend](https://shrouded-waters-76897.herokuapp.com) is hosted on heroku.
  - [Test Database](https://mlab.com/databases/interiit) is hosted on mLab.

## API endpoints

Use [Postman](https://www.getpostman.com/apps) or curl to make HTTP requests to the site.

### Sports Endpoints

- POST Request -
    ```
    https://shrouded-waters-76897.herokuapp.com/score/<sport>/
    ``` 
    Description - Creates a new instance
    
    E.g. JSON body format - {"teamA":"IITG","teamB":"IITR"} for cricket.

- PUT Request -
    ```
    https://shrouded-waters-76897.herokuapp.com/score/<sport>/<id>
    ``` 
    Description - Updates the score
    
    E.g. JSON body format - {"winner?":"IITB","loser?":"IITM","pointA?":"22/1","pointB?":"22/1","overs?":"3.1","strike?":["A","B"]} for cricket.

- DELETE Request -
    ```
    https://shrouded-waters-76897.herokuapp.com/score/<sport>/<id>
    ``` 
    Description - Delete the specified instance and all its associated comments.
    
    E.g. JSON body format - No body has to be sent.

## Sports

\<sport\> has to be replaced with any of these:
* athlectics
* badminton
* basketball
* cricket
* football
* hockey
* squash
* swimming
* tabletennis
* tennis
* volleyball
* waterpolo
* weightlifting

For indiviual sport JSON format, see models/\<sport\>Score.js and routes/\<sport\>Score.js.

### Comment Endpoints

- POST Request -
    ```
    https://shrouded-waters-76897.herokuapp.com/comment/
    ``` 
    Description - Creates a new instance
    
    JSON body format - {"matchID":"xyz","text":"IITG has won the match."}

- PUT Request -
    ```
    https://shrouded-waters-76897.herokuapp.com/comment/<id>
    ``` 
    Description - Updates the comment
    
    JSON body format - {"text?":"Something new"}

- DELETE Request -
    ```
    https://shrouded-waters-76897.herokuapp.com/comment/<id>
    ``` 
    Description - Deletes the comment.
    
    JSON body format - No body has to be sent.

### Active sports Endpoints

Should be GET request
```
https://shrouded-waters-76897.herokuapp.com/active
``` 
Description - Returns the list of all active sports


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Install NodeJS and npm.
```
sudo apt-get install nodejs
sudo apt-get install npm
```


### Installing
1. Download the Repository and switch liveScoreBackend branch.

```
git clone https://github.com/swciitg/interIIT/
```
1. CD to liveScoreBackend, install dependencies and start server.

```
cd liveScoreBackend
npm install
npm install --dev
npm run server
```

3. Instead of above Heroku links, use 127.0.0.1:5000 for testing.

## Built With

* [ExpressJS](https://expressjs.com/)
* [MongooseJS](https://mongoosejs.com/)
* [MongoDB](https://www.mongodb.com/)
