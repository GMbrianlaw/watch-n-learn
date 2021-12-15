for (const links of document.getElementsByTagName("nav").item(0).children) {
    for (const link of links.children) {
        if (link.pathname === window.location.pathname) {
            link.classList.add("navbar_active");
        }
    }
}

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
