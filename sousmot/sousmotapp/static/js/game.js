let userTry = 0;
let userPosition = 1;
let word = wordFirstLetter.concat('.'.repeat(wordLength - 1));
writeWord();

document.addEventListener('keydown', (event) => {
    let letter = event.key;
    addLetterToWord(letter);

    // Uncomment this to display the code value
    //var code = event.code;
    //alert(`Key pressed ${letter} \r\n Key code value: ${code}`);
}, false);

function addLetterToWord(letter) {
    letter = letter.toUpperCase()
    if ("ABCDEFGHIJKLMNOPQRSTUVWXYZ".includes(letter)) {
        if (userPosition < wordLength) {
            word = word.replaceAt(userPosition, letter);
            userPosition++;
            writeWord();
        }
    } else if (letter === "BACKSPACE") {
        if (userPosition > 1) {
            word = word.replaceAt(userPosition - 1, '.')
            userPosition--;
            writeWord();
        }
    } else if (letter === "ENTER") {
        // Send only if word is full
        if (word.match(/\./g) == null) {
            userTry++;
            userPosition = 1;
            verifyWord();
            writeWord();
        }
    }
}

function verifyWord() {
    console.log("Verify word : " + word); // TODO replace by function to send word to server

    // TODO get response from server
    let response = [
        {"letter": "P", "type": "good_place"},
        {"letter": "O", "type": "wrong"},
        {"letter": "R", "type": "bad_place"},
        {"letter": "T", "type": "good_place"},
        {"letter": "E", "type": "good_place"}
    ]

    // Clean cached word
    word = wordFirstLetter.concat('.'.repeat(wordLength - 1));

    let myTable = document.getElementById('table');
    let rows = myTable.rows;
    let resultRow = rows[userTry - 1];
    for (let i = 0; i < response.length; i++) {
        let keyboardLetter = document.getElementById('kb' + response[i]["letter"]);
        if (response[i]["type"] === "good_place") {
            word = word.replaceAt(i, response[i]["letter"]);
            resultRow.cells[i].classList.add("good_place");
            keyboardLetter.classList.add("good_place")
        } else if (response[i]["type"] === "bad_place") {
            resultRow.cells[i].classList.add("bad_place");
            keyboardLetter.classList.add("bad_place")
        }
    }
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
    let now = new Date().getTime();
    let distance = countDownDate - now;

    // Time calculations for minutes and seconds
    let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result
    if (minutes >= 0 && seconds >= 0) {
        document.getElementById("timer").innerHTML = pad(minutes, 2) + ":" + pad(seconds, 2);
    }
}, 1000);

// https://stackoverflow.com/questions/1431094/how-do-i-replace-a-character-at-a-particular-index-in-javascript
String.prototype.replaceAt = function (index, replacement) {
    return this.substring(0, index) + replacement + this.substring(index + replacement.length);
}

//https://stackoverflow.com/questions/2998784/how-to-output-numbers-with-leading-zeros-in-javascript
function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}