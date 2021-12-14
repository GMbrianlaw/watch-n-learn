window.onload = () => {
    for (const link of document.getElementsByTagName("nav").item(0).children) {
        if (link.pathname === document.location.pathname) {
            link.classList.add("navbar_active");
        }
    }
};

/**
 * @function
 * 
 * @param {Element} message
 * 
 * @returns {undefined}
 */
function removeMessage(message) {

    message.parentElement.remove();

}
