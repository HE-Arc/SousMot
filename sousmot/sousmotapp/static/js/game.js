// Variables declaration
let grid = {
    x: 1,
    y: 0
}
let word = wordFirstLetter.concat('.'.repeat(wordLength - 1)); // Shared word variable filled with dots and initial letter
const countDownDate = new Date(end_time * 1000).getTime(); // Date to the end of countdown
let userTryToWriteFirstLetter = false //Variable used to remember if the user is trying to write the first letter at the first position

writeWord(); // Write word in grid for first time

/**
 * Listen to the keydown event user keyboard
 */
document.addEventListener('keydown', (event) => {
    addLetterToWord(event.key);

    // Uncomment this to display the code value
    //alert(`Key pressed ${event.key} \r\n Key code value: ${event.code}`);
}, false);

/**
 * Add a given letter to the grid
 * @param letter char to add to the grid
 */
function addLetterToWord(letter) {
    // Every letter should be uppercase
    letter = letter.toUpperCase()

    // Test if the received letter is accepted
    if ("ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").includes(letter)) {
        // When the letter is a regular alphabet letter, set it at the right position in word
        if (grid.x === 1) {
            word = wordFirstLetter.concat('.'.repeat(wordLength - 1));
            writeWord()
        }

        if (grid.x < wordLength) {
            if (letter !== wordFirstLetter || grid.x !== 1 || userTryToWriteFirstLetter === true) {
                word = word.replaceAt(grid.x, letter);
                // Once the letter is added we need to increment the user position in grid (grid column)
                grid.x++;
                writeWord();
            } else {
                userTryToWriteFirstLetter = true
            }
        }
    } else if (letter === "BACKSPACE") {
        // When user send backspace character we need to replace the last added character by '.'
        // Pay attention : First letter is never erased !
        if (grid.x > 1) {
            word = word.replaceAt(grid.x - 1, '.')
            // Once the letter is added we need to decrement the user position in grid (grid column)
            grid.x--;
            writeWord();
        } else {
            userTryToWriteFirstLetter = false
        }
    } else if (letter === "ENTER") {
        // When user send enter character we need to verify the word
        // The letter is verified only when the word is full
        if (word.match(/\./g) == null) {
            // Increment the number of user try (grid rows) and reset user position in grid (grid column)
            grid.y++;
            grid.x = 1;
            userTryToWriteFirstLetter = false

            verifyWord();
            writeWord();
        }
    }
}

/**
 * Send the word to the server and wait a response to colorize the letters
 */
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

    // Get user previous row
    let myTable = document.getElementById('table');
    let rows = myTable.rows;
    let resultRow = rows[grid.y - 1];

    // For each letter in the response build word and colorize letters
    for (let i = 0; i < response.length; i++) {
        // Get the corresponding keyboard letter
        let keyboardLetter = document.getElementById('kb' + response[i]["letter"]);

        // Check if the letter is right or not
        if (response[i]["type"] === "good_place") {
            // Build word for the next display
            word = word.replaceAt(i, response[i]["letter"]);

            // Colorize cells and keyboard
            resultRow.cells[i].classList.add("good_place");
            keyboardLetter.classList.add("good_place")
        } else if (response[i]["type"] === "bad_place") {
            // Colorize cells and keyboard
            resultRow.cells[i].classList.add("bad_place");
            keyboardLetter.classList.add("bad_place")
        }
    }
}

/**
 * Write the word variable in the grid
 */
function writeWord() {
    // Get user current row
    let myTable = document.getElementById('table');
    let rows = myTable.rows;
    let inputRow = rows[grid.y];

    // Write inside the grid letter by letter
    for (let i = 0; i < wordLength; i++) {
        inputRow.cells[i].children[0].innerText = word[i];
    }
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