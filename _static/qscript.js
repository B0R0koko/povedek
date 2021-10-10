
document.querySelector('label.col-form-label').innerHTML = "Предложите чему равно данное выражение: "

let timer
let seconds = 10
countdown()

function countdown() {
    document.querySelector("#timer-text").innerHTML = `Осталось ${seconds} секунд`
    seconds--
    if (seconds<0) {
        clearTimeout(timer)
    } else {
        timer = setTimeout(countdown, 1000);
    }
}