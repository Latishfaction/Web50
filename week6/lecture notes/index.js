function counter(){
    let count =0;
    const heading = document.querySelector('h1');
    heading.innerHTML = ++count;
}
document.addEventListener("DOMContentLoaded",()=>{
    const button = document.querySelector('button');
    button.onclick = counter;
    console.log(button);
});

