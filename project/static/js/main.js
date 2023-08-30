let gameSocket = null
let playerTurn = "x"
let currentTurn = "x"
const game_id = document.querySelector(".game_id .id").textContent
const fullMsg = document.querySelector(".overlay")
const gameContainer = document.querySelector(".main")
const result = document.querySelector(".result")
class ElementCollection extends Array {
  on(event, callbackOrSelector, callback) {
    if (typeof callbackOrSelector === "function") {
      this.forEach((e) =>
        e.addEventListener(event, callbackOrSelector, callback)
      );
    } else {
      this.forEach((element) => {
        element.addEventListener(event, (e) => {
          if (e.target.matches(callbackOrSelector)) callback(e);
        });
      });
    }
    return this;
  }
  removeClass(className) {
    this.forEach((e) => e.classList.remove(className));
    return this;
  }
  addClass(className) {
    this.forEach((e) => e.classList.add(className));
    return this;
  }
}

function $(param) {
  if (typeof param === "string" || param instanceof String) {
    if (param.includes("<")) {
      return new ElementCollection(
        ...new DOMParser().parseFromString(param, "text/html").body.childNodes
      );
    } else {
      return new ElementCollection(...document.querySelectorAll(param));
    }
  } else {
    return new ElementCollection(param);
  }
}

function setAnimation(id, value) {
  let elem = document.getElementById(id)
  const symbols = { "x": `<svg xmlns="http://www.w3.org/2000/svg" class="h-1/2 w-1/2 text-white pointer-events-none select-none duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 20 20 4M4 4 20 20" /></svg>`, "o": `<svg xmlns="http://www.w3.org/2000/svg" class="h-1/2 w-1/2 text-white pointer-events-none select-none duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728" /></svg>`, "": "" };
  if (value) {
    console.log("value=>", value)
    elem.innerHTML = symbols[value.toLowerCase()];
    setTimeout(() => {
      let cell = elem.firstElementChild;
      $(cell)
        .removeClass("h-1/2")
        .removeClass("w-1/2")
        .addClass("h-full")
        .addClass("w-full");
    }, 10);
  } else { elem.innerHTML = ""}
}

function play(id) {
  let elem = document.getElementById(id)
  if (currentTurn.toLowerCase() == playerTurn.toLowerCase() && elem) {
    gameSocket.send(
      JSON.stringify({
        type: "message",
        id: id,
        value: playerTurn.toUpperCase(),
        current_turn: currentTurn
      })
    );
  }
}

function update(data) {
  for (let id in data) {
    elem = document.getElementById(id)
    if (elem.getAttribute("value") != data[id]) {
      setAnimation(id, data[id])
      elem.setAttribute("value", data[id])
    }
  }
}

function setResult(x_score, o_score) {
  if (x_score || o_score) {
    document.querySelector(".x-score").textContent = x_score
    document.querySelector(".o-score").textContent = o_score
  }
}

function joinGame() {
  gameSocket = new WebSocket(`ws://${window.location.host}/ws/${game_id}/`)

  gameSocket.onclose = function (e) {
    // fullMsg.style.visibility = "visible"
    // gameContainer.style.display = "none"
  }

  gameSocket.onmessage = function (e) {
    if (e.data.length == 1) {
      playerTurn = e.data
    } else {
      data = JSON.parse(e.data)
      update((data)["state"])
      if (data["current_turn"]) {
        currentTurn = data["current_turn"]
      }
      setResult(data["x_score"], data["o_score"])
    }
  }
}

window.onload = joinGame