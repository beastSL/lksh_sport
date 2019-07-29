document.addEventListener("DOMContentLoaded", function(event) {
    var tabfield = document.querySelector(".tabs");
    console.log(tabfield);
    var instance = M.Tabs.init(tabfield, {});
});

var decodeAnswer = function (s) {
    for(var a, b, i = -1, l = (s = s.split("")).length, o = String.fromCharCode, c = "charCodeAt"; ++i < l;
        ((a = s[i][c](0)) & 0x80) &&
        (s[i] = (a & 0xfc) == 0xc0 && ((b = s[i + 1][c](0)) & 0xc0) == 0x80 ?
        o(((a & 0x03) << 6) + (b & 0x3f)) : o(128), s[++i] = "")
    );
    return s.join("");
};

document.addEventListener("DOMContentLoaded", function(event) {
    var divTable = document.getElementById("participants");
    var table = divTable.querySelector("table");
    var getParticipants = async function () {
        const response = await fetch("http://sport.lksh.ru:42069/api/participants?sport=streetball");
        const data = await response.json();
        var dictionary = {};
        for (var i = 0; i < data.length; i++) {
            dictionary[decodeAnswer(data[i].team)] = [];
        }
        for (var i = 0; i < data.length; i++) {
            dictionary[decodeAnswer(data[i].team)].push([decodeAnswer(data[i].name), decodeAnswer(data[i].group)]);
        }
        for (var property in dictionary) {
            var row = document.createElement("tr");
            table.appendChild(row);
            var cell = document.createElement("td");
            cell.textContent = property;
            row.appendChild(cell);
            cell = document.createElement("td");
            cell.classList.add("participants");
            var divider = document.createElement("div");
            divider.classList.add("divider");
            for (var i = 0; i < dictionary[property].length; i++) {
                cell.innerHTML += dictionary[property][i][0] + " ";
                var group = document.createElement("div");
                group.classList.add("parallel");
                group.textContent = decodeAnswer(dictionary[property][i][1]);
                cell.appendChild(group);
                if (i != dictionary[property].length - 1) {
                    cell.appendChild(divider);
                }
            }
            row.appendChild(cell);
        }
        console.log(typeof response);
        console.log(response);
    };
    getParticipants().catch(error => {
        var errorElement = document.createElement("p");
        errorElement.classList.add("error");
        errorElement.textContent = "Произошла ошибка, обновите страницу.";
        divTable.appendChild(errorElement);
    });
});