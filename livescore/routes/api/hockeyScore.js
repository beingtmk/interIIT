module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["hockey"];    
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Hockey Model
    const HockeyScore = require('../../models/HockeyScore');

    // @route   GET score/hockey
    // @desc    Get a hockey score instance
    router.get('/hockey/:id',(req,res)=>{
        HockeyScore.findOne({'djangoID':req.params.id},'comment',(err,hockey)=>{
            if(err||(!hockey)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": hockey.comment});
            }
        })
    });

    // @route   POST score/hockey
    // @desc    Add a new hockey score instance to the database
    router.post('/hockey',(req,res)=>{

        const newHockeyInstance = new HockeyScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newHockeyInstance
        .save()
        .then(hockeyScore => res.json(hockeyScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/hockey
    // @desc    Updates the hockey score instance 
    router.put('/hockey/:id',(req,res)=>{
        HockeyScore.findById(req.params.id)
        .then(hockeyScore => {

            if(req.body.winner){
                hockeyScore.winner = req.body.winner;
            }

            if(req.body.loser){
                hockeyScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                hockeyScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                hockeyScore.pointB = req.body.pointB;
            }

            hockeyScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", hockeyScore.teamA + ": " + hockeyScore.pointA + " - " + hockeyScore.teamB + ": " + hockeyScore.pointB);
                    }
                }
                res.json({
                    success:"true",
                    message:"Hockey Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/hockey/:id
    // @desc    Delete the specified hockey score instance
    router.delete('/hockey/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        HockeyScore.findById(req.params.id)
        .then(hockeyScore => hockeyScore.remove()
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