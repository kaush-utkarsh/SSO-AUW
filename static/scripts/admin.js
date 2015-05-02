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

function makePieChart(div,data)
{
    var plotObj = $.plot($(div), data, {
        series: {
            pie: {
                show: true
            }
        },
        grid: {
            hoverable: true
        },
        tooltip: true,
        tooltipOpts: {
            content: "%p.0%, %s", // show percentages, rounding to 2 decimal places
            shifts: {
                x: 20,
                y: 0
            },
            defaultTheme: false
        }
    });

};
