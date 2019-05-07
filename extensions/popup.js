$(document).ready(function(){
    // variables
    var inputs;
    var btn;
    var image;
    // start listener
    chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
        if (message.msg == "picked") {
            inputs.val(message.data);
            btn.css("background-color", "#222222");
            // send message to contet script for deactivating picker and clicker
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {action: "finishedPicking"}, function(response) {
                });
            });
        } else if (message.msg == "imagepicked") {
            image.css("backgound-color", "none");
            image.attr('src', message.data);
            // send message to contet script for deactivating image picker and image clicker
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {action: "finishedImagePicking"}, function(response) {
                });
            });
        }
    });

    //back button click
    $(".backspan").click(function(){
        // send message to content script for back activity
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: "back"}, function(response) {
            });
          });
    });

    // clear form
    $("#clear").click(function(){
        // take all the input and clear it
        $("#productname").val('');
        $("#productsku").val('');
        $("#category").val('');
        $("#productdesc").val('');
        $("#productdim").val('');
        $("#productprice").val('');
        // clear out the img box
        var _trashbtn = $(document).find('.buttontrash');
        $.each(_trashbtn, function () {
            $(this).parent().remove();
        });
        // add a single image box
        $("#imageAR").append(`<div style="display: flex; align-items: center; width: 80px;">
        <img src="img_pick.png" width="80" height="80" class="imagepicker" /><button class="buttontrash">&#10008;</button>
    </div>`)    

    });

    // add image
    $("#addimage").click(function(){
        $("#imageAR").append(`<div style="display: flex; align-items: center; width: 80px;">
        <img src="img_pick.png" width="80" height="80" class="imagepicker"/><button class="buttontrash">&#10008;</button>
    </div>`)
    });

    // delete image
    $(document).on('click', '.buttontrash', function() {
        $(this).parent().remove();
    });

    // highlighter
    $(document).on('click', '.pickbutton', function() {
        btn = $(this)
        // check if its already clicked
        if (btn.css("background-color") == "#222222") {
            return false;
        } else {
            // get the input field
            var p = $(this).parent().parent();
            inputs = p.find('input');
            btn.css("background-color", "#ffffff");
            // send message to contet script for activating mouseover and click 
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {action: "picker"}, function(response) {
                });
            });
        }
        
    });

    // image picker click
    $(document).on('click', '.imagepicker', function() {
        image = $(this);
        image.css("background-color", "#ffffff");
        // send message to contet script for activating image mouseover and image click
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: "imagepicker"}, function(response) {
            });
        });
        
    });

    // upload
    $(".upload").click(function () {
        chrome.tabs.getSelected(null, function(tab) {
            // take everything from field
            var jsonObject = new Object();
            var tabUrl = tab.url;
            jsonObject.SiteId = 2;
            jsonObject.URL = tabUrl;
            jsonObject.ItemName = $("#productname").val();
            jsonObject.SKU = $("#productsku").val();
            jsonObject.Category = $("#category").val();
            jsonObject.ItemDescription = $("#productdesc").val();
            jsonObject.Dimension = $("#productdim").val();
            jsonObject.NET = $("#productprice").val();
            var photos = [];
            var _capturedimage = $(document).find('.imagepicker');
            $.each(_capturedimage, function() {
                var source = $(this).attr('src');
                photos.push(source);
            });
            // take images
            jsonObject.Photo = photos;
            // process as single json
            // upload
            alert(JSON.stringify(jsonObject));
        });
        
    });
});