module.exports = function (getIOInstance, connectedClients) {
    var clients = connectedClients()["basketball"];
    const express = require('express');
    const router = express.Router();

    //Comment Model
    const Comment = require('../../models/Comment');

    //Basketball Model
    const BasketballScore = require('../../models/BasketballScore');


    // var commentsList=[];




    // @route   GET score/basketball
    // @desc    Get a basketball score instance
    router.get('/basketball/:id',(req,res)=>{
        BasketballScore.findOne({'djangoID':req.params.id},'comment',(err,basketball)=>{
            if(err||(!basketball)){
                res.json({
                    success:false,
                    err: err
                });
            }
            else{
                // commentsList=[];
                // function add(x){
                //     commentsList.push(x);
                // }
                // (basketball.comment).forEach((id)=>{
                //     Comment.findById(id)
                //     .then(comment=>{
                //         add(comment.text);
                //         console.log(comment.text);
                //     })
                //     .catch((err) => res.json({
                //         success:false,
                //         message: err
                //     }))
                // })
                res.json({"comments": basketball.comment});
            }
        })
    });

    // @route   POST score/basketball
    // @desc    Add a new basketball score instance to the database
    router.post('/basketball',(req,res)=>{

        const newBasketballInstance = new BasketballScore({
            teamA: req.body.teamA,
            teamB: req.body.teamB,
            djangoID: req.body.id
        })

        newBasketballInstance
        .save()
        .then(basketballScore => res.json(basketballScore))
        .catch((err) => res.json({
            success:false,
            message: err
        }));
    });

    // @route   PUT score/basketball
    // @desc    Updates the basketball score instance 
    router.put('/basketball/:id',(req,res)=>{
        BasketballScore.findById(req.params.id)
        .then(basketballScore => {

            if(req.body.winner){
                basketballScore.winner = req.body.winner;
            }

            if(req.body.loser){
                basketballScore.loser = req.body.loser;
            }

            if(req.body.pointA){
                basketballScore.pointA = req.body.pointA;
            }

            if(req.body.pointB){
                basketballScore.pointB = req.body.pointB;
            }

            basketballScore.save((err) => {
                if(err){
                    res.json({
                        success:false,
                        message: err
                    })
                }
                if(clients&&clients[req.params.id]&&Object.entries(clients[req.params.id])){
                    for (const [key, value] of Object.entries(clients[req.params.id])) {
                        getIOInstance().sockets.sockets[key].emit("score_update", basketballScore.teamA + ": " + basketballScore.pointA + " - " + basketballScore.teamB + ": " + basketballScore.pointB);
                    }
                }

                res.json({
                    success:"true",
                    message:"Basketball Score updated"})
            })
        })
        .catch(err => res.json({
            success:false,
            message: err
        }))
    });

    // @route   DELETE score/basketball/:id
    // @desc    Delete the specified basketball score instance
    router.delete('/basketball/:id',(req,res)=>{

        //Cascade delete the comments associated with current match
        Comment.find({'matchID':req.params.id})
        .then((comments) => {
            Promise.all(comments.forEach((comment) => comment.remove()))
            .then(next());
        })


        BasketballScore.findById(req.params.id)
        .then(basketballScore => basketballScore.remove()
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