module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["cricket"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Cricket Model
    const CricketScore = require('../../models/CricketScore');

    // @route   GET score/cricket
    // @desc    Get a cricket score instance
    router.get('/cricket/:id',(req,res)=>{
        CricketScore.findOne({'djangoID':req.params.id},'comment',(err,cricket)=>{
            if(err||(!cricket)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": cricket.comment});
            }
        })
    });

    // @route   POST score/cricket
    // @desc    Add a new cricket score instance to the database
    router.post('/cricket',(req,res)=>{

        const newCriketInstance = new CricketScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newCriketInstance
        .save()
        .then(cricketScore => res.json(cricketScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });
    // @route   PUT score/cricket
    // @desc    Updates the cricket score instance 
    router.put('/cricket/:id',(req,res)=>{
        CricketScore.findById(req.params.id)
        .then(cricketScore => {
            if(req.body.winner){
                cricketScore.winner = req.body.winner;
            }

            if(req.body.loser){
                cricketScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                cricketScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                cricketScore.pointB = req.body.pointB;
            }

            if(req.body.overs){
                cricketScore.overs = req.body.overs;
            }

            if(req.body.strike){
                cricketScore.strike = req.body.strike;
            }

            cricketScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        if (cricketScore.strike[0] === 'A') {
                            getIOInstance().sockets.sockets[key].emit("score_update", cricketScore.teamA + ": " + cricketScore.pointA + " at " + cricketScore.overs + " over(s).");
                        }
                        else if (cricketScore.strike[0] === 'B') {
                            getIOInstance().sockets.sockets[key].emit("score_update", cricketScore.teamB + ": " + cricketScore.pointB + " at " + cricketScore.overs + " over(s).");
                        }
                    }
                }
                res.json({
                    success:"true",
                    message:"Cricket Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/cricket/:id
    // @desc    Delete the specified cricket score instance
    router.delete('/cricket/:id',(req,res)=>{

    //Cascade delete the comments associated with current match
    Comment.find({'matchID':req.params.id})
    .then((comments) => {
        Promise.all(comments.forEach((comment) => comment.remove()))
        .then(next());
    })


    CricketScore.findById(req.params.id)
    .then(cricketScore => cricketScore.remove()
        .then(() => res.json({
            success: true,
            message: "Instance deleted successfully"
        }))
        ).catch(err => res.status(404).json({
            success:false,
            message: "Instance not found"
        }))
    });

    return router
};