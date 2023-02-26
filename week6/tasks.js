document.addEventListener("DOMContentLoaded",function(){
    document.querySelector("#task-form").onsubmit = function(){
        const input = document.querySelector("#task-value");

        if(input.value.length == 0){
            // get the button and disabled it
            button.disabled = true;
            button.style.color = 'red';
            return false;
        }
        else{
            // create li element
            const li = document.createElement('li');
            // adding the input text to li
            li.innerHTML = input.value
            // select ul and appending li
            document.querySelector('#tasks').append(li);
            input.value = '';
            return false;
        }
    }
});