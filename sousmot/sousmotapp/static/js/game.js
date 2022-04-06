let userTry = 0;
let userPosition = 1;
let word = wordFirstLetter.concat('.'.repeat(wordLength - 1));
writeWord();

document.addEventListener('keydown', (event) => {
    let letter = event.key;
    addLetterToWord(letter);

    //var code = event.code;
    //alert(`Key pressed ${letter} \r\n Key code value: ${code}`);
}, false);

function addLetterToWord(letter) {
    letter = letter.toUpperCase()
    if ("ABCDEFGHIJKLMNOPQRSTUVWXYZ".includes(letter)) {
        if (userPosition < wordLength) {
            word = word.replaceAt(userPosition, letter);
            userPosition++;
            writeWord()
        }
    } else if (letter == "BACKSPACE") {
        if (userPosition > 0) {
            word = word.replaceAt(userPosition - 1, '.')
            userPosition--;
            writeWord()
        }
    } else if (letter == "ENTER") {
        if (userPosition > 0) {
            userTry++;
            userPosition=1;
            verifyWord()
            writeWord();
        }
    }
}

function verifyWord() {
    console.log("Verify word : " + word); // Replace by function to verify word
    word = "P.R.." // Known letters
}

function writeWord() {
    let myTable = document.getElementById('table');
    let rows = myTable.rows;
    let inputRow = rows[userTry];
    for (let i = 0; i < wordLength; i++) {
        inputRow.cells[i].children[0].innerText = word[i];
    }
}

let countDownDate = new Date(end_time * 1000).getTime();
let x = setInterval(function () {
    // Get today's date and time
    let now = new Date().getTime();
    // Find the distance between now and the count down date
    let distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result in the element with id="demo"
    if (minutes >= 0 && seconds >= 0) {
        document.getElementById("timer").innerHTML = pad(minutes, 2) + ":" + pad(seconds, 2);
    }
}, 1000);

// https://stackoverflow.com/questions/1431094/how-do-i-replace-a-character-at-a-particular-index-in-javascript
String.prototype.replaceAt = function (index, replacement) {
    return this.substring(0, index) + replacement + this.substring(index + replacement.length);
}

https://stackoverflow.com/questions/2998784/how-to-output-numbers-with-leading-zeros-in-javascript
    function pad(num, size) {
        num = num.toString();
        while (num.length < size) num = "0" + num;
        return num;
    }