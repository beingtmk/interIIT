global.gc();
const app = require('express')();
const mongoose = require('mongoose')
const bodyParser = require('body-parser')
const http = require('http').Server(app);
const io = require('socket.io')(http,{path:'/nodeserver'});

const getIOInstance = function(){
    return io;
};

var connected_clients = {"cricket":{},"athletics":{},"badminton":{},"basketball":{},"football":{},"squash":{},"swimming":{},"table_tennis":{},"volleyball":{},"weight_lifting":{},"water_polo":{},"tennis":{}};

const connectedClients = function(){
    return connected_clients;
};

const cricketScore = require('./routes/api/cricketScore')(getIOInstance,connectedClients)
const comment = require('./routes/api/comment')(getIOInstance,connectedClients)
const badmintonScore = require('./routes/api/badmintonScore')(getIOInstance,connectedClients)
const basketballScore = require('./routes/api/basketballScore')(getIOInstance,connectedClients)
const athleticsScore = require('./routes/api/athleticsScore')(getIOInstance,connectedClients)
const footballScore = require('./routes/api/footballScore')(getIOInstance,connectedClients)
const hockeyScore = require('./routes/api/hockeyScore')(getIOInstance,connectedClients)
const squashScore = require('./routes/api/squashScore')(getIOInstance,connectedClients)
const swimmingScore = require('./routes/api/swimmingScore')(getIOInstance,connectedClients)
const tableTennisScore = require('./routes/api/tableTennisScore')(getIOInstance,connectedClients)
const tennisScore = require('./routes/api/tennisScore')(getIOInstance,connectedClients)
const volleyballScore = require('./routes/api/volleyballScore')(getIOInstance,connectedClients)
const weightLiftingScore = require('./routes/api/weightLiftingScore')(getIOInstance,connectedClients)
const waterPoloScore = require('./routes/api/waterPoloScore')(getIOInstance,connectedClients)
const activeSports = require('./routes/api/activeSports')

const CricketScore = require('./models/CricketScore')
const Comment = require('./models/Comment')
const BadmintonScore = require('./models/BadmintonScore')
const BasketballScore = require('./models/BasketballScore')
const AthleticsScore = require('./models/AthleticsScore')
const FootballScore = require('./models/FootballScore')
const HockeyScore = require('./models/HockeyScore')
const SquashScore = require('./models/SquashScore')
const SwimmingScore = require('./models/SwimmingScore')
const TableTennisScore = require('./models/TableTennisScore')
const TennisScore = require('./models/TennisScore')
const VolleyballScore = require('./models/VolleyballScore')
const WeightLiftingScore = require('./models/WeightLiftingScore')
const WaterPoloScore = require('./models/WaterPoloScore')
const ActiveSports = require('./models/ActiveSports')


//Bodyparser
app.use(bodyParser.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
    extended: true
}));

/*
Each socket has a unique id and every socket will be assigned a match_id
Connected Client will have all the matches and each match will have sockets subscribed by it.
*/


//DB config
const db = require('./config/keys').mongoURI;

//Connect to Mongo
mongoose
.connect(db)
.then(() => console.log("MongoDB connected"))
.catch(err => console.log(err));

//Use score routes
app.use('/score', cricketScore);
app.use('/score', badmintonScore);
app.use('/score', basketballScore);
app.use('/score', athleticsScore);
app.use('/score', footballScore);
app.use('/score', hockeyScore);
app.use('/score', squashScore);
app.use('/score', swimmingScore);
app.use('/score', tableTennisScore);
app.use('/score', tennisScore);
app.use('/score', volleyballScore);
app.use('/score', weightLiftingScore);
app.use('/score', waterPoloScore);
app.use('/', comment);
app.use('/', activeSports);

function getTime(date){
    return msg = date.getHours().toString() + ":" + date.getMinutes().toString().padStart(2, '0') + ":" + date.getSeconds().toString().padStart(2, '0') + " - ";
}

function get5Comments(len, loc,socket){
    let loct = [];
    if(len===0){
        socket.emit("add_comment",{"comment_id":0,"comments":[]});
    }
    else if(len>0){
        Comment.findById(loc[0],function(err,commentmodel){
            if (err) handleError(err);
            loct.push(getTime(commentmodel.time) + commentmodel.text);
            if(loc.length<=1) socket.emit("add_comment",{"comment_id":len-1,"comments":loct});
            else{
                Comment.findById(loc[1],function(err,commentmodel2){
                    if (err) handleError(err);
                    loct.push(getTime(commentmodel2.time) + commentmodel2.text);
                    if(loc.length<=2) socket.emit("add_comment",{"comment_id":len-2,"comments":loct});
                    else{
                        Comment.findById(loc[2],function(err,commentmodel3){
                            if (err) handleError(err);
                            loct.push(getTime(commentmodel3.time) + commentmodel3.text);
                            if(loc.length<=3) socket.emit("add_comment",{"comment_id":len-3,"comments":loct});
                            else{
                                Comment.findById(loc[3],function(err,commentmodel4){
                                    if (err) handleError(err);
                                    loct.push(getTime(commentmodel4.time) + commentmodel4.text);
                                    if(loc.length<=4) socket.emit("add_comment",{"comment_id":len-4,"comments":loct});
                                    else{
                                        Comment.findById(loc[4],function(err,commentmodel5){
                                            if (err) handleError(err);
                                            loct.push(getTime(commentmodel5.time) + commentmodel5.text);
                                            socket.emit("add_comment",{"comment_id":len-5,"comments":loct});
                                        });
                                    }
                                });
                            }
                        });
                    }
                });
            }
        });
    }
}

