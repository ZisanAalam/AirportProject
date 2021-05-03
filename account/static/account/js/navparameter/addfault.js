$('.ui.dropdown').dropdown({
    forceSelection : false
});

const inputLocation = document.getElementById('locations')
const locationPartDataBox = document.getElementById('location-part-data-box')
const locationPartText = document.getElementById('location-Part-Text')

inputLocation.addEventListener('change',e=>{
    console.log(e.target.value)
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