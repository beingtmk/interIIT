module.exports = function (getIOInstance, connectedClients) {

    const express = require('express');
    const router = express.Router();

//Comment Model
const Comment = require('../../models/Comment');

const CricketScore = require('../../models/CricketScore');
const AthleticsScore = require('../../models/AthleticsScore');
const BadmintonScore = require('../../models/BadmintonScore');
const BasketballScore = require('../../models/BasketballScore');
const FootballScore = require('../../models/FootballScore');
const HockeyScore = require('../../models/HockeyScore');
const SquashScore = require('../../models/SquashScore');
const SwimmingScore = require('../../models/SwimmingScore');
const TableTennisScore = require('../../models/TableTennisScore');
const TennisScore = require('../../models/TennisScore');
const VolleyballScore = require('../../models/VolleyballScore');
const WaterPoloScore = require('../../models/WaterPoloScore');
const WeightLiftingScore = require('../../models/WeightLiftingScore');


// @route   GET comment/:id
// @desc    Get a comment instance
router.get('/comment/:id',(req,res)=>{
    Comment.findById(req.params.id)
    .then((comment)=>{
        res.json(comment);
    })
});

// @route   POST score/comment
// @desc    Add a new comment instance to the database
router.post('/comment',(req,res)=>{
    const newCommentInstance = new Comment({
        matchID: req.body.matchID,
        text: req.body.text
    })
    if(req.body.sport == "cricket"){
        CricketScore.findById(req.body.matchID)
        .then(cricketScore => {
            cricketScore.comment.push(newCommentInstance.id);
            cricketScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save cricket instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "athletics"){
        AthleticsScore.findById(req.body.matchID)
        .then(athleticsScore => {

            athleticsScore.comment.push(newCommentInstance.id);

            athleticsScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save athletics instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "badminton"){
        BadmintonScore.findById(req.body.matchID)
        .then(badmintonScore => {

            badmintonScore.comment.push(newCommentInstance.id);

            badmintonScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save badminton instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "basketball"){
        BasketballScore.findById(req.body.matchID)
        .then(basketballScore => {

            basketballScore.comment.push(newCommentInstance._id);

            basketballScore.save()
            .then(basketballScore => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save basketball instance",
                err: err
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "football"){
        FootballScore.findById(req.body.matchID)
        .then(footballScore => {

            footballScore.comment.push(newCommentInstance.id);

            footballScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save football instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "hockey"){
        HockeyScore.findById(req.body.matchID)
        .then(hockeyScore => {

            hockeyScore.comment.push(newCommentInstance.id);

            hockeyScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save hockey instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "squash"){
        SquashScore.findById(req.body.matchID)
        .then(squashScore => {

            squashScore.comment.push(newCommentInstance.id);

            squashScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save squash instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "swimming"){
        SwimmingScore.findById(req.body.matchID)
        .then(swimmingScore => {

            swimmingScore.comment.push(newCommentInstance.id);

            swimmingScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save swimming instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "tableTennis"){
        TableTennisScore.findById(req.body.matchID)
        .then(tableTennisScore => {

            tableTennisScore.comment.push(newCommentInstance.id);

            tableTennisScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save tableTennis instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "tennis"){
        TennisScore.findById(req.body.matchID)
        .then(tennisScore => {

            tennisScore.comment.push(newCommentInstance.id);

            tennisScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save tennis instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "volleyball"){
        VolleyballScore.findById(req.body.matchID)
        .then(volleyballScore => {

            volleyballScore.comment.push(newCommentInstance.id);

            volleyballScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save volleyball instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "waterPolo"){
        WaterPoloScore.findById(req.body.matchID)
        .then(waterPoloScore => {

            waterPoloScore.comment.push(newCommentInstance.id);

            waterPoloScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save waterPolo instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else if(req.body.sport == "weightLifting"){
        WeightLiftingScore.findById(req.body.matchID)
        .then(weightLiftingScore => {

            weightLiftingScore.comment.push(newCommentInstance.id);

            weightLiftingScore.save()
            .then(a => {
                newCommentInstance
                .save()
                .then(comment => res.json(comment))
                .catch((err) => res.json({
                    success:false,
                    message: "Unable to save comment instance"
                }));
            })
            .catch((err) => res.json({
                success:false,
                message: "Unable to save weightLifting instance"
            }));

        })
        .catch((err) => res.json({
            success:false,
            message: "Unable to find match instance"
        }));
    }
    else{
        res.json({
            success:false,
            message: "Please specify sport type"
        })
    }


    if (req.body.text){
        let date = new Date();
        let msg = date.getHours().toString() + ":" + date.getMinutes().toString().padStart(2, '0') + ":" + date.getSeconds().toString().padStart(2, '0') + " - " + req.body.text
        let match_id = req.body.matchID;
        let sport = req.body.sport;
        sport = sport.replace(/([A-Z])/g, "_$1").toLowerCase();
        if(connectedClients()[sport]&&connectedClients()[sport][match_id]&&Object.entries(connectedClients()[sport][match_id])){    
            for (const [key, value] of Object.entries(connectedClients()[sport][match_id])) {
                getIOInstance().sockets.sockets[key].emit("comment", msg);
            }
        }
    }
    // CricketScore.findOneAndUpdate(
    //     req.body.matchID,
    //     {
    //         $push: {"comment":req.body.matchID}
    //     },
    //     {safe: true, upsert: true},
    //     function(err, model) {
    //         console.log(err);
    //     }
    // );
    
});

// @route   PUT score/comment
// @desc    Updates the comment instance 
router.put('/comment/:id',(req,res)=>{
    Comment.findById(req.params.id)
    .then(comment => {

        if(req.body.text){
            comment.text = req.body.text;
        }

        comment.save((err) => {
            if(err){
                res.json({
                    success:false,
                    message: err
                })
            }
            res.json({
                success:"true",
                message:"Comment updated"
            })
        })
    })
    .catch(err => res.json({
        success:false,
        message: err
    }))
});

// @route   DELETE score/comment/:id
// @desc    Delete the specified comment instance
router.delete('/comment/:id',(req,res)=>{
    Comment.findById(req.params.id)
    .then(comment => comment.remove()
        .then(() => res.json({
            success: true,
            message: "Instance deleted successfully"
        }))
        ).catch(err => res.status(404).json({
            success:false,
            message: "Instance not found"
        }))
    });

return router;
};
