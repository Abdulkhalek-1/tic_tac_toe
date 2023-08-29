let gameSocket = null
let turn = ""

const game_id = document.querySelector(".game_id .id").textContent
const fullMsg = document.querySelector(".overlay")
const gameContainer = document.querySelector(".main")


// function setPaly() {
//   console.log
// }

function play(id) {
  elem = document.getElementById(id)
  elem.setAttribute("value", turn.toUpperCase())
  gameSocket.send(
    JSON.stringify({
      type: "message",
      id: id,
      value: elem.getAttribute("value")
    })
  );
  elem.textContent = turn.toUpperCase()
}

function update(data) {
  data = JSON.parse(data)
  for (let id in data) {
    document.getElementById(id).value = data[id]
    document.getElementById(id).textContent = data[id]
  }
}

function joinGame() {
  gameSocket = new WebSocket(`ws://${window.location.host}/ws/${game_id}/`)

  gameSocket.onclose = function (e) {
    fullMsg.style.visibility = "visible"
    gameContainer.style.display = "none"
  }

  gameSocket.onmessage = function (e) {
    if (e.data.length == 1) {
      turn = e.data
    } else {
      update(e.data)
    }
  };
}
window.onload = joinGame