module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["squash"]; 
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Squash Model
    const SquashScore = require('../../models/SquashScore');

    // @route   GET score/squash
    // @desc    Get a squash score instance
    router.get('/squash/:id',(req,res)=>{
        SquashScore.findOne({'djangoID':req.params.id},'comment',(err,squash)=>{
            if(err||(!squash)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": squash.comment});
            }
        })
    });

    // @route   POST score/squash
    // @desc    Add a new squash score instance to the database
    router.post('/squash',(req,res)=>{

        const newSInstance = new SquashScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newSquashInstance
        .save()
        .then(squashScore => res.json(squashScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/squash
    // @desc    Updates the squash score instance 
    router.put('/squash/:id',(req,res)=>{
        SquashScore.findById(req.params.id)
        .then(squashScore => {

            if(req.body.winner){
                squashScore.winner = req.body.winner;
            }

            if(req.body.loser){
                squashScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                squashScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                squashScore.pointB = req.body.pointB;
            }

            squashScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", squashScore.teamA + ": " + squashScore.pointA + " - " + squashScore.teamB + ": " + squashScore.pointB);
                    }
                }
                res.json({
                    success:"true",
                    message:"Squash Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/squash/:id
    // @desc    Delete the specified squash score instance
    router.delete('/squash/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        SquashScore.findById(req.params.id)
        .then(squashScore => squashScore.remove()
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