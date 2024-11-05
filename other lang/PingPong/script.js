const canvas = document.getElementById("pongCanvas");
const context = canvas.getContext("2d");
const menuScreen = document.getElementById("menuScreen");
const gameOverScreen = document.getElementById("gameOverScreen");
const startButton = document.getElementById("startButton");
const restartButton = document.getElementById("restartButton");
const scoreDisplay = document.getElementById("scoreDisplay");
const difficultySelect = document.getElementById("difficulty");

canvas.width = 800;
canvas.height = 400;

let score = 0;
let gameRunning = false;
let ballSpeed = 5; // Default speed, changes with difficulty
let aiSpeed = 3; // Default AI speed
let playerHealth = 5;
let aiHealth = 5;
let timer = 0;
let timerInterval;
let rouletteResult = null;
let activePowerUps = { player: null, ai: null };


// Paddle properties
const paddleWidth = 10;
const paddleHeight = 100;
const playerPaddle = {
    x: 10,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    dy: 5
};

const aiPaddle = {
    x: canvas.width - 20,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    dy: aiSpeed
};

// Ball properties
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 10, // Made the ball larger
    dx: ballSpeed,
    dy: ballSpeed - 1
};

// Controls
let upPressed = false;
let downPressed = false;

function drawPaddle(x, y, width, height) {
    context.fillStyle = "#fff";
    context.fillRect(x, y, width, height);
}

function drawBall(x, y, radius) {
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI * 2);
    context.fillStyle = "#fff";
    context.fill();
    context.closePath();
}

function movePaddle() {
    if (upPressed && playerPaddle.y > 0) {
        playerPaddle.y -= playerPaddle.dy;
    }
    if (downPressed && playerPaddle.y < canvas.height - playerPaddle.height) {
        playerPaddle.y += playerPaddle.dy;
    }
}

function moveAIPaddle() {
    // AI tracks the ball with varying accuracy based on difficulty
    if (ball.y < aiPaddle.y + aiPaddle.height / 2) {
        aiPaddle.y -= aiPaddle.dy;
    } else if (ball.y > aiPaddle.y + aiPaddle.height / 2) {
        aiPaddle.y += aiPaddle.dy;
    }

    // Keep the AI paddle within canvas bounds
    aiPaddle.y = Math.max(0, Math.min(canvas.height - aiPaddle.height, aiPaddle.y));
}

function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Ball bounces off top and bottom walls
    if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
        ball.dy *= -1;
    }

    // Ball hits player paddle
    if (
        ball.x - ball.radius < playerPaddle.x + playerPaddle.width &&
        ball.y > playerPaddle.y &&
        ball.y < playerPaddle.y + playerPaddle.height
    ) {
        ball.dx *= -1;
        score += 1;
    }

    // Ball hits AI paddle
    if (
        ball.x + ball.radius > aiPaddle.x &&
        ball.y > aiPaddle.y &&
        ball.y < aiPaddle.y + aiPaddle.height
    ) {
        ball.dx *= -1;
    }

    // Game over if ball goes past player paddle
    if (ball.x - ball.radius < 0 || ball.x + ball.radius > canvas.width) {
        gameOver();
    }
}

function gameOver() {
    gameRunning = false;
    canvas.style.display = "none";
    gameOverScreen.style.display = "block";
    scoreDisplay.textContent = score;
}

function startTimer() {
    timerInterval = setInterval(() => {
        timer++;
        document.getElementById("timer").textContent = formatTime(timer);
    }, 1000);
}

// Helper function to format time as mm:ss
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
}

function spinRoulette() {
    const prizes = ["Nothing", "Double Balls", "Extra Health", "Triple Damage", "Lightning Ball"];
    const result = prizes[Math.floor(Math.random() * prizes.length)];
    document.getElementById("resultDisplay").textContent = `You won: ${result}`;
    return result;
}

