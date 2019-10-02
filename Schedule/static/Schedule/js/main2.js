$(document).ready(function(){
// Countdown Clock
  var BeginDate = new Date("Dec 15, 2018 18:00:00").getTime();
  
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
  <div class=\"numbers\"><b>" + days + "  :</b></div><div class=\"texts\">DAYS</div></div> \
<div class=\"hours\"> \
  <div class=\"numbers\"><b>" + hours +"  :</b></div><div class=\"texts\">HRS</div></div> \
<div class=\"minutes\"> \
  <div class=\"numbers\"><b>" + minutes +"  :</b></div><div class=\"texts\">MINS</div></div> \
  <div class=\"seconds\"> \
  <div class=\"numbers\"><b>" + seconds +"</b></div><div class=\"texts\">SECS</div></div> \
  ";

}, 1000);
  

});
$(document).ready(function() {
  $('#pagepiling').pagepiling({
      menu: null,
        direction: 'vertical',
        verticalCentered: true,
        sectionsColor: [],
        anchors: [],
        scrollingSpeed: 300,
        easing: 'swing',
       // afterRender: function(){
          //playing the video
       //   $('video').get(0).play();
      //  }
  });
  var height= $('.navbar').height();
});