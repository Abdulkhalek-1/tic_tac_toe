const result = document.querySelector(".result");
let x_score = document.querySelector(".score .x");
let o_score = document.querySelector(".score .o");
let turn = "x";
let squares = [];
let gameSocket = null
const game_id = document.querySelector(".game_id .id").textContent;

function joinGame() {
  gameSocket = new WebSocket(`ws://${window.location.host}/ws/${game_id}/`)
  gameSocket.onopen = function (e) {
    console.log("opened")
  }
  gameSocket.onclose = function (e) {
    console.log("closed")
  }
  gameSocket.onmessage = function (e) {
    console.log(JSON.parse(e.data))
  }
}

joinGame()


Array.from(document.getElementsByClassName("square")).forEach((square) => {
  let x = square.getAttribute("x");
  let y = square.getAttribute("y");
  let value = square.getAttribute("value");
  squares.unshift([square, x, y, value]);
});

function copy() {
  navigator.clipboard.writeText(`${window.location}`);
}

function update() {
  squares.forEach((elem) => {
    elem[3] = elem[0].getAttribute("value");
  });
}

function reset() {
  // Reset the board and variables
  Array.from(document.getElementsByClassName("square")).forEach((square) => {
    square.textContent = "";
    square.setAttribute("value", "");
  });
  turn = "x";
  update();
  result.style.display = "none";
}

function winner() {
  update();
  let winningCombinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
    [0, 4, 8], [2, 4, 6], // Diagonals
  ];

  for (let combination of winningCombinations) {
    let [a, b, c] = combination;
    if (squares[a][3] && squares[a][3] === squares[b][3] && squares[a][3] === squares[c][3]) {
      result.style.background = "rgb(34 255 181 / .9)";
      let winner = squares[a][3].toUpperCase()
      result.innerHTML = `<p>${winner} wins!</p>`;
      result.style.display = "block";
      if (winner === "X") {
        x_score.textContent = (Number.parseInt(x_score.textContent)+1).toString()
      } else if (winner === "O") {
        o_score.textContent = (Number.parseInt(o_score.textContent)+1).toString()
      }
      return;
    }
  }
  // Check for a draw
  if (squares.every((elem) => elem[3])) {
    result.style.background = "rgb(255 218 53 / 0.9)";
    result.innerHTML = "<p>Draw!</p>";
    result.style.display = "block";
  }
}

function game(id) {
  let elem = document.getElementById(id);
  if (!elem.textContent) {
    if (turn === "x") {
      elem.textContent = "X";
      elem.setAttribute("value", "x");
      turn = "o";
    } else if (turn === "o") {
      elem.textContent = "O";
      elem.setAttribute("value", "o");
      turn = "x";
    }
    winner();
  }
}




/**
 * score
 * turn
 * count
 */