var mongoose = require('mongoose');

var Schema = mongoose.Schema;

//Comment for any match
var CommentSchema = new Schema({
    time: {
        type: Date,
        default: Date.now
    },
    matchID: {
        type: Schema.Types.ObjectId,
        ref: 'MatchID',
        required: true
    },
    text: {
        type: String,
        required:true
    },
  }
);

//Export model
module.exports = mongoose.model('Comment', CommentSchema);