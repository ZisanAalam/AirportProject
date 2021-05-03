$('.ui.dropdown').dropdown({
    forceSelection : false
});

const inputLocation = document.getElementById('locations')
const locationPartDataBox = document.getElementById('location-part-data-box')
const locationPartText = document.getElementById('location-Part-Text')

inputLocation.addEventListener('change',e=>{
    const selectedLocation = e.target.value
    locationPartDataBox.innerHTML = ""
    locationPartText.textContent = "Choose a part"
    locationPartText.classList.add("default")

    $.ajax({
        url: `loactionpart-json/${selectedLocation}/`,
        method : "GET",
        success: function(response){
            console.log(response.data)
            const modelsData = response.data
            modelsData.map(item=>{
            const option = document.createElement('div')
            option.textContent = item.name
            option.setAttribute('class','item')
            option.setAttribute('data-value',item.name)
            locationPartDataBox.appendChild(option)
        })
        },
        error: function(error){
            console.log(error)
        }
    })
})

const makesInput = document.getElementById('makes')

const modeldatabox = document.getElementById('models-data-box')
const modelText = document.getElementById('model-text')
        
makesInput.addEventListener('change',e=>{
    const makeId = e.target.value
    modeldatabox.innerHTML = ""
    modelText.textContent = "Choose a model"
    modelText.classList.add("default")

    const url = "{% url 'get_model' %}"
        
    $.ajax({
    url : url,
    data : {"make_id":makeId},
    success: function(data){
        $("#models-data-box").html(data)
    }
    });
        
});