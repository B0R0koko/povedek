// Disable next page button 
var opened = true
var buttonNext = document.querySelector("button.otree-btn-next")
buttonNext.setAttribute('disabled', 'disabled')

function openPopup() {
    if (!! opened) {
        document.querySelector("#popup-1").classList.toggle("active")
        opened = false
    } 

} 

function closePopup() {
    document.querySelector("#popup-1").classList.remove("active")
    var checkbox = document.querySelector("#check-agreement")
    buttonNext.removeAttribute('disabled')
    checkbox.setAttribute('disabled', 'disabled')
}