function applyRouletteEffect(effect, concedingPlayer) {
    if (effect === "Nothing") return;

    if (effect === "Double Balls") {
        addExtraBall();
    } else if (effect === "Extra Health") {
        if (concedingPlayer === "player") {
            playerHealth = Math.min(5, playerHealth + 1);
        } else {
            aiHealth = Math.min(5, aiHealth + 1);
        }
    } else if (effect === "Triple Damage") {
        activePowerUps[concedingPlayer] = "Triple Damage";
        setTimeout(() => { activePowerUps[concedingPlayer] = null; }, 10000); // Lasts 10 seconds
    } else if (effect === "Lightning Ball") {
        activePowerUps[concedingPlayer] = "Lightning Ball";
    }
    updateHealthDisplay();
}

function updateHealthDisplay() {
    document.getElementById("playerHealth").textContent = `Player Health: ${playerHealth}`;
    document.getElementById("aiHealth").textContent = `AI Health: ${aiHealth}`;
}

function checkGameOver() {
    if (playerHealth <= 0 || aiHealth <= 0) {
        clearInterval(timerInterval);
        alert(playerHealth <= 0 ? "AI Wins!" : "Player Wins!");
        resetGame();
    }
}

function addExtraBall() {
    let extraBall = { x: canvas.width / 2, y: canvas.height / 2, dx: ball.dx, dy: ball.dy, radius: 10 };
    balls.push(extraBall); // Assume balls is an array holding active balls
}

function resetGame() {
    playerHealth = 5;
    aiHealth = 5;
    timer = 0;
    balls = [ball]; // Reset to a single ball
    startTimer();
    updateHealthDisplay();
}

function onScore(concedingPlayer) {
    if (concedingPlayer === "player") aiHealth--;
    else playerHealth--;

    // Show roulette screen and apply effects
    canvas.style.display = "none";
    document.getElementById("rouletteScreen").style.display = "block";

    document.getElementById("spinButton").onclick = () => {
        rouletteResult = spinRoulette();
        document.getElementById("rouletteScreen").style.display = "none";
        canvas.style.display = "block";
        applyRouletteEffect(rouletteResult, concedingPlayer);
        checkGameOver();
    };
}

function resetGame() {
    score = 0;
    playerPaddle.y = canvas.height / 2 - paddleHeight / 2;
    aiPaddle.y = canvas.height / 2 - paddleHeight / 2;
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;

    // Set ball speed and AI paddle speed based on selected difficulty
    switch (difficultySelect.value) {
        case "easy":
            ball.dx = 4;
            ball.dy = 3;
            aiPaddle.dy = 2; // Slowest AI speed
            break;
        case "medium":
            ball.dx = 6;
            ball.dy = 5;
            aiPaddle.dy = 4; // Moderate AI speed
            break;
        case "hard":
            ball.dx = 8;
            ball.dy = 7;
            aiPaddle.dy = 6; // Fastest AI speed
            break;
    }
}

function gameLoop() {
    if (gameRunning) {
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawPaddle(playerPaddle.x, playerPaddle.y, playerPaddle.width, playerPaddle.height);
        drawPaddle(aiPaddle.x, aiPaddle.y, aiPaddle.width, aiPaddle.height);
        balls.forEach((ball) => drawBall(ball.x, ball.y, ball.radius)); // Track multiple balls

        // AI paddle and player paddle movement
        movePaddle();
        moveAIPaddle();

        // Ball movement logic with added effect
        balls.forEach(moveBall);

        requestAnimationFrame(gameLoop);
    }
}

document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowUp") upPressed = true;
    if (event.key === "ArrowDown") downPressed = true;
});

document.addEventListener("keyup", (event) => {
    if (event.key === "ArrowUp") upPressed = false;
    if (event.key === "ArrowDown") downPressed = false;
});

startButton.addEventListener("click", () => {
    menuScreen.style.display = "none";
    canvas.style.display = "block";
    gameRunning = true;
    resetGame();
    gameLoop();
});

restartButton.addEventListener("click", () => {
    gameOverScreen.style.display = "none";
    canvas.style.display = "block";
    gameRunning = true;
    resetGame();
    gameLoop();
});
