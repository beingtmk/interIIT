var mongoose = require('mongoose');

var Schema = mongoose.Schema;

//Live score for a cricket match instance
var CricketScoreSchema = new Schema({
    winner: {
        type: String,
        default: ""
    },
    loser: {
        type: String,
        default: ""
    },
    comment: [{
        type: Schema.Types.ObjectId,
        ref: 'Comment',
    }],
    teamA: {
        type: String,
        required:true
    },
    teamB: {
        type: String,
        required:true
    },
    pointA: {
        type: String,
        default: "0/0"
    },
    pointB: {
        type: String,
        default: "0/0"
    },
    overs: {
        type: String,
        default: "0"
    },
    strike: {
        type: String,
        default: "A",
        enum: ["A","B"]
    },
    djangoID: {
        type: String,
        required:true
    }
  }
);

//Export model
module.exports = mongoose.model('CricketScore', CricketScoreSchema);