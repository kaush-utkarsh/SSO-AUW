var pageData;

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


function barGraph(div,data)
{

    $.plot(div, [ data ], {
        series: {
            bars: {
                show: true,
                barWidth: 0.2,
                align: "center"
            }
        },
        xaxis: {
            mode: "categories",
            tickLength: 0
        }
    });

}


function overViewPageLoad(data)
{
    pageData=JSON.parse(data)

    $.each(pageData.siblings,function(i,item){
        $('select[id="siblings"]').append("<option value='"+item+"'>"+item+"</option>")
    })

    updateOverview(pageData.sibling_data)
}

function cityPageLoad(data)
{
    pageData=JSON.parse(data)

    $.each(pageData.siblings,function(i,item){
        $('select[id="siblings"]').append("<option value='"+item+"'>"+item+"</option>")
    })

    updateCityPage(pageData.sibling_data)
}
function sessionsLoad(data)
{
    pageData=JSON.parse(data)

    $.each(pageData.siblings,function(i,item){
        $('select[id="siblings"]').append("<option value='"+item+"'>"+item+"</option>")
    })

    updateSessionPage(pageData.sibling_data)
}

function overDaysLoad(data)
{
    pageData=JSON.parse(data)

    $.each(pageData.siblings,function(i,item){
        $('select[id="siblings"]').append("<option value='"+item+"'>"+item+"</option>")
    })

    updateDaysPage(pageData.sibling_data)
}



function updateOverview(data)
{

    $('#Devices').empty()
    $('#Cities').empty()
    $('#day_line').empty()


    makePieChart("#Devices",data.devices)
    makePieChart("#Cities",data.cities)
    makePieChart("#day_line",data.day_time)
    
}

function updateDaysPage(data)
{

    // console.log(data)
    // barGraph("#days_graph",data)
    $('#days_graph').empty()
    makePieChart("#days_graph",data)
    
}

function updateCityPage(data)
{
$('tbody[id="cityTable"]').empty()
$.each(data,function(i,item){
    $('tbody[id="cityTable"]').append("<tr><td>"+item.city+"</td><td>"+item.state+"</td><td>"+item.country+"</td><td>"+item.morning+"</td><td>"+item.office+"</td><td>"+item.evening+"</td><td>"+item.total+"</td></tr>")
})
    
}

function updateSessionPage(data)
{
$('tbody[id="sessionTab"]').empty()
$.each(data,function(i,item){
    $('tbody[id="sessionTab"]').append("<tr><td>"+item.ipAdd+"</td><td>"+item.referer+"</td><td>"+item.session_start+"</td><td>"+item.os+"</td><td>"+item.browser+"</td><td>"+item.device_type+"</td><td>"+item.city+"</td><td>"+item.state+"</td><td>"+item.country+"</td></tr>")
})
    
}

function pageUpdate()
{
    var dt=$('#datepicker').val()
    var sibl=$('#siblings').val()    
    var headr= $('#siblings').parents('.container-fluid').find('h1:eq(0)').html()
    var payload={date:dt,referer:sibl,page:headr}
    $.ajax(
        {
            url: '/admin_page_fetch',
            type: "POST",
            crossDomain: true,
            data: payload,
            datatype:'html',
            success: function (data) {
                var jsonD = JSON.parse(data)
                if(headr=="Last 100 sessions")
                    updateSessionPage(jsonD.sibling_data)
                if(headr=="Hits per Days")
                    updateCityPage(jsonD.sibling_data)
                if(headr=="Hits per City")
                    updateCityPage(jsonD.sibling_data)
                if(headr=="Overview")
                    updateOverview(jsonD.sibling_data)
            }
    });

}

$('#datepicker').change(function(event){
    pageUpdate();
});
$('#siblings').change(function(event){
   pageUpdate(); 
});
