document.addEventListener("DOMContentLoaded",function(){
    document.querySelector("form").onsubmit = function(){
        fetch("https://open.er-api.com/v6/latest/USD/")
        .then(response => response.json())
        .then(data=> {
            // get the country from the input
            let country  = document.querySelector("#currency").value.toUpperCase();
            // find the cuntry in api
            if(data.rates[country]!==undefined){
                // get the value
                let value  = data.rates[country];
                // set the rate in the html page
                document.querySelector("#result").innerHTML = `1 USD = ${value} ${country}`
                
            }
            else{
                document.querySelector("#result").innerHTML = `Invalid Currency.`
            }
        })
        .catch(error=> {
            document.querySelector("body").innerHTML = `${error}`
        })
        return false;
    }
});