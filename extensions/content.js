// get message from background js
chrome.runtime.onMessage.addListener(function(msg, sender){
    if(msg == "toggle"){
        $.fn.toggle();
    }
})

// Side panel iframe injection to the dom
var iframe = document.createElement('iframe');
iframe.setAttribute('class', 'vendacart')
iframe.style.background = "white";
iframe.style.height = "100%";
iframe.style.width = "0%";
iframe.style.position = "fixed";
iframe.style.top = "0px";
iframe.style.right = "0px";
iframe.style.zIndex = "9000000000000000000";
iframe.frameBorder = "none"; 
iframe.src = chrome.extension.getURL("popup.html")

document.body.appendChild(iframe);

// back or close
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    var prev;
    var pickerhighlightlistener;
    var imagepickerhighlightlistener;
    if (request.action == "back"){
      $.fn.expand();
      return false;
    } else if (request.action == "picker") {
      onOffSwitch = true;
      // mouseover on
      pickerhighlightlistener = document.addEventListener('mouseover', highlighthandler);
      // click listenong on
      document.addEventListener("click", clickhandler);
    
    } else if (request.action == "finishedPicking") {
      onOffSwitch = false;
      // mouseover off
      document.removeEventListener('mouseover', pickerhighlightlistener);
      // click listenong off
      document.removeEventListener("click", clickhandler);
    } else if (request.action == "imagepicker") {
      onOffSwitch = true;
      // mouseover on
      imagepickerhighlightlistener = document.addEventListener('mouseover', imagehighlighthandler);
      // click listenong on
      document.addEventListener("click", imageclickhandler, true);
    } else if (request.action == "finishedImagePicking") {
      onOffSwitch = false;
      document.removeEventListener('mouseover', imagepickerhighlightlistener);
      // click listenong on
      document.removeEventListener("click", imageclickhandler, true);
    }
    // simple highlight all
    function highlighthandler(event) {
      if (onOffSwitch) {
        if (event.target === document.body || (prev && prev === event.target)) {
          return;
        }
        if (prev) {
          prev.className = prev.className.replace(/ \bhighlight\b/, '');
          prev = undefined;
        }
        if (event.target) {
          prev = event.target;
          prev.className += " highlight";
        } 
      } else {
        if (prev) {
          prev.className = prev.className.replace(/ \bhighlight\b/, '');
          prev = undefined;
        }
        // alert("its off");
      }
    }
    // only image highlight
    function imagehighlighthandler(event) {
      if (onOffSwitch) {
        if (event.target === document.body || (prev && prev === event.target)) {
          return;
        }
        if (prev) {
          prev.className = prev.className.replace(/ \bimagehighlight\b/, '');
          prev = undefined;
        }
        if (event.target && event.target.tagName.toUpperCase() == "IMG") {
          prev = event.target;
          prev.className += " imagehighlight";
        }
      } else {
        if (prev) {
          prev.className = prev.className.replace(/ \bimagehighlight\b/, '');
          prev = undefined;
        }
      }
      
    }
  });


// click handler
function clickhandler(event) {
  event.preventDefault();
  event.stopPropagation();
  var text = $(event.target).text();
  chrome.runtime.sendMessage({msg: "picked", data: text}, function (response) {
    console.log(response);
  });
}

function imageclickhandler(event) {
  event.preventDefault();
  event.stopPropagation();
  if (event.target.tagName.toUpperCase() == 'IMG') {
    // document.getElementById('imgSrc').value = event.target.src;
    var source = event.target.src;
    chrome.runtime.sendMessage({msg: "imagepicked", data: source}, function (response) {
      console.log(response);
    });
  } 
  
}

// toggle side panel on or off
$.fn.toggle = function(){
  var html;
  if (document.documentElement) {
    html = $(document.documentElement); //just drop $ wrapper if no jQuery
  } else if (document.getElementsByTagName('html') && document.getElementsByTagName('html')[0]) {
    html = $(document.getElementsByTagName('html')[0]);
  } else if ($('html').length > -1) {//drop this branch if no jQuery
    html = $('html');
  } else {
    alert('no html tag retrieved...!');
    throw 'no html tag retrieved son.';
  }
  //position
  if (html.css('position') === 'static') { //or //or getComputedStyle(html).position
    html.css('position', 'relative');//or use .style or setAttribute
  }
  $.fn.expand();
};

// expand or close
$.fn.expand = function(){
  if(iframe.style.width == "0%"){
    iframe.style.width="25%";
    document.documentElement.style.width = '75%';
  } else{
    iframe.style.width="0%";
    document.documentElement.style.width = '100%';
  }
};
