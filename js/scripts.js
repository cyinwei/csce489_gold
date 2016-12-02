$(document).ready(function() {

});

var callapi = function() {
    $.get("https://ec2-35-162-69-135.us-west-2.compute.amazonaws.com:8888/api/")
        .done(function(res) {
            $("#response").append((new Date()) + " " + res).css({color: "green"});
        })
        .fail(function(res) {
            $("#response").append((new Date()) + " failed").css({color: "red"});
        })
        .always(function() {
            $("#response").append("</br>");
        });

}