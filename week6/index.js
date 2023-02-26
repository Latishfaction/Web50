// apply local storage
if(!localStorage.getItem('counter')){
    // SET local storage item
    localStorage.setItem('counter',0);
}
function count(){
    let counter = localStorage.getItem('counter');
    counter++;
    document.querySelector('h1').innerHTML = counter;
    // set the incremented value to the local storage
    localStorage.setItem('counter',counter);
}
document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    document.querySelector('button').onclick=count;

});