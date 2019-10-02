module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["water_polo"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //WaterPolo Model
    const WaterPoloScore = require('../../models/WaterPoloScore');

    // @route   GET score/waterPolo
    // @desc    Get a waterPolo score instance
    router.get('/waterPolo/:id',(req,res)=>{
        WaterPoloScore.findOne({'djangoID':req.params.id},'comment',(err,waterPolo)=>{
            if(err||(!waterPolo)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": waterPolo.comment});
            }
        })
    });

    // @route   POST score/waterPolo
    // @desc    Add a new waterPolo score instance to the database
    router.post('/waterpolo',(req,res)=>{

        const newWaterPoloInstance = new WaterPoloScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            timestamp: req.body.timestamp,
            djangoID: req.body.id
        })

        newWaterPoloInstance
        .save()
        .then(waterPoloScore => res.json(waterPoloScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/waterPolo
    // @desc    Updates the waterPolo score instance 
    router.put('/waterpolo/:id',(req,res)=>{
        WaterPoloScore.findById(req.params.id)
        .then(waterPoloScore => {

            if(req.body.pointA){
                waterPoloScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                waterPoloScore.pointB = req.body.pointB;
            }

            waterPoloScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", waterPoloScore.teamA + ": " + waterPoloScore.pointA + " - " + waterPoloScore.teamB + ": " + waterPoloScore.pointB);
                    }
                }
                res.json({
                    success:"true",
                    message:"WaterPolo Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/waterPolo/:id
    // @desc    Delete the specified waterPolo score instance
    router.delete('/waterpolo/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        WaterPoloScore.findById(req.params.id)
        .then(waterPoloScore => waterPoloScore.remove()
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