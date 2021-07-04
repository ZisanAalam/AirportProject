$('.ui.dropdown').dropdown({
    forceSelection : false
});

/* ----------------------------- Form Validation ------------------------------- */
function clearError(){
    document.getElementById('runway-error').innerHTML =""
    document.getElementById('equipment-error').innerHTML =""
    document.getElementById('make-error').innerHTML =""
    document.getElementById('model-error').innerHTML =""
    document.getElementById('location-error').innerHTML =""
    document.getElementById('module-error').innerHTML =""
    document.getElementById('sdate-error').innerHTML =""
    document.getElementById('edate-error').innerHTML =""
    document.getElementById('stime-error').innerHTML =""
    document.getElementById('etime-error').innerHTML =""
}


const runway_element=document.getElementById('runway')
const equipment_element=document.getElementById('equipment')
const make_element=document.getElementById('make')
const model_element=document.getElementById('model')
const location_element=document.getElementById('location')
const module_element=document.getElementById('location-part')
const sdate_element = document.getElementById('sdate')
const edate_element = document.getElementById('edate')
const stime_element = document.getElementById('stime')
const etime_element = document.getElementById('etime')
runway_element.onchange=clearError
equipment_element.onchange=clearError
make_element.onchange=clearError
model_element.onchange=clearError
location_element.onchange=clearError
sdate_element.onchange=clearError
edate_element.onchange=clearError
stime_element.onchange=clearError
etime_element.onchange=clearError


function checkInputs(event){
    let dateregex=/^\d{4}[\/\-](0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])$/
    let timeregex=/^(([0-1]\d{1})|(2[0-3])):[0-5]\d{1}:[0-5]\d{1}$/
    const sdate = sdate_element.value
    const edate = edate_element.value
    const stime = stime_element.value
    const etime = etime_element.value
    const runway=runway_element.value
    const equipment=equipment_element.value
    const make=make_element.value
    const model=model_element.value
    const location=location_element.value
    const module=module_element.value
    var flag=false

    let dateObj = new Date();
    let month = String(dateObj.getMonth() + 1).padStart(2, '0');
    let day = String(dateObj.getDate()).padStart(2, '0');
    let year = dateObj.getFullYear();
    let cdate = year + '-' + month + '-' + day;

    if(runway==""){
        document.getElementById('runway-error').innerHTML ="Please select a runway."
        flag=true
    }
    if(equipment==""){
        document.getElementById('equipment-error').innerHTML ="Please select an equipment."
        flag=true
    }
    if(make==""){
        document.getElementById('make-error').innerHTML ="Please select a maker."
        flag=true
    }
    if(model==""){
        document.getElementById('model-error').innerHTML ="Please select a model."
        flag=true
    }
    if(location==""){
        document.getElementById('location-error').innerHTML ="Please select a fault location."
        flag=true
    }
    if(module==""){
        document.getElementById('module-error').innerHTML ="Please select a fault module."
        flag=true
    }
    if(!dateregex.test(sdate)){
        document.getElementById('sdate-error').innerHTML ="Please enter start date"
        flag=true
    }
    if(!dateregex.test(edate)){
        document.getElementById('edate-error').innerHTML ="Please enter end date"
        flag=true
    } 
    if(!timeregex.test(stime)){
        document.getElementById('stime-error').innerHTML ="Please enter start time"
        flag=true
    } 
    if(!timeregex.test(etime)){
        document.getElementById('etime-error').innerHTML ="Please enter end time"
        flag=true
    }
    if(sdate>edate){
        document.getElementById('date-error').innerHTML ="Invalid date entry. Start date cannot be greated than end date"
        flag=true 
    }
    if(edate<sdate){
        document.getElementById('date-error').innerHTML ="Invalid date entry. End date cannot be smaller than Start date"
        flag=true 
    }
    if(sdate>cdate || edate>cdate){
        document.getElementById('date-error').innerHTML ="Invalid date entry. Selected date is greater than current date"
        flag=true 
    }
    if(flag){
        event.preventDefault()
        flag=false
    }  
}
const form = document.getElementById('form')
form.onsubmit=checkInputs

/* ----------------------- For Equipment dropdown ----------------------------------*/
const inputRunway = document.getElementById('runways')
const equipmentDataBox = document.getElementById('equipment-data-box')
const equipmentText = document.getElementById('equipment-text')

inputRunway.addEventListener('change',e=>{
    const selectedRunway = e.target.value
    equipmentDataBox.innerHTML = ""
    equipmentText.textContent = "Choose a Insturment"
    equipmentText.classList.add("default")

    $.ajax({
        url: `equiment/${selectedRunway}/`,
        method : "GET",
        success: function(response){
            const modelsData = response.data
            modelsData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.equipment
            option.setAttribute('class','item')
            option.setAttribute('data-value',item.id)
            
            equipmentDataBox.appendChild(option)
            console.log(equipmentDataBox)
        })
        },
        error: function(error){
            console.log(error)
        }
    })
})


/* ---------------------- For Fault Location Part dropdwon----------------------------*/

const inputLocation = document.getElementById('locations')
const locationPartDataBox = document.getElementById('location-part-data-box')
const locationPartText = document.getElementById('location-Part-Text')

inputLocation.addEventListener('change',e=>{
    const selectedLocation = e.target.value
    locationPartDataBox.innerHTML = ""
    locationPartText.textContent = "Choose a part"
    locationPartText.classList.add("default")

    $.ajax({
        url: `loactionpart/${selectedLocation}/`,
        method : "GET",
        success: function(response){
            const modelsData = response.data
            modelsData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class','item')
            option.setAttribute('data-value',item.id)
            locationPartDataBox.appendChild(option)
        })
        },
        error: function(error){
            console.log(error)
        }
    })
})

/* ------------------------------------Model Dropdown ------------------------------ */

const makesInput = document.getElementById('makes')

const modeldatabox = document.getElementById('models-data-box')
const modelText = document.getElementById('model-text')
        
makesInput.addEventListener('change',e=>{
    const selectedMake = e.target.value
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

/* ---------------------------- Date Picker --------------------------------------------- */

$( function() {
    $( ".dateinput" ).datepicker({
        changeYear:true,
        changeMonth:true,
        dateFormat:'yy-mm-dd'
    });
} );

/* --------------------------- Time Picker --------------------------*/
$('.clockpicker').clockpicker({
    placement: 'top',
    align: 'left',
    donetext: 'Done'
});

