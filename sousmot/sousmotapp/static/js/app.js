
document.getElementById('word-length-value').textContent = document.getElementById("word-length").value;

// Create Game form : Toggle mode button
let gamemodeList = [];
const gameModeInput = document.getElementById("gamemode-input");
const gameDurationField = document.querySelector(".game-duration-field");
const nbOfRoundField = document.querySelector(".number-word-field");

document.querySelectorAll(".field.gamemode .button").forEach( el => {

    el.addEventListener("click", ev => {
        gamemodeList.forEach( i => i.classList.remove("is-selected", "is-crimson"));
        el.classList.add("is-selected", "is-crimson");
        gameModeInput.value = el.dataset.gamemode;

        // Hide field like game duration and number of round depending on the mode
        if (el.textContent.trim().toLowerCase() === "rounds") {
            // Hide Game Duration
            gameDurationField.classList.add("field-is-invisible");
            nbOfRoundField.classList.remove("field-is-invisible");
        }
        else {
            // Hide Number of rounds
            nbOfRoundField.classList.add("field-is-invisible");
            gameDurationField.classList.remove("field-is-invisible");
        }

    });
    gamemodeList.push(el);
})

// Slider management
