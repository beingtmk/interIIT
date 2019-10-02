module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["athletics"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Athlectics Model
    const AthleticsScore = require('../../models/AthleticsScore');

    // @route   GET score/athletics
    // @desc    Get a athletics score instance
    router.get('/athletics/:id',(req,res)=>{
        AthleticsScore.findOne({'djangoID':req.params.id},'comment',(err,athletics)=>{
            if(err||(!athletics)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                res.json({"comments": athletics.comment});
            }
        })
    });

    // @route   POST score/Athlectics
    // @desc    Add a new Athlectics score instance to the database
    router.post('/athletics',(req,res)=>{

        const newAthlecticsInstance = new AthleticsScore({
            djangoID: req.body.id
        })

        newAthlecticsInstance
        .save()
        .then(AthleticsScore => res.json(AthleticsScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/Athlectics
    // @desc    Updates the Athlectics score instance 
    router.put('/athletics/:id',(req,res)=>{
        AthleticsScore.findById(req.params.id)
        .then(athleticsScore => {

            if(req.body.first){
                athleticsScore.first = req.body.first;
            }

            if(req.body.second){
                athleticsScore.second = req.body.second;
            }

            if(req.body.thrid){
                athleticsScore.third = req.body.third;
            }

            if(req.body.comment){
                athleticsScore.comment = req.body.comment;
            }

            athleticsScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", "First: " + athleticsScore.first + "<br>Second: " + athleticsScore.second + "<br>Third: " + athleticsScore.third);
                    }
                }
                res.json({
                    success:"true",
                    message:"Athlectics Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/Athlectics/:id
    // @desc    Delete the specified Athlectics score instance
    router.delete('/athletics/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        AthleticsScore.findById(req.params.id)
        .then(athleticsScore => athleticsScore.remove()
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