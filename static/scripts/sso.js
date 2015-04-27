$(function() 
{
	$('a[rel*=popupModal]').popupModal({closeButton: ".close" });  /*top: 20 ,*/
});

$(document).ready(function()
{
	$('a[rel*=popupModal]').click()
});

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

var lat=0, lng =0, ip="0.0.0.0";

function showPosition(position) {
    // x.innerHTML = "Latitude: " + position.coords;  
    lat=position.coords.latitude;
    lng=position.coords.longitude;
}

function myIP() {
    if (window.XMLHttpRequest) xmlhttp = new XMLHttpRequest();
    else xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");

    xmlhttp.open("GET","http://api.hostip.info/get_html.php",false);
    xmlhttp.send();

    hostipInfo = xmlhttp.responseText.split("\n");

    for (i=0; hostipInfo.length >= i; i++) {
        ipAddress = hostipInfo[i].split(":");
        if ( ipAddress[0] == "IP" ) return ipAddress[1];
    }

    return "0.0.0.0";
}

ip=myIP();

getLocation();

function signupAjax(payload)
{
	$.ajax(
        {
            url: "/signupAPI",
            type: "POST",
            crossDomain: true,
            data: payload,
            datatype:'html',
            success: function (data) {
                if(data=="True")
                    window.location.assign('/signup_proceed')
                else
                    console.log(data)
            }
    });
}


$('form[id="signUp"]').submit(function(event)
{
    event.preventDefault();
    var ip_Add=myIP()
    var payload={source:"auw",name:$('input[name="name"]').val(),city:$('input[name="city"]').val(),email:$('input[name="email"]').val(),psword:$('input[name="pwd"]').val(),ip:ip,geo:"("+lat+","+lng+")"}
    signupAjax(payload);
})

$('form[id="SignIn"]').submit(function(event)
{

    event.preventDefault();
    var ip_Add=myIP()
    var payload={name:$('input[name="name"]').val(),psword:$('input[name="pwd"]').val(),ip:ip,geo:"("+lat+","+lng+")"}
    signupAjax(payload);

})


$('form[id="setPwd"]').submit(function(event)
{

    event.preventDefault();
    var ip_Add=myIP()
    var payload={psword:$('input[name="pwd"]').val()}
	$.ajax(
        {
            url: "/setPwdAPI",
            type: "POST",
            crossDomain: true,
            data: payload,
            datatype:'html',
            success: function (data) {
                if(data=="True")
                    window.location.assign('/signup_proceed')
                else
                    console.log(data)
            }
    });
})