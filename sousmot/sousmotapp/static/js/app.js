
document.getElementById('word-length-value').textContent = document.getElementById("word-length").value;

// Create Game form : Toggle mode button
let gamemodeList = [];
const gameModeInput = document.getElementById("gamemode-input");

document.querySelectorAll(".field.gamemode .button").forEach( el => {
    el.addEventListener("click", ev => {
        gamemodeList.forEach( i => i.classList.remove("is-selected", "is-crimson"));
        el.classList.add("is-selected", "is-crimson");
        gameModeInput.value = el.dataset.gamemode;

    });
    gamemodeList.push(el);
})

// Slider management
