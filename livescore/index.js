var app = require('express')();
var bodyParser = require('body-parser')
app.use(bodyParser.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
    extended: true
}));
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function (req, res) {
    res.send("<h1>Initial Setup</h1>");
});

connected_clients = {};
/*
Each socket has a unique id and every socket will be assigned a match_id
Connected Client will have all the matches and each match will have sockets subscribed by it.
*/

io.on('connection', function (socket) {
    //Adding user to the list of connected clients and the matches he is subscribed to
    socket.match_id = socket.handshake.query.match_id;
    console.log('User Has Joined');
    if(connected_clients[socket.match_id]){
        connected_clients[socket.match_id][socket.id] = socket.id;
    }
    else{
        connected_clients[socket.match_id] = {};
        connected_clients[socket.match_id][socket.id] = socket.id;
    }
    console.log(connected_clients);

    // 35/3 to be replaced by DB fetch
    io.sockets.sockets[socket.id].emit("score_update","35/3 overs.");
    
    io.sockets.sockets[socket.id].emit("add_comment",{"comment_id":35,"comments":["comment1","comment2","comment2","comment2","comment2"]});

    // the first comment is the latest one and the comment id sent will be of the last one
    socket.on('load_comment',function(msg){
        // this is was
        socket.emit("add_comment",{"comment_id":35,"comments":["comment5","comment6","comment2","comment3","comment4"]});
    });

    //on disconnect delete the user from connected list.
    socket.on('disconnect',function(){
        if(connected_clients[socket.match_id]&&connected_clients[socket.match_id][socket.id])
        delete connected_clients[socket.match_id][socket.id];                
        console.log("User Disconnected from Match_id : " + socket.match_id);
    });
});



app.get('/broadcast',function(req,res){
    /*
        Params:
        Score Update/Comment : type : 0/1
        Match id : mid : integer
        Message : message : string (Can be score or comment depending on the type)
    */
    if(connected_clients[req.query.mid]){
        res.send('Broadcasting message to users subscribed with match_id : ' + req.query.mid);
        if(req.query.type==="1"){
            let date = new Date();
            let msg = date.getHours().toString() + ":" + date.getMinutes().toString().padStart(2,'0') +":" + date.getSeconds().toString().padStart(2,'0') + " - " + req.query.message
            for (const[key,value] of Object.entries(connected_clients[req.query.mid])){
                io.sockets.sockets[key].emit("comment",msg);
            }
        }
        else if(req.query.type==="0"){
            for (const[key,value] of Object.entries(connected_clients[req.query.mid])){
                io.sockets.sockets[key].emit("score_update",req.query.message);
            }
        }
    }
    else{
        res.send("Invalid Match ID");
    }
});


http.listen(3000, function () {
    console.log('Listening on *:3000');
});
