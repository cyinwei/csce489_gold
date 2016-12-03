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

    req += ("&datetime=" + unixtime)

    console.log( req );

    $.post("https://ec2-35-163-195-254.us-west-2.compute.amazonaws.com/api/analyze", data=req)
        .done(function(res) {
            $("#res").css({'color': 'green'});
        })
        .fail(function(res) {
            $("#res").css({'color': 'red'});
        })
        .always(function(res) {
            $("#res").css({"display": "block"})

            $("#ressubreddit").html(res['subreddit']);
            $("#resdatetime").html(new Date(res['datetime'] * 1000));
            $("#rescomment").html(res['comment']);

            $("#response").html(JSON.stringify(res))
            console.log(res)
        });

});