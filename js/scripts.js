$(document).ready(function() {

});

var callapi = function() {
    $.get("https://ec2-35-163-195-254.us-west-2.compute.amazonaws.com:8888/api/")
        .done(function(res) {
            $("#response").append("<p style='color:green;'>" + (new Date()) + " success</p>");
        })
        .fail(function(res) {
            $("#response").append(("<p style='color:red;'>" + new Date()) + " failed</p>");
        })
}