var pageData;

// var d = new Date();

// var currDate = d.getDate();
// var currMonth = d.getMonth();
// var currYear = d.getFullYear();

// var dateStr = currYear + "-" + currMonth + "-" + currDate;
$('.datepicker').datepicker({
    format: 'yyyy-mm-dd',
    todayHighlight:true,
    autoclose:true,
    endDate: new Date(),
    todayBtn:true
})

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
            content: "%p.0% (%y.0), %s", // show percentages, rounding to 2 decimal places
            shifts: {
                x: 20,
                y: 0
            },
            defaultTheme: false
        }
    });

};


function plotLineGraph(div,datum,labl) {

    var options = {
        series: {
            lines: {
                show: true
            },
            points: {
                show: true
            }
        },
        grid: {
            hoverable: true //IMPORTANT! this is needed for tooltip to work
        },
        yaxis: {
            min: 0
        },
        tooltip: true
        
    };

    var plotObj = $.plot($(div), [{
            data: datum,
            label: labl
        }],
    options);
}


function pageLoad(data)
{
    pageData=JSON.parse(data)
    console.log(pageData)
    $.each(pageData.siblings,function(i,item){
        $('select[id="siblings"]').append("<option value='"+item+"'>"+item+"</option>")
    })
    updateOverview(pageData.sibling_data)
}

function updateOverview(data)
{

    makePieChart("#Devices",data.devices)
    makePieChart("#Cities",data.cities)
    makePieChart("#day_line",data.day_time)
    
}