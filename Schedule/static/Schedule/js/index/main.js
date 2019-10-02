$(document).ready(function(){
// Countdown Clock
  var BeginDate = new Date("Oct 03, 2018 08:30:00").getTime();
  
  var timer = setInterval(function() {

  // get today's date
  var today = new Date().getTime();

  // get the difference
  var diff = BeginDate - today;

  // math
  var days = Math.floor(diff / (1000 * 60 * 60 * 24));
  var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((diff % (1000 * 60)) / 1000);
  hours = ("0" + hours).slice(-2);
  minutes = ("0" + minutes).slice(-2);
  seconds = ("0" + seconds).slice(-2);
  // display
  document.getElementById("countdown").innerHTML =
    "<div class=\"days\"> \
  <div class=\"numbers\"><b>" + days + "     </b><small>  :</small></div><div class=\"textdays\">Days</div></div> \
<div class=\"hours\"> \
  <div class=\"numbers\"><b>" + hours +"     </b><small>  :</small></div><div class=\"texthrs\">Hours</div></div> \
<div class=\"minutes\"> \
  <div class=\"numbers\"><b>" + minutes +"</b></div><div class=\"textmin\">Minutes</div></div> \
  </div> \
  ";

}, 1000);
});
