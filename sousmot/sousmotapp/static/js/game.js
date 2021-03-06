// Variables declaration

let grid = {
    x: 1,
    y: 0
}
let word = wordFirstLetter.concat('.'.repeat(wordLength - 1)); // Shared word variable filled with dots and initial letter
const countDownDate = new Date(end_time * 1000).getTime(); // Date to the end of countdown
let isUserTryToWriteFirstLetter = false;// Variable used to remember if the user is trying to write the first letter at the first position


writeWord(); // Write word in grid for first time

/**
 * Listen to the keydown event user keyboard
 */
document.addEventListener('keydown', (event) => {
    addLetterToWord(event.key);

    // Uncomment this to display the code value
    // alert(`Key pressed ${event.key} \r\n Key code value: ${event.code}`);
}, false);

/**
 * Add a given letter to the grid
 * @param letter char to add to the grid
 */
function addLetterToWord(letter) {
    // Every letter should be uppercase
    letter = letter.toUpperCase();

    if ("ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").includes(letter) && grid.x < wordLength) {
        // When the letter is a regular alphabet letter, set it at the right position in word

        // Erase the rest of the word when user start to type
        word = grid.x === 1 ? wordFirstLetter.concat('.'.repeat(wordLength - 1)) : word;

        // Do not display letter if the first letter is typed but only onw time
        if (letter === wordFirstLetter && grid.x === 1 && !isUserTryToWriteFirstLetter) {
            isUserTryToWriteFirstLetter = true;
        } else {
            isUserTryToWriteFirstLetter = false;
            word = word.replaceAt(grid.x, letter);
            grid.x++;
        }
        writeWord();

    } else if (letter === "BACKSPACE" && grid.x > 1) {
        // When user send backspace character we need to replace the last added character by '.'
        word = word.replaceAt(grid.x - 1, '.');
        grid.x--;
        writeWord();


    } else if (letter === "ENTER" && word.match(/\./g) == null) {
        // When user send enter character we need to verify the word
        // The letter is verified only when the word is full

        grid.y++;
        grid.x = 1;
        verifyWord();
        if (grid.y === 6) {
            raz();
        }
    }

}

/**
 * Send the word to the server and wait a response to colorize the letters
 */
function verifyWord() {

    let xmlhttp = new XMLHttpRequest();
    let url = window.location.href + "verify/?word=" + word;

    xmlhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let response = JSON.parse(this.responseText);
            if (response["result"] !== "Not found in dictionnary") {
                displayResponse(response["result"]);
                if (response["next"] != null) {
                    nextWord(response["next"]["first_letter"])
                }
            } else {
                grid.y--;
                word = wordFirstLetter.concat('.'.repeat(wordLength - 1));
                writeWord()
            }
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

}

/**
 * Colorize letters with the response
 * @param response
 */
function displayResponse(response) {
    // Clean cached word
    word = wordFirstLetter.concat('.'.repeat(wordLength - 1));

    // Get user previous row
    let resultRow = document.getElementById('table').rows[grid.y - 1];

    // For each letter in the response build word and colorize letters

    for (let i = 0; i < response.length; i++) {
        // Colorize cells and keyboard
        resultRow.cells[i].classList.add(response[i]["type"]);

        document.getElementById('kb' + response[i]["letter"]).classList.add(response[i]["type"]);

        // Check if the letter is right or not and bild word for next display
        word = response[i]["type"] === "good_place" ? word.replaceAt(i, response[i]["letter"]) : word;
    }
    if (word.includes(".")) {
        writeWord();
    }
}

/**
 * Write the word variable in the grid
 */
function writeWord() {
    // Get user current row
    let inputRow = document.getElementById('table').rows[grid.y];

    // Write inside the grid letter by letter
    for (let i = 0; i < wordLength; i++) {
        inputRow.cells[i].children[0].innerText = word[i];
    }
}

/**
 * Reset game and get a new word
 * @param first_letter
 */
function nextWord(first_letter) {
    setTimeout(function () {
        wordFirstLetter = first_letter
        document.getElementById("wordcounter").textContent++;
        raz()

    }, 2000);
}

/**
 * Restart view
 */
function raz() {
    word = wordFirstLetter.concat('.'.repeat(wordLength - 1))
    grid.x = 1
    grid.y = 0
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").forEach(letter => document.getElementById('kb' + letter).className = "")
    let cells = document.getElementsByTagName("td")
    for (let i = 0; i < cells.length; i++) {
        cells[i].className = "";
        cells[i].children[0].innerText = "";
    }
    writeWord()
}

/**
 * Display the countdown on the
 * @type {number}
 * @see https://www.w3schools.com/howto/howto_js_countdown.asp
 */
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

    if (minutes === 0 && seconds === 0) {
        window.location.href = urlredirect;
    }
}, 1000);

/**
 * Replace a letter at a given index in a string
 * @param index index of letter to replace
 * @param replacement letter to replace with
 * @returns {string}
 * @see https://stackoverflow.com/questions/1431094/how-do-i-replace-a-character-at-a-particular-index-in-javascript
 */
String.prototype.replaceAt = function (index, replacement) {
    return this.substring(0, index) + replacement + this.substring(index + replacement.length);
}

/**
 * Write a number with a given number of 0 before if needed ex: 08, 09, 10, 11...
 * @param num Number to write
 * @param size Size to match
 * @returns {string | string}
 * @see //https://stackoverflow.com/questions/2998784/how-to-output-numbers-with-leading-zeros-in-javascript
 */
function pad(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}