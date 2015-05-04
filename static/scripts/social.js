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

// Linkedin JS

function liAuth()
{
   IN.User.authorize(function(){
        onSignIn();
   });
}
function onSignIn()
{
   IN.API.Profile("me").fields("id","first-name", "last-name", "email-address","location").result(function (data) {
        fName=data.values[0].firstName;
        lName=data.values[0].lastName;
        email=data.values[0].emailAddress;
        lin=data.values[0].id;
        try
        {
            var location=data.values[0].location.name;
        }
        catch (err)
        {
            var location=""
        }
        IN.API.Profile("me").result(function (data) {
            try
            {
                var picture=data.values[0].pictureUrl;
            }
            catch (err)
            {
                var picture=""
            }
            
            var payload = {source:"lnkd_id",name:fName+" "+lName,email:email,ip:ip,geo:"("+lat+","+lng+")",id:lin,referer:$('input[id="referer"]').val(),picture:picture,location:location}
            socialSubmit(payload);

        })

    }).error(function (data) {
        console.log(data);
    });
}


// Facebook JS

function statusChangeCallback(response) {

    if (response.status === 'connected') {
        FB.api('/me', function(fbResponse) {
            
            var source="fb_id"
            var name=fbResponse.first_name+" "+fbResponse.last_name
            var email=fbResponse.email
            var geo="("+lat+","+lng+")"
            var id=fbResponse.id
            var referer=$('input[id="referer"]').val()

            FB.api('/me?fields=name,picture{url},location', function(response) {
            
                try
                    {
                        var picture=response.picture.data.url
                    }
                catch(e)
                    {
                        var picture=""
                    }
                try
                    {
                        var location=response.location.name
                    }
                catch(e)
                    {
                        var location=""
                    }

                var payload = {source:source,name:name,email:email,ip:ip,geo:geo,id:id,referer:referer,picture:picture,location:location}
    
            socialSubmit(payload)
        })
        })
    };      
}

function checkLoginState() {
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);

    });
}

// Google JS

function onGSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    if (profile.getImageUrl() === undefined || profile.getImageUrl() === null) {
    var pictureUrl=""
    }
    else
    {
       var pictureUrl = profile.getImageUrl() 
    }
    var payload = {source:"google_id",name:profile.getName(),email:profile.getEmail(),ip:ip,geo:"("+lat+","+lng+")",id:profile.getId(),referer:$('input[id="referer"]').val(),picture:pictureUrl,location:""}
    socialSubmit(payload)
}