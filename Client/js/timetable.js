document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, {
        format: "dd.mm",
        defaultDate: new Date(),
        setDefaultDate: true,
        firstDay: 1
    });
});

document.addEventListener("DOMContentLoaded", function(event) {
  var elems = document.querySelectorAll("select");
  var instances = M.FormSelect.init(elems, {});
});

document.addEventListener("DOMContentLoaded", function(event) {
    var sportsTypes = [
        "not-chosen",
        "volleyball",
        "streetball",
        "table-tennis",
        "poker",
        "chess",
        "water-polo",
        "badminton",
        "mafia"
    ];
    var selectList = document.querySelectorAll(".select-wrapper ul li");
    var sportTts = document.querySelectorAll("div.sport");
    var setHiddenExcept = function (sport) {
        for (var i = 0; i < sportTts.length; i++) {
            if (sportTts[i].classList[2] === sport || sport === "not-chosen") {
                sportTts[i].classList.remove("hidden-sport");
            } else {
                sportTts[i].classList.add("hidden-sport");
            }
        }
    }
    for (let i = 0; i < sportsTypes.length; i++) {
        let sportType = sportsTypes[i];
        selectList[i].addEventListener("click", event => {
            setHiddenExcept(sportType);
        });
    }
});


document.addEventListener("DOMContentLoaded", function(event) {
    var updateHiddenDate = function () {
        var dateSpan = document.querySelector(".date-text");
        var getMonth = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        };
        var date = dateSpan.textContent;
        var dateModified = "";
        if (date.length == 10) {
            dateModified += "0" + date[date.length - 1] + "." + getMonth[date.slice(5, 8)];
        } else {
            dateModified += date[date.length - 2] + date[date.length - 1] + "." + getMonth[date.slice(5, 8)];
        }
        var sportTts = document.querySelectorAll("div.sport");
        for (var i = 0; i < sportTts.length; i++) {
            if (sportTts[i].classList[2] != "chess" && sportTts[i].classList[2] != "badminton" && sportTts[i].classList[2] != 
                "table-tennis") {
                var isHidden = true;
                var games = sportTts[i].querySelectorAll("tr");
                console.log(games);
                for (var j = 1; j < games.length; j++) {
                    console.log(games[j].childNodes[1].textContent.slice(0, 5));
                    console.log(dateModified);
                    if (games[j].childNodes[1].textContent.slice(0, 5) != dateModified) {
                        games[j].classList.add("hidden-date");
                    } else {
                        games[j].classList.remove("hidden-date");
                        isHidden = false;
                    }
                }
                if (isHidden) {
                    sportTts[i].classList.add("hidden-date");   
                } else {
                    sportTts[i].classList.remove("hidden-date");
                }
            } else {
                var today = (new Date()).toString();
                var todayModified = today.slice(8, 10) + "." + getMonth[today.slice(4, 7)];
                if (todayModified == dateModified) {
                    sportTts[i].classList.remove("hidden-date");
                } else {
                    sportTts[i].classList.add("hidden-date");
                }
            }
        }
    };
    updateHiddenDate();
    var datePickerDone = document.querySelector(".datepicker-done");
    datePickerDone.addEventListener("click", function(event) {
        updateHiddenDate();
    });
});