const express = require('express');
const router = express.Router();

const cricketScore = require('../../models/CricketScore')
const badmintonScore = require('../../models/BadmintonScore')
const basketballScore = require('../../models/BasketballScore')
const athleticsScore = require('../../models/AthleticsScore')
const footballScore = require('../../models/FootballScore')
const hockeyScore = require('../../models/HockeyScore')
const squashScore = require('../../models/SquashScore')
const swimmingScore = require('../../models/SwimmingScore')
const tableTennisScore = require('../../models/TableTennisScore')
const tennisScore = require('../../models/TennisScore')
const volleyballScore = require('../../models/VolleyballScore')
const weightLiftingScore = require('../../models/WeightLiftingScore')
const waterPoloScore = require('../../models/WaterPoloScore')

router.get('/active',async (req,res)=>{
    
    var sports=[];

    basketballScore.find({}, function(err, sport) {
        Promise.all(sport.forEach((s) => sports.push({"sport":"basketball",details:s})))
        .then((result)=>{})
        .catch((err)=>{});
        footballScore.find({}, function(err, sport) {
            Promise.all(sport.forEach((s) => sports.push({"sport":"football",details:s})))
            .then((result)=>{})
            .catch((err)=>{});
            cricketScore.find({}, function(err, sport) {
                Promise.all(sport.forEach((s) => sports.push({"sport":"cricket",details:s})))
                .then((result)=>{})
                .catch((err)=>{});
                badmintonScore.find({}, function(err, sport) {
                    Promise.all(sport.forEach((s) => sports.push({"sport":"badminton",details:s})))
                    .then((result)=>{})
                    .catch((err)=>{});
                    athleticsScore.find({}, function(err, sport) {
                        Promise.all(sport.forEach((s) => sports.push({"sport":"athletics",details:s})))
                        .then((result)=>{})
                        .catch((err)=>{});
                        hockeyScore.find({}, function(err, sport) {
                            Promise.all(sport.forEach((s) => sports.push({"sport":"hockey",details:s})))
                            .then((result)=>{})
                            .catch((err)=>{});
                            squashScore.find({}, function(err, sport) {
                                Promise.all(sport.forEach((s) => sports.push({"sport":"squash",details:s})))
                                .then((result)=>{})
                                .catch((err)=>{});
                                swimmingScore.find({}, function(err, sport) {
                                    Promise.all(sport.forEach((s) => sports.push({"sport":"swimming",details:s})))
                                    .then((result)=>{})
                                    .catch((err)=>{});
                                    tableTennisScore.find({}, function(err, sport) {
                                        Promise.all(sport.forEach((s) => sports.push({"sport":"tableTennis",details:s})))
                                        .then((result)=>{})
                                        .catch((err)=>{});
                                        tennisScore.find({}, function(err, sport) {
                                            Promise.all(sport.forEach((s) => sports.push({"sport":"tennis",details:s})))
                                            .then((result)=>{})
                                            .catch((err)=>{});
                                            volleyballScore.find({}, function(err, sport) {
                                                Promise.all(sport.forEach((s) => sports.push({"sport":"volleyball",details:s})))
                                                .then((result)=>{})
                                                .catch((err)=>{});
                                                waterPoloScore.find({}, function(err, sport) {
                                                    Promise.all(sport.forEach((s) => sports.push({"sport":"waterPolo",details:s})))
                                                    .then((result)=>{})
                                                    .catch((err)=>{});
                                                    weightLiftingScore.find({}, function(err, sport) {
                                                        Promise.all(sport.forEach((s) => sports.push({"sport":"weightLifting",details:s})))
                                                        .then((result)=>{})
                                                        .catch((err)=>{});
                                                        res.send({list:sports});
                                                    })
                                                })
                                            })
                                        })
                                    })
                                })
                            })
                        })
                    })
                })
            })
        })
    })

    // Promise.all(cricketScore.forEach(element => {
    //     sports.push({sport:"cricket",detail:element});
    // }))
    // .then(
    //      (result)=>{return Promise.all(badmintonScore.forEach(element => {
    //         sports.push({sport:"badminton",detail:element});
    //     }))}
    // )
    // .then(res.send(sports));

});

module.exports = router;