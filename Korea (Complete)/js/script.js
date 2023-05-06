/* Menu */

let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");

// The code adds an event listener to the HTML element with the variable 'closeBtn', which is triggered by a click,
// when the event listener is triggered, it toggles the 'open' class of the HTML element with the variable sidebar,
// it also calls the function 'menuBtnChange()'.

// The 'menuBtnChange()' function checks whether sidebar contains the 'open' class,
// if it does, it replaces the class of the 'closeBtn' element from 'bx-menu' to 'bx-menu-alt-right',
// if it does not, it replaces the class of the 'closeBtn' element from 'bx-menu-alt-right' to 'bx-menu'.

closeBtn.addEventListener("click", ()=>{

    sidebar.classList.toggle("open");
    menuBtnChange();
});

function menuBtnChange(){

    if (sidebar.classList.contains("open")){

        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
    } else {
        
        closeBtn.classList.replace("bx-menu-alt-right","bx-menu");
    }
}

/* Footer */

// sets the 'innerHTML' property of the 'year' element to the current year using the 'getFullYear' method of the 'Date' object.

const year = document.querySelector('#year');
year.innerHTML = new Date().getFullYear();