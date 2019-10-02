module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["table_tennis"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //TableTennis Model
    const TableTennisScore = require('../../models/TableTennisScore');

    // @route   GET score/tableTennis
    // @desc    Get a tableTennis score instance
    router.get('/tableTennis/:id',(req,res)=>{
        TableTennisScore.findOne({'djangoID':req.params.id},'comment',(err,tableTennis)=>{
            if(err||(!tableTennis)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": tableTennis.comment});
            }
        })
    });

    // @route   POST score/tableTennis
    // @desc    Add a new tableTennis score instance to the database
    router.post('/tabletennis',(req,res)=>{

        const newTableTennisInstance = new TableTennisScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newTableTennisInstance
        .save()
        .then(tableTennisScore => res.json(tableTennisScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/tableTennis
    // @desc    Updates the tableTennis score instance 
    router.put('/tabletennis/:id',(req,res)=>{
        TableTennisScore.findById(req.params.id)
        .then(tableTennisScore => {

            if(req.body.winner){
                tableTennisScore.winner = req.body.winner;
            }

            if(req.body.loser){
                tableTennisScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                tableTennisScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                tableTennisScore.pointB = req.body.pointB;
            }

            if(req.body.setA){
                tableTennisScore.setA = req.body.setA;
            }

            if(req.body.setB){
                tableTennisScore.setB = req.body.setB;
            }

            tableTennisScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", tableTennisScore.teamA + ": " + tableTennisScore.pointA + " - " + tableTennisScore.teamB + ": " + tableTennisScore.pointB);
                    }
                }

                res.json({
                    success:"true",
                    message:"TableTennis Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/tableTennis/:id
    // @desc    Delete the specified tableTennis score instance
    router.delete('/tabletennis/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        TableTennisScore.findById(req.params.id)
        .then(tableTennisScore => tableTennisScore.remove()
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