function connect_new_client(model,socket,sport_type){
    model.findOne({'djangoID':socket.handshake.query.match_id}, function(err,modelscore){
        if (err) return handleError(err);
        if(modelscore===null){
            socket.emit("score_update","It seems like match has not started yet.");
            socket.emit("add_comment",{"comment_id":0,"comments":["Match has not started"]});

            return;
        };
        socket.match_id = modelscore.id;
        socket.sport = socket.handshake.query.sport;
        if(connected_clients[socket.sport][socket.match_id]){
            connected_clients[socket.sport][socket.match_id][socket.id] = socket.id;
        }
        else{
            connected_clients[socket.sport][socket.match_id] = {};
            connected_clients[socket.sport][socket.match_id][socket.id] = socket.id;
        }
        if(sport_type===1){
            if(modelscore.strike[0]==="A") socket.emit("score_update",modelscore.teamA + ": " + modelscore.pointA + " at " + modelscore.overs + " over(s).");
            else if(modelscore.strike[0]==="B") socket.emit("score_update",modelscore.teamB + ": " + modelscore.pointB + " at " + modelscore.overs + " over(s).");
        }
        else if(sport_type===2){
            socket.emit("score_update", "First: " + modelscore.first + "<br>Second: " + modelscore.second + "<br>Third: " + modelscore.third);
        }
        else if(sport_type===3){
            socket.emit("score_update", modelscore.teamA + ": " + modelscore.pointA + " - " + modelscore.teamB + ": " + modelscore.pointB);
        }
        let loc = modelscore.comment.slice(-5).reverse();
        let len = modelscore.comment.length;
        get5Comments(len,loc,socket);
    });
}

function load_comment(model,socket,msg){
    if(socket.match_id===undefined){
        return;
    }
    model.findById(socket.match_id, function (err, modelscore) {
        if(err) return handleError(err);
        let loc;
        if(msg.comment_id-5<0) loc = modelscore.comment.slice(0,msg.comment_id).reverse();
        else loc = modelscore.comment.slice(msg.comment_id-5,msg.comment_id).reverse();
        let len = msg.comment_id;
        get5Comments(len,loc,socket);
    });
}

io.on('connection', function (socket) {
    //Adding user to the list of connected clients and the matches he is subscribed to
    if(socket.handshake.query.sport==="cricket") connect_new_client(CricketScore,socket,1);
    else if(socket.handshake.query.sport==="athletics") connect_new_client(AthleticsScore,socket,2);
    else if(socket.handshake.query.sport==="badminton") connect_new_client(BadmintonScore,socket,3);
    else if(socket.handshake.query.sport==="basketball") connect_new_client(BasketballScore,socket,3);
    else if(socket.handshake.query.sport==="football") connect_new_client(FootballScore,socket,3);
    else if(socket.handshake.query.sport==="squash") connect_new_client(SquashScore,socket,3);
    else if(socket.handshake.query.sport==="swimming") connect_new_client(SwimmingScore,socket,2);
    else if(socket.handshake.query.sport==="table_tennis") connect_new_client(TableTennisScore,socket,3);
    else if(socket.handshake.query.sport==="volleyball") connect_new_client(VolleyballScore,socket,3);
    else if(socket.handshake.query.sport==="weight_lifting") connect_new_client(WeightLiftingScore,socket,1);
    else if(socket.handshake.query.sport==="water_polo") connect_new_client(WaterPoloScore,socket,3);
    else if(socket.handshake.query.sport==="tennis") connect_new_client(TennisScore,socket,3);

    socket.on('load_comment',function(msg){
        if(socket.handshake.query.sport==="cricket") load_comment(CricketScore,socket,msg);
        else if(socket.handshake.query.sport==="athletics") load_comment(AthleticsScore,socket,msg);
        else if(socket.handshake.query.sport==="badminton") load_comment(BadmintonScore,socket,msg);
        else if(socket.handshake.query.sport==="basketball") load_comment(BasketballScore,socket,msg);
        else if(socket.handshake.query.sport==="football") load_comment(FootballScore,socket,msg);
        else if(socket.handshake.query.sport==="squash") load_comment(SquashScore,socket,msg);
        else if(socket.handshake.query.sport==="swimming") load_comment(SwimmingScore,socket,msg);
        else if(socket.handshake.query.sport==="table_tennis") load_comment(TableTennisScore,socket,msg);
        else if(socket.handshake.query.sport==="volleyball") load_comment(VolleyballScore,socket,msg);
        else if(socket.handshake.query.sport==="weight_lifting") load_comment(WeightLiftingScore,socket,msg);
        else if(socket.handshake.query.sport==="water_polo") load_comment(WaterPoloScore,socket,msg);
        else if(socket.handshake.query.sport==="tennis") load_comment(TennisScore,socket,msg);
    });

    socket.on('disconnect',function(){
        if(socket.match_id !== undefined&&connected_clients[socket.sport][socket.match_id]&&connected_clients[socket.sport][socket.match_id][socket.id])
            delete connected_clients[socket.sport][socket.match_id][socket.id];                
    });
});


http.listen(3000, function () {

    console.log('Listening on *:3000');
});
