module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["swimming"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Swimming Model
    const SwimmingScore = require('../../models/SwimmingScore');

    // @route   GET score/swimming
    // @desc    Get a swimming score instance
    router.get('/swimming/:id',(req,res)=>{
        SwimmingScore.findOne({'djangoID':req.params.id},'comment',(err,swimming)=>{
            if(err||(!swimming)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": swimming.comment});
            }
        })
    });

    // @route   POST score/swimming
    // @desc    Add a new swimming score instance to the database
    router.post('/swimming',(req,res)=>{

        const newSwimmingInstance = new SwimmingScore({
            djangoID: req.body.id
        })

        newSwimmingInstance
        .save()
        .then(swimmingScore => res.json(swimmingScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/swimming
    // @desc    Updates the swimming score instance 
    router.put('/swimming/:id',(req,res)=>{
        SwimmingScore.findById(req.params.id)
        .then(swimmingScore => {

            if(req.body.first){
                swimmingScore.first = req.body.first;
            }

            if(req.body.second){
                swimmingScore.second = req.body.second;
            }

            if(req.body.third){
                swimmingScore.third = req.body.third;
            }

            swimmingScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", "First: " + swimmingScore.first + "<br>Second: " + swimmingScore.second + "<br>Third: " + swimmingScore.third);
                    }
                }
                res.json({
                    success:"true",
                    message:"Swimming Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/swimming/:id
    // @desc    Delete the specified swimming score instance
    router.delete('/swimming/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        SwimmingScore.findById(req.params.id)
        .then(swimmingScore => swimmingScore.remove()
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