$(document).ready(function() {

});

var createTable = function(obj){
    keys = [];
    values = [];
    $.each(obj, function(key, val){
        console.log(key + ': ' + val);
        keys.push(key);
        values.push(val);
    });
    th = '<thead><tr>'
    tb = '<tbody><tr>'
    keys.forEach(function(key) {
        th = th.concat('<th>' + key + '</th>');
    });
    th = th.concat('</tr></thead>');
    values.forEach(function(value) {
        tb = tb.concat('<td>' + value + '</td>');
    });
    tb = tb.concat('</tr></tbody>');
    return ("<table class='table'>" + th + tb + "</table>");
}

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

    console.log( req );

    $.post("https://csce489.jsmoorman.com/api/analyze", data=req)
        .done(function(res) {
            // Give prediction
            if(res['prediction'] === 'True') {
                $("#resgilded").html("Yes!").css({'color': 'green'});
            }
            else {
                $("#resgilded").html("No.").css({'color': 'red'});
            }
            // Remove prediction for table creation
            delete res['prediction'];
            // Create table html string
            var table = createTable(res);
            // Table of features in page
            $('#fintro').html('Here are the relevant features of your comment:');
            $('#featureTable').html(table);
        })
        .fail(function(res) {
            $("#fintro").html("Error with request or server. Please try again.").css({'color': 'red'});
        })
        .always(function(res) {
            console.log(res)
        });

});