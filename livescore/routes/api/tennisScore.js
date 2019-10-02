module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["tennis"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Tennis Model
    const TennisScore = require('../../models/TennisScore');

    // @route   GET score/tennis
    // @desc    Get a tennis score instance
    router.get('/tennis/:id',(req,res)=>{
        TennisScore.findOne({'djangoID':req.params.id},'comment',(err,tennis)=>{
            if(err||(!tennis)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": tennis.comment});
            }
        })
    });


    // @route   POST score/tennis
    // @desc    Add a new tennis score instance to the database
    router.post('/tennis',(req,res)=>{

        const newTennisInstance = new TennisScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newTennisInstance
        .save()
        .then(tennisScore => res.json(tennisScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/tennis
    // @desc    Updates the tennis score instance 
    router.put('/tennis/:id',(req,res)=>{
        TennisScore.findById(req.params.id)
        .then(tennisScore => {

            if(req.body.winner){
                tennisScore.winner = req.body.winner;
            }

            if(req.body.loser){
                tennisScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                tennisScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                tennisScore.pointB = req.body.pointB;
            }

            if(req.body.setA){
                tennisScore.overs = req.body.setA;
            }

            if(req.body.setB){
                tennisScore.setB = req.body.setB;
            }

            tennisScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", tennisScore.teamA + ": " + tennisScore.pointA + " - " + tennisScore.teamB + ": " + tennisScore.pointB);
                    }
                }
                res.json({
                    success:"true",
                    message:"Tennis Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/tennis/:id
    // @desc    Delete the specified tennis score instance
    router.delete('/tennis/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        TennisScore.findById(req.params.id)
        .then(tennisScore => tennisScore.remove()
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