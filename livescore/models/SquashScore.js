var mongoose = require('mongoose');

var Schema = mongoose.Schema;

//Live score for a Squash match instance
var SquashScoreSchema = new Schema({
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
    djangoID: {
        type: String,
        required:true
    }
  }
);

//Export model
module.exports = mongoose.model('SquashScore', SquashScoreSchema);