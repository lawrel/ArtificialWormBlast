/* JAVASCRIPT FOR A TABBED INTERFACE ON ONE WEBPAGE
 * [USAGE]: <button class="tabbutton" onclick(event, tab name)>
 * <div class="tabcontent" id="tab name"> </div>
 * Only content inside the "tabconntent" class is hidden
 * Add a separate button and corresponding div for each tab you desire
 *----------------------------------------------------------------------
*/
function openTab(evt, Name) {
    var i, tabcontent, tablinks;

    // hide all tabs we are not clicked on
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // force all other buttons into default state
    tablinks = document.getElementsByClassName("tabbutton");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // register current tab's button as 'active' when viewing, not just when clicked
    document.getElementById(Name).style.display = "block";
    evt.currentTarget.className += " active";
}