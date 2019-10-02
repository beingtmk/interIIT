var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var WaterPoloScoreSchema = new Schema({
    timestamp: {
        type: String,
        required: true
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
        default: "0"
    },
    pointB: {
        type: String,
        default: "0"
    },
    djangoID: {
        type: String,
        required:true
    }
}
);

//Export model
module.exports = mongoose.model('WaterPoloScore', WaterPoloScoreSchema);