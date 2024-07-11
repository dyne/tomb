// When the user scrolls the page, execute scrollMenu
window.onscroll = function () { scrollMenu() };

// Get the navbar
var navbar = document.getElementById("logo");
var hider = document.getElementById("navigation");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function scrollMenu() {
  if (window.pageYOffset >= sticky) {
    hider.classList.add("enabled");
    navbar.classList.add("slider");

  } else {
    hider.classList.remove("enabled");
    navbar.classList.remove("slider");

  }
}





// Make a pretty background when menu is open
var bodyBluring = document.getElementById("main-wrapper");

function blurBody() {
  bodyBluring.classList.toggle("blurredout");
}
function removeBlur() {
  bodyBluring.classList.remove("blurredout");
}

/// request permission to autoplay
