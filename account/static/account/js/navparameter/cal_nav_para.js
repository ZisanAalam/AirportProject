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