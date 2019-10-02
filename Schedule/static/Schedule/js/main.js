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

  // display
  document.getElementById("countdown").innerHTML =
    "<div class=\"days\"> \
  <div class=\"numbers\"><b>" + days + ":</b></div><div class=\"texts\">Days</div></div> \
<div class=\"hours\"> \
  <div class=\"numbers\"><b>" + hours +":</b></div><div class=\"texts\">Hrs</div></div> \
<div class=\"minutes\"> \
  <div class=\"numbers\"><b>" + minutes +":</b></div><div class=\"texts\">Mins</div></div> \
  <div class=\"seconds\"> \
  <div class=\"numbers\"><b>" + seconds +"</b></div><div class=\"texts\">Secs</div></div> \
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
        afterRender: function(){
          //playing the video
          $('video').get(0).play();
        }
  });
  var height= $(window).height()-$('#above-nav').height()-$('.navbar').height();
});