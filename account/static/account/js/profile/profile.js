listener=(mql)=>{
    if (mql.matches){
        column=document.getElementById('user-details-column')
        column.removeAttribute('class')
        column.setAttribute('class','col-8')
    }
    else{
        column=document.getElementById('user-details-column')
        column.removeAttribute('class')
        column.setAttribute('class','col-8 mx-auto')
    }
}
var mql = window.matchMedia('(max-width: 500px)');
listener(mql)
window.addEventListener('resize',()=>{
    listener(mql)
})
