$('.ui.dropdown').dropdown({
    forceSelection : false
});


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

/* ----------------------------- Form Validation ------------------------------- */

const form = document.getElementById('form')
const sdate = document.getElementById('sdate')
form.addEventListener('submit',(e) =>{
    e.preventDefault()
    checkInputs()
});

function checkInputs(){
    var sdate = sdate.value();
    if(sdate==''){
        document.getElementById('sdate-error').innerHTML ="Please enter start date"
    }
}