module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["football"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Football Model
    const FootballScore = require('../../models/FootballScore');

    // @route   GET score/football
    // @desc    Get a football score instance
    router.get('/football/:id',(req,res)=>{
        FootballScore.findOne({'djangoID':req.params.id},'comment',(err,football)=>{
            if(err||(!football)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": football.comment});
            }
        })
    });

    // @route   POST score/football
    // @desc    Add a new football score instance to the database
    router.post('/football',(req,res)=>{

        const newFootballInstance = new FootballScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newFootballInstance
        .save()
        .then(footballScore => res.json(footballScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/football
    // @desc    Updates the football score instance 
    router.put('/football/:id',(req,res)=>{
        FootballScore.findById(req.params.id)
        .then(footballScore => {

            if(req.body.winner){
                footballScore.winner = req.body.winner;
            }

            if(req.body.loser){
                footballScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                footballScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                footballScore.pointB = req.body.pointB;
            }

            footballScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", footballScore.teamA + ": " + footballScore.pointA + " - " + footballScore.teamB + ": " + footballScore.pointB);
                    }
                }

                res.json({
                    success:"true",
                    message:"Football Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/football/:id
    // @desc    Delete the specified football score instance
    router.delete('/football/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        FootballScore.findById(req.params.id)
        .then(footballScore => footballScore.remove()
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