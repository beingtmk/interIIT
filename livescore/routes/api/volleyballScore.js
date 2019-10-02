module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["volleyball"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Volleyball Model
    const VolleyballScore = require('../../models/VolleyballScore');

    // @route   GET score/volleyball
    // @desc    Get a volleyball score instance
    router.get('/volleyball/:id',(req,res)=>{
        VolleyballScore.findOne({'djangoID':req.params.id},'comment',(err,volleyball)=>{
            if(err||(!volleyball)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": volleyball.comment});
            }
        })
    });

    // @route   POST score/volleyball
    // @desc    Add a new volleyball score instance to the database
    router.post('/volleyball',(req,res)=>{

        const newVolleyballInstance = new VolleyballScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newVolleyballInstance
        .save()
        .then(volleyballScore => res.json(volleyballScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/volleyball
    // @desc    Updates the volleyball score instance 
    router.put('/volleyball/:id',(req,res)=>{
        VolleyballScore.findById(req.params.id)
        .then(volleyballScore => {

            if(req.body.winner){
                volleyballScore.winner = req.body.winner;
            }

            if(req.body.loser){
                volleyballScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                volleyballScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                volleyballScore.pointB = req.body.pointB;
            }

            volleyballScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", volleyballScore.teamA + ": " + volleyballScore.pointA + " - " + volleyballScore.teamB + ": " + volleyballScore.pointB);
                    }
                }
                res.json({
                    success:"true",
                    message:"Volleyball Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/volleyball/:id
    // @desc    Delete the specified volleyball score instance
    router.delete('/volleyball/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        VolleyballScore.findById(req.params.id)
        .then(volleyballScore => volleyballScore.remove()
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