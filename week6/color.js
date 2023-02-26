document.addEventListener("DOMContentLoaded",()=>{
    document.querySelector("#colors").onchange = function(){
        document.querySelector('h1').style.color = this.value;
    }
});