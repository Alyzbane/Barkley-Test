function toggleNames() {
    var scientificNames = document.querySelectorAll('.scientific-name');
    var commonNames = document.querySelectorAll('.common-name');
    for (var i = 0; i < scientificNames.length; i++) {
        if (scientificNames[i].style.display === 'none') {
            scientificNames[i].style.display = 'inline';
            commonNames[i].style.display = 'none';
        } else {
            scientificNames[i].style.display = 'none';
            commonNames[i].style.display = 'inline';
        }
    }
}
// Dropdown toggle function
function toggleDropdown() {
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.classList.toggle('hidden');
}