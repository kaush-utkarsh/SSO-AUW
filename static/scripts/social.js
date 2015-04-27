// Linkedin JS
var fName="", lName="", email="", lin="";

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

function socialSubmit(payload)
{
    $.ajax(
        {
            url: "/socialSignIn",
            type: "POST",
            crossDomain: true,
            data: payload,
            datatype:'html',
            success: function (data) {
                if(data=="True")
                    window.location.assign('/signup_proceed')
                else
                    window.location.assign('/password_set')
            }
    });    
}

function liAuth()
{
   IN.User.authorize(function(){
        onSignIn();
   });
}
function onSignIn()
{
   IN.API.Profile("me").fields("id","first-name", "last-name", "email-address").result(function (data) {
        fName=data.values[0].firstName;
        lName=data.values[0].lastName;
        email=data.values[0].emailAddress;
        lin=data.values[0].id;
        var payload = {source:"lnkd_id",name:fName+" "+lName,email:email,ip:ip,geo:"("+lat+","+lng+")",id:lin}
        socialSubmit(payload);
    }).error(function (data) {
        console.log(data);
    });
}


// Facebook JS

function statusChangeCallback(response) {

    if (response.status === 'connected') {
        FB.api('/me', function(fbResponse) {
            var payload = {source:"fb_id",name:fbResponse.first_name+" "+fbResponse.last_name,email:fbResponse.email,ip:ip,geo:"("+lat+","+lng+")",id:fbResponse.id}
            socialSubmit(payload)
        })
    };      
}

function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);

    });
}


