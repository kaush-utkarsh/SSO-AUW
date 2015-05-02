$('form[id="admin_signin_form"]').submit(function(event)
{

    event.preventDefault();
    var payload={email:$('input[name="email"]').val(),psword:$('input[name="password"]').val()}
    $.ajax(
        {
            url: '/admin_login',
            type: "POST",
            crossDomain: true,
            data: payload,
            datatype:'html',
            success: function (data) {
                // console.log(data)
                if(data=="True")
                    window.location.assign('/admin')
                else
                    alert('Please check the credentials');
            }
    });
})