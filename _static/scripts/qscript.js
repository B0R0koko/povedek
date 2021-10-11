// let timer
// let seconds = 10
// countdown()

// function countdown() {
//     let seconds_string = document.querySelector("span.otree-timer__time-left").innerHTML
//     let seconds = parseInt(seconds_string.slice(0)) * 60 + parseInt(seconds_string.slice(2, 4))
//     document.querySelector("#timer-text").innerHTML = `Осталось ${seconds} секунд`
//     seconds--
//     if (seconds < 0) {
//         clearTimeout(timer)
//     } else {
//         timer = setTimeout(countdown, 1000);
//     }
// }