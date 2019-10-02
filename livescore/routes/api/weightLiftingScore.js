module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["weight_lifting"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //WeightLifting Model
    const WeightLiftingScore = require('../../models/WeightLiftingScore');

    // @route   GET score/weightLifting
    // @desc    Get a weightLifting score instance
    router.get('/weightLifting/:id',(req,res)=>{
        WeightLiftingScore.findOne({'djangoID':req.params.id},'comment',(err,weightLifting)=>{
            if(err||(!weightLifting)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": weightLifting.comment});
            }
        })
    });

    // @route   POST score/weightLifting
    // @desc    Add a new weightLifting score instance to the database
    router.post('/weightlifting',(req,res)=>{

        const newWeightLiftingInstance = new WeightLiftingScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newWeightLiftingInstance
        .save()
        .then(weightLiftingScore => res.json(weightLiftingScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/weightLifting
    // @desc    Updates the weightLifting score instance 
    router.put('/weightlifting/:id',(req,res)=>{
        WeightLiftingScore.findById(req.params.id)
        .then(weightLiftingScore => {

            if(req.body.winner){
                weightLiftingScore.winner = req.body.winner;
            }

            if(req.body.loser){
                weightLiftingScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                weightLiftingScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                weightLiftingScore.pointB = req.body.pointB;
            }

            if(req.body.overs){
                weightLiftingScore.overs = req.body.overs;
            }

            if(req.body.strike){
                weightLiftingScore.strike = req.body.strike;
            }

            weightLiftingScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        if (weightLiftingScore.strike[0] === 'A') {
                            getIOInstance().sockets.sockets[key].emit("score_update", weightLiftingScore.teamA + ": " + weightLiftingScore.pointA + " at " + weightLiftingScore.overs + " over(s).");
                        }
                        else if (weightLiftingScore.strike[0] === 'B') {
                            getIOInstance().sockets.sockets[key].emit("score_update", weightLiftingScore.teamB + ": " + weightLiftingScore.pointB + " at " + weightLiftingScore.overs + " over(s).");
                        }
                    }
                }
                res.json({
                    success:"true",
                    message:"WeightLifting Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/weightLifting/:id
    // @desc    Delete the specified weightLifting score instance
    router.delete('/weightlifting/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        WeightLiftingScore.findById(req.params.id)
        .then(weightLiftingScore => weightLiftingScore.remove()
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