$('.ui.dropdown').dropdown({
    forceSelection : false
});

/* ---------------------------- Date Picker --------------------------------------------- */

$( function() {
    $( ".dateinput" ).datepicker({
        changeYear:true,
        changeMonth:true,
        dateFormat:'yy-mm-dd'
    });
} );

/* ------------------------------------Model Dropdown ------------------------------ */

const makesInput = document.getElementById('makes')

const modeldatabox = document.getElementById('models-data-box')
const modelText = document.getElementById('model-text')
        
makesInput.addEventListener('change',e=>{
    const selectedMake = e.target.value
    console.log(selectedMake)
    modeldatabox.innerHTML = ""
    modelText.textContent = "Choose a model"
    modelText.classList.add("default")
        
    $.ajax({
        url: `get_model/${selectedMake}/`,
        method : "GET",
        success: function(response){
            const modelsData = response.data
            modelsData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class','item')
            option.setAttribute('data-value',item.id)
            modeldatabox.appendChild(option)
        })
        },
        error: function(error){
            console.log(error)
        }
    })
        
});

/* ------------------------------------ Table data ------------------------------ */

const allinput=document.getElementsByClassName('myinput')
Array.from(allinput).forEach(item=>item.onchange=()=>{
    const makes=document.getElementById('nav-make').value
    const models=document.getElementById('nav-model').value
    const startDate = document.getElementById('nav-startdate').value
    const endDate=document.getElementById('nav-enddate').value
    $.ajax({
        url: 'get_data/',
        method : "GET",
        data:{'makes':makes,'models':models,'startdate':startDate,'enddate':endDate},
        success: function(response){
            if(response.data==="invalid"){
                document.getElementById('navtable-init-header').style.display="none"
                document.getElementById('navtable-init').style.display="none"
                document.getElementById('radarChart').style.display="none"
                document.getElementById('navtable-header').style.display="none"
                document.getElementById('navtable').style.display="none"
                document.getElementById('lineChart').style.display="none"
            }
            else{
                document.getElementById('radarChart').remove()
                document.getElementById('lineChart').remove()
                all_rows_dom=document.querySelectorAll('tr')
                all_headers_dom=document.querySelectorAll('thead')
                for (var i=0; i<all_rows_dom.length;i++){
                    if(all_rows_dom[i].parentElement !== all_headers_dom[0] && all_rows_dom[i].parentElement !== all_headers_dom[1]){
                        all_rows_dom[i].remove()
                    }
                }
                performance_table(response.navparams)
                radar_chart(response.navparams)
                reliability_table(response.data)
                line_chart(response.data)
                
                document.getElementById('navtable-init-header').style.display="block"
                document.getElementById('navtable-init').style.display="table"
                document.getElementById('radarChart').style.display="inline-block"
                document.getElementById('navtable-header').style.display="block"
                document.getElementById('navtable').style.display="table"
                document.getElementById('lineChart').style.display="inline-block"
            }
        },
        error: function(error){
            console.log(error)
        }
    })
        
});

const performance_table=(init_entries)=>{
    init_entries.forEach((item,index)=>{
        const each_row=document.createElement('tr')
        each_row.setAttribute('id',`navinit${index}`)
        const availability=document.createElement('td')
        availability.innerHTML=item.availability.toFixed(5)
        each_row.appendChild(availability)
        const reliability=document.createElement('td')
        reliability.innerHTML=item.reliability.toFixed(5)
        each_row.appendChild(reliability)
        const integrity=document.createElement('td')
        integrity.innerHTML=item.integrity.toFixed(5)
        each_row.appendChild(integrity)
        const continuity=document.createElement('td')
        continuity.innerHTML=item.continuity.toFixed(5)
        each_row.appendChild(continuity)
        document.getElementById('navtable-init-body').appendChild(each_row)

    })

}

const reliability_table=(all_entries)=>{
    all_entries.forEach((item,index)=>{
        const each_row=document.createElement('tr')
        each_row.setAttribute('id',`nav${index}`)
        const equipment=document.createElement('td')
        equipment.innerHTML=item.equipment
        each_row.appendChild(equipment)
        const faultlocation=document.createElement('td')
        faultlocation.innerHTML=item.location
        each_row.appendChild(faultlocation)
        const faultlocationpart=document.createElement('td')
        faultlocationpart.innerHTML=item.locationpart
        each_row.appendChild(faultlocationpart)
        const nooffailures=document.createElement('td')
        nooffailures.innerHTML=item.num_failures
        each_row.appendChild(nooffailures)
        const failureRate=document.createElement('td')
        failureRate.innerHTML=(item.failure_rate*1000000.0).toFixed(4)
        each_row.appendChild(failureRate)
        document.getElementById('navtable-body').appendChild(each_row)
    })

}

/* ------------------------------------ Graphical analysis ------------------------------ */

const radar_chart=(response_data)=>{
    
    
    data={
        labels: ['Availability','Reliability','Integrity','Continuity'],
        datasets: [{
            data: !response_data.length ? [] : [response_data[0].availability,response_data[0].reliability,response_data[0].integrity, response_data[0].continuity] ,
            fill: true,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            pointBackgroundColor: 'rgb(54, 162, 235)',
            pointRadius: 6,
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(54, 162, 235)'
        }]
    }
    
    const config = {
        type: 'radar',
        data: data,
        options: {
            plugins:{
                legend: {
                    display: false
                },
            },
            scales:{
                r:{
                    pointLabels:{
                        padding: 20,
                        font:{
                            weight: 'bold',
                            size: 15
                        }
                    }
                }
            },
            elements: {
                line: {
                    borderWidth: 3
                }
            },
      }
    }
    var chartDiv=document.getElementById('radar-chart-div');
    var ctx=document.createElement('canvas')
    ctx.setAttribute('id','radarChart')
    chartDiv.appendChild(ctx)
    var radarChart=new Chart(ctx,config)

    
}

const line_chart=(response_data)=>{
    
    var labels=response_data.map(item=>{
        return `${item.equipment}, ${item.locationpart}`
    })
    var dataset=response_data.map(item=>{
        return item.failure_rate*1000000.0.toFixed(4)
    })
    const data = {
        labels: labels,
        datasets: [{
          data: dataset,
          fill: false,
          backgroundColor: response_data.map(()=>'rgb(75, 192, 192)'),
          tension: 0.1
        }]
      };
    const config = {
        type: 'bar',
        data: data,
        options:{
            plugins:{
                legend: {
                    display: false
                },
            },
        }
      };
    var chartDiv=document.getElementById('line-chart-div');
    var ctx=document.createElement('canvas')
    ctx.setAttribute('id','lineChart')
    chartDiv.appendChild(ctx)
    var lineChart=new Chart(ctx,config)

    
}