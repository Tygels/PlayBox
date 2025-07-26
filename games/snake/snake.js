const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

const box = 20;
let snake = [{x: 9 * box, y: 10 * box}];
let direction = null;
let food = randomFood();
let score = 0;

document.addEventListener('keydown', changeDirection);

function changeDirection(event) {
    const key = event.keyCode;
    if (key === 37 && direction !== 'RIGHT') direction = 'LEFT';
    else if (key === 38 && direction !== 'DOWN') direction = 'UP';
    else if (key === 39 && direction !== 'LEFT') direction = 'RIGHT';
    else if (key === 40 && direction !== 'UP') direction = 'down';
}

function randomFood(){
    return {
        x: Math.floor(Math.random() * 19) * box,
        y: Math.floor(Math.random() * 19) * box
    };

}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw snake
  for (let i = 0; i < snake.length; i++) {
    ctx.fillStyle = i === 0 ? "#00e676" : "#00c853";
    ctx.fillRect(snake[i].x, snake[i].y, box, box);
  }

  // Draw food
  ctx.fillStyle = "#ff1744";
  ctx.fillRect(food.x, food.y, box, box);

  // Move snake
  const head = { ...snake[0] };
  if (direction === 'LEFT') head.x -= box;
  else if (direction === 'UP') head.y -= box;
  else if (direction === 'RIGHT') head.x += box;
  else if (direction === 'DOWN') head.y += box;

  // Collision with wall
  if (
    head.x < 0 || head.x >= canvas.width ||
    head.y < 0 || head.y >= canvas.height
  ) return gameOver();

  // Collision with self
  for (let i = 1; i < snake.length; i++) {
    if (head.x === snake[i].x && head.y === snake[i].y) return gameOver();
  }

  // Eat food
  if (head.x === food.x && head.y === food.y) {
    score++;
    document.getElementById("score").innerText = `Score: ${score}`;
    food = randomFood();
  } else {
    snake.pop();
  }

  snake.unshift(head);
}

function gameOver() {
  clearInterval(game);
  alert(`Game Over! Your score: ${score}`);
}

const game = setInterval(draw, 100);