// console.log("Hello Kushal, you are at home.js. Hello again. Once Again. 3 more time");
// console.log($);


let k = 1;
let x = 0;


function getBotResponse(textInput) {
  html += `<div class="media">
    <div class="media-body">
      <h5 style="text-align:right" class="mt-0 mb-1">User</h5>
      <p class = "userText" style="text-align:right; margin-left: 400px; font-style: oblique; font-weight: bold; font-size: 17px;"><span>${textInput}</span></p>
    </div>
    <img src="static/SVG/people-circle.svg" height = "40px" width = "40px" class="align-self-center ml-3" style="margin-right: 10px;" alt="User">
  </div>`
  var chatBox = $("#chatBox")
  chatBox.html(html)

  // console.log("Input Box Cleared")
  $("#textInput").val("")

  document
    .getElementById("formInput")
    .scrollIntoView({ block: "start", behavior: "smooth" });
  
  $.get("/get", { msg: textInput }).done(function (data) {
    // console.log("Inside function data")
    html += `<div class="media">
        <img src="static/SVG/doctor.png" height = "40px" width = "40px" class="align-self-center mr-3" style="margin-left: 10px;" alt="DocBot">
        <div class="media-body">
          <h5 class="mt-0">DocBot</h5>
          <p class = "botText" style="margin-right: 400px; font-style: oblique; font-weight: bold; font-size: 17px;"><span>` + data + `</span></p>
        </div>
      </div>`
    chatBox.html(html)
    document
      .getElementById("formInput")
      .scrollIntoView({ block: "start", behavior: "smooth" });

    if ('speechSynthesis' in window) with (speechSynthesis) {
      botText = document.getElementsByClassName("botText");
      // console.log(botText);
 

      utterance = new SpeechSynthesisUtterance(botText[k].textContent);
      utterance.voice = getVoices()[0];
     
      utterance.volume = 1
      utterance.rate = 1
      utterance.pitch = 1
      k = k + 1;
      // console.log("Speech Function Activated for", utterance.text);
      speak(utterance);
      setTimeout(() => {
        if (utterance.text == "Good bye sir. It was nice talking to you. Have a nice day !"){
          // console.log("Inside break function")
          x = 0;
          html = ` <div class="media">
          <img src="static/SVG/doctor.png" height = "40px" width = "40px" class="align-self-center mr-3" style="margin-left: 10px;" alt="DocBot">
          <div class="media-body">
            <h5 class="mt-0">DocBot</h5>
            <p class = "botText" style="margin-right: 400px; font-style: oblique; font-weight: bold; font-size: 17px;"><span>Hi! I'm Candice your personal ChatBot</span></p>
          </div>
          </div>`
          chatBox.html(html)
          $(".collapse").collapse("hide")
          $("#collapse").html("Click here to talk with your personal DocBot")
          }
      }, 6000);
    }
  })  
}


$("#collapse").click(function(e){
  e.preventDefault()
  $("#collapse").html("I can tell you about signs, symptoms, risk-factors, diagnosis and treatment of CKD")
})


$('.popover-dismiss').popover({
  trigger: 'focus'
})


$(function () {
  $('[data-toggle="popover"]').popover()
})

let html = ` <div class="media">
<img src="static/SVG/doctor.png" height = "40px" width = "40px" class="align-self-center mr-3" style="margin-left: 10px;" alt="DocBot">
<div class="media-body">
  <h5 class="mt-0">DocBot</h5>
  <p class = "botText" style="margin-right: 400px; font-style: oblique; font-weight: bold; font-size: 17px;"><span>Hi! I'm Candice your personal ChatBot</span></p>
</div>
</div>`


$("#userInput").click(function (e) {

  e.preventDefault()
  // console.log("submit button clicked")
  x = x + 1;
  var textInput = $("#textInput").val();
  // console.log("Got textInput id")
  // console.log(textInput)
  getBotResponse(textInput)
})


$("#micBtn").click(function (e) {
  e.preventDefault()
  // console.log("Mic Clicked")
  $("#micBtn").html(`<img alt="Start" id="start_img" src="static/GIF/mic-animate.gif" height="20px" width="20px" >`)
  // console.log("Animation On")


  var SpeechRecognition = window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
 
  recognition.continuous = false;
  recognition.lang = 'en-IN';
  recognition.start();
  recognition.onresult = function (event) {
  // console.log(event.results[0][0].transcript)
   

    var chatBox = $("#chatBox")
    chatBox.html(html)
    recognition.stop()
    $("#micBtn").html(`<img alt="Start" id="start_img" src="static/SVG/mic-fill.svg" height="20px" width="20px" >`)
    getBotResponse(event.results[0][0].transcript)
  }
})