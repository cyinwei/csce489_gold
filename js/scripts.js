$(document).ready(function() {

});

var callapi = function() {
    $.get("https://ec2-35-163-195-254.us-west-2.compute.amazonaws.com/api/")
        .done(function(res) {
            $("#response").append("<p style='color:green;'>" + (new Date()) + " success</p>");
        })
        .fail(function(res) {
            $("#response").append(("<p style='color:red;'>" + new Date()) + " failed</p>");
        })
}

$( "form" ).on( "submit", function( event ) {
    event.preventDefault();

    var req = $( this ).serialize()
    var unixtime = Date.parse(new Date())/1000

    // req += ("&datetime=" + unixtime)
    // // TODO: Read in actual flair
    // req += ("&flair=" + 'testflair')

    console.log( req );

    $.post("https://csce489.jsmoorman.com/api/analyze", data=req)
        .done(function(res) {
            if(res['prediction'] === 'True') {
                $("#resgilded").html("Your comment has a chance of being gilded!").css({'color': 'green'});
            }
            else {
                $("#resgilded").html("Your comment does not have a chance of being gilded.").css({'color': 'red'});
            }

            // $("#res").css({'color': 'green'});
            // $("#res").css({"display": "block"})
            // $("#ressubreddit").html(res['subreddit']);
            // $("#resdatetime").html(new Date(res['datetime'] * 1000));
            // $("#rescomment").html(res['comment']);
        })
        .fail(function(res) {
            // $("#res").css({'color': 'red'});
            // $("#res").css({"display": "none"})
        })
        .always(function(res) {
            // $("#response").html(JSON.stringify(res))
            console.log(res)
        });

});