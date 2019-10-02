var mongoose = require('mongoose');

var Schema = mongoose.Schema;

//Live score for a cricket match instance
var AthleticsScoreSchema = new Schema({
    first: {
        type: String,
        default: ""
    },
    second: {
        type: String,
        default: ""
    },
    third: {
        type: String,
        default: ""
    },
    comment: [{
        type: Schema.Types.ObjectId,
        ref: 'Comment',
    }],
    djangoID: {
        type: String,
        required:true
    }
  }
);

//Export model
module.exports = mongoose.model('AthleticsScore', AthleticsScoreSchema);