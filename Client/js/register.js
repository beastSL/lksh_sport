document.addEventListener("DOMContentLoaded", function(event) {
    var elems = document.querySelectorAll("select");
    var instances = M.FormSelect.init(elems, {});
});

document.addEventListener("DOMContentLoaded", function(event) {
    var sportsTypes = [
        "not-chosen",
        "football",
        "volleyball",
        "streetball",
        "table-tennis",
        "poker",
        "chess",
        "water-polo",
        "badminton",
        "mafia"
    ];
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
    let requiredInputs = [
        [0, -1],
        [0, 3],
        [0, 6],
        [0, 3],
        [9, 9],
        [9, 9],
        [9, 9],
        [0, 4],
        [9, 9],
        [9, 9]
    ];
    for (let i = 0; i < sportsTypes.length; i++) {
        let sportType = sportsTypes[i];
        let required = requiredInputs[i];
        selectList[i].addEventListener("click", event => {
            divSelect.classList.replace(divSelect.classList[1], sportType);
            setRequired(...required);
        });
    }
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

window.addEventListener("load", function() {
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
            alert("Oops! Something went wrong.");
        });

        // Set up our request2620:9b::194b:a5f6 25.75.165.246
        XHR.open("POST", "http://sport.lksh.ru:42069/api/register_team");

        // The data sent is what the user provided in the form
        XHR.send(FD);
    }

    // Access the form element...
    var form = document.getElementById("registerForm");
    // ...and take over its submit event.
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        sendData();
    });
});
/*
var decodeAnswer = function (s) {
    for(var a, b, i = -1, l = (s = s.split("")).length, o = String.fromCharCode, c = "charCodeAt"; ++i < l;
        ((a = s[i][c](0)) & 0x80) &&
        (s[i] = (a & 0xfc) == 0xc0 && ((b = s[i + 1][c](0)) & 0xc0) == 0x80 ?
        o(((a & 0x03) << 6) + (b & 0x3f)) : o(128), s[++i] = "")
    );
    return s.join("");
}

fetch('http://25.75.165.246:42069/api/events')
    .then(function(response) {
        return response.json();
    })
    .then(function(myJson) {
        console.log(JSON.stringify(myJson));
    });
*/