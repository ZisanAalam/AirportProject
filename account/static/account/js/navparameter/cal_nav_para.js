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
            console.log(response)
            if(response.data==="invalid"){
                document.getElementById('navtable-init-header').style.display="none"
                document.getElementById('navtable-init').style.display="none"
                document.getElementById('navtable-header').style.display="none"
                document.getElementById('navtable').style.display="none"
            }
            else{
                all_rows_dom=document.querySelectorAll('tr')
                all_headers_dom=document.querySelectorAll('thead')
                for (var i=0; i<all_rows_dom.length;i++){
                    if(all_rows_dom[i].parentElement !== all_headers_dom[0] && all_rows_dom[i].parentElement !== all_headers_dom[1]){
                        all_rows_dom[i].remove()
                    }
                }
                init_entries=response.navparams
                init_entries.forEach((item,index)=>{
                    const each_row=document.createElement('tr')
                    each_row.setAttribute('id',`navinit${index}`)
                    const equipment=document.createElement('td')
                    equipment.innerHTML=item.equipment
                    each_row.appendChild(equipment)
                    const faultlocation=document.createElement('td')
                    faultlocation.innerHTML=item.location
                    each_row.appendChild(faultlocation)
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
                all_entries=response.data
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
                document.getElementById('navtable-init-header').style.display="block"
                document.getElementById('navtable-init').style.display="table"
                document.getElementById('navtable-header').style.display="block"
                document.getElementById('navtable').style.display="table"
            }
        },
        error: function(error){
            console.log(error)
        }
    })
        
});

