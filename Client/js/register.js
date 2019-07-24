
document.addEventListener('DOMContentLoaded', function(event) {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {});
});

document.addEventListener("DOMContentLoaded", function(event){
    var sportsTypes = ["not-chosen", "volleyball", "streetball", "table-tennis", "poker", "chess", "water-polo", 
        "badminton", "mafia"];
    var divSelect = document.querySelector("div.select-sport");
    var selectList = document.querySelectorAll(".select-wrapper ul li");   
    var inputs = document.querySelectorAll('.input-field > input[type="text"]');
    var setRequired = function(from, to) {
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].required = false;
        }
        for (var i = from; i <= to; i++) {
            inputs[i].required = true;
        }
    };
    console.log(inputs);
    selectList[0].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[0]);
        setRequired(0, -1);
    });
    selectList[1].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[1]);
        setRequired(0, 6);
    });
    selectList[2].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[2]);
        setRequired(0, 3);
    });
    selectList[3].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[3]);
        setRequired(9, 9);
    });
    selectList[4].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[4]);
        setRequired(9, 9);
    });
    selectList[5].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[5]);
        setRequired(9, 9);
    });
    selectList[6].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[6]);
        setRequired(0, 5);
    });
    selectList[7].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[7]);
        setRequired(9, 9);
    });
    selectList[8].addEventListener("click", function(event) {
        divSelect.classList.replace(divSelect.classList[1], sportsTypes[8]);
        setRequired(9, 9);
    });
});

var checkboxNoTeam = document.querySelector(".chkbox p label input");
checkboxNoTeam.addEventListener("click", function(event) {
    var noTeam = document.querySelector(".chkbox");
    var inputs = document.querySelectorAll('.input-field > input[type="text"]');
    var setRequired = function(from, to) {
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].required = false;
        }
        for (var i = from; i <= to; i++) {
            inputs[i].required = true;
        }
    };
    var checked = false;
    for (var i = 0; i < noTeam.classList.length; i++) {
        if (noTeam.classList[i] == "checked") {
            checked = true;
            break;
        }
    }
    if (checked) {
        noTeam.classList.remove("checked");
    } else {
        noTeam.classList.add("checked");
    }
    setRequired(9, 9);
});

window.addEventListener("load", function () {
    function sendData() {
        var XHR = new XMLHttpRequest();
    
        // Bind the FormData object and the form element
        var FD = new FormData(form);
    
        // Define what happens on successful data submission
        XHR.addEventListener("load", function(event) {
            alert(event.target.responseText);
        });
    
        // Define what happens in case of error
        XHR.addEventListener("error", function(event) {
            alert('Oops! Something went wrong.');
        });
    
        // Set up our request
        XHR.open("POST", "https://echo.htmlacademy.ru");
    
        // The data sent is what the user provided in the form
        XHR.send(FD);
    }

    // Access the form element...
    var form = document.getElementById("registerForm");
    // ...and take over its submit event.
    form.addEventListener("submit", function (event) {
        event.preventDefault();
    
        sendData();
    });
});