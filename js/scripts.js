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

    var data = $( this ).serialize()
    var unixtime = Date.parse(new Date())/1000

    data += ("&datetime=" + unixtime)

    console.log( data );

    callapi()
});