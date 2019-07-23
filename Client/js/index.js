document.addEventListener("DOMContentLoaded", function(event) {
    var elems = document.querySelectorAll(".dropdown-trigger");
    var instances = M.Dropdown.init(elems, {
        hover: true,
        constrainWidth: true,
        coverTrigger: false
    });
});
