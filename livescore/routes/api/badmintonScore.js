module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["badminton"];
    const express = require('express');
    const router = express.Router();

//Comment Model
const Comment = require('../../models/Comment');

//Badminton Model
const BadmintonScore = require('../../models/BadmintonScore');

// @route   GET score/badminton
// @desc    Get a badminton score instance
router.get('/badminton/:id',(req,res)=>{
    BadmintonScore.findOne({'djangoID':req.params.id},'comment',(err,badminton)=>{
        if(err||(!badminton)){
            res.json({
                success:false,
                err: err
            });
        }
        else{
            res.json({"comments": badminton.comment});
        }
    })
});

// @route   POST score/badminton
// @desc    Add a new badminton score instance to the database
router.post('/badminton',(req,res)=>{

    const newBadmintonInstance = new BadmintonScore({
        teamA: req.body.teamA,
        teamB: req.body.teamB,
        djangoID: req.body.id
    })

    newBadmintonInstance
    .save()
    .then(badmintonScore => res.json(badmintonScore))
    .catch((err) => res.json({
        success:false,
        message: err
    }));
});

// @route   PUT score/badminton
// @desc    Updates the badminton score instance 
router.put('/badminton/:id',(req,res)=>{
    BadmintonScore.findById(req.params.id)
    .then(badmintonScore => {

        if(req.body.winner){
            badmintonScore.winner = req.body.winner;
        }

        if(req.body.loser){
            badmintonScore.loser = req.body.loser;
        }

        if(req.body.pointA){
            badmintonScore.pointA = req.body.pointA;
        }

        if(req.body.pointB){
            badmintonScore.pointB = req.body.pointB;
        }

        badmintonScore.save((err) => {
            if(err){
                res.json({
                    success:false,
                    message: err
                })
            } 
            if(Object.entries(clients[req.params.id])){
                for (const [key, value] of Object.entries(clients[req.params.id])) {
                    getIOInstance().sockets.sockets[key].emit("score_update", badmintonScore.teamA + ": " + badmintonScore.pointA + " - " + badmintonScore.teamB + ": " + badmintonScore.pointB);
                }
            }
            res.json({
                success:"true",
                message:"Badminton Score updated"})
        })
    })
    .catch(err => res.json({
        success:false,
        message: err
    }))
});

// @route   DELETE score/badminton/:id
// @desc    Delete the specified badminton score instance
router.delete('/badminton/:id',(req,res)=>{

    //Cascade delete the comments associated with current match
    Comment.find({'matchID':req.params.id})
    .then((comments) => {
        Promise.all(comments.forEach((comment) => comment.remove()))
        .then(next());
    })


    BadmintonScore.findById(req.params.id)
    .then(badmintonScore => badmintonScore.remove()
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