var userTry = 0;
var userPosition = 1;
var word = wordFirstLetter.concat('.'.repeat(wordLength - 1));
writeWord();

document.addEventListener('keydown', (event) => {
    var letter = event.key;
    var code = event.code;
    addLetterToWord(letter);
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
    }
}

function writeWord() {
    var myTable = document.getElementById('table');
    var rows = myTable.rows;
    var inputRow = rows[userTry];
    for (let i = 0; i < wordLength; i++) {
        inputRow.cells[i].innerText = word[i];
    }
}

// https://stackoverflow.com/questions/1431094/how-do-i-replace-a-character-at-a-particular-index-in-javascript
String.prototype.replaceAt = function (index, replacement) {
    return this.substring(0, index) + replacement + this.substring(index + replacement.length);
}