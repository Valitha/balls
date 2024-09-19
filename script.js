let balls = [];
let rectangles = [];
let smallRects = [];
let teamACollisions = 0;
let teamBCollisions = 0;
const ballRadius = 20;
const numBalls = 10;
const gravity = 0.2;
const elasticity = 0.8;
const erraticForce = 0.1;

function setup() {
    createCanvas(800, 600);
    for (let i = 0; i < numBalls; i++) {
        let pos = createVector(random(ballRadius, width - ballRadius), random(ballRadius, height - ballRadius));
        let velocity = createVector(random(-1.5, 1.5), random(-1.5, 1.5));
        let team = (i < numBalls / 2) ? 'A' : 'B';
        balls.push({ pos, velocity, team, collisions: 0 });
    }

    // Add moving rectangles
    rectangles.push({ pos: createVector(100, 200), size: createVector(150, 30), velocity: createVector(2, 0) });
    rectangles.push({ pos: createVector(500, 400), size: createVector(200, 30), velocity: createVector(-2, 0) });

    // Add small moving rectangles
    for (let i = 0; i < 10; i++) {
        let rectSize = createVector(random(20, 40), random(10, 20));
        let rectPos = createVector(random(0, width - rectSize.x), random(0, height - rectSize.y));
        let rectVelocity = createVector(random(-2, 2), random(-2, 2));
        smallRects.push({ pos: rectPos, size: rectSize, velocity: rectVelocity });
    }
}

function draw() {
    background(255, 192, 203); // Light pink

    // Update and draw rectangles
    rectangles.forEach(rect => {
        rect.pos.add(rect.velocity);
        if (rect.pos.x < 0 || rect.pos.x + rect.size.x > width) {
            rect.velocity.x *= -1;
        }
        rect(pos.x, pos.y, rect.size.x, rect.size.y);
    });

    smallRects.forEach(rect => {
        rect.pos.add(rect.velocity);
        if (rect.pos.x < 0 || rect.pos.x + rect.size.x > width) {
            rect.velocity.x *= -1;
        }
        if (rect.pos.y < 0 || rect.pos.y + rect.size.y > height) {
            rect.velocity.y *= -1;
        }
        rect(rect.pos.x, rect.pos.y, rect.size.x, rect.size.y);
    });

    // Update and draw balls
    balls.forEach(ball => {
        ball.velocity.y += gravity;
        ball.velocity.x += random(-erraticForce / 2, erraticForce / 2);
        ball.velocity.y += random(-erraticForce / 2, erraticForce / 2);

        ball.pos.add(ball.velocity);

        // Wall collisions
        if (ball.pos.x - ballRadius < 0) {
            ball.pos.x = ballRadius;
            ball.velocity.x *= -elasticity;
        } else if (ball.pos.x + ballRadius > width) {
            ball.pos.x = width - ballRadius;
            ball.velocity.x *= -elasticity;
        }

        if (ball.pos.y - ballRadius < 0) {
            ball.pos.y = ballRadius;
            ball.velocity.y *= -elasticity;
        } else if (ball.pos.y + ballRadius > height) {
            ball.pos.y = height - ballRadius;
            ball.velocity.y *= -elasticity;
        }

        // Rectangle collisions
        rectangles.forEach(rect => {
            if (ball.pos.x > rect.pos.x && ball.pos.x < rect.pos.x + rect.size.x &&
                ball.pos.y + ballRadius > rect.pos.y && ball.pos.y - ballRadius < rect.pos.y + rect.size.y) {
                ball.velocity.y *= -elasticity;
                ball.pos.y = rect.pos.y - ballRadius;
                ball.collisions++;
                if (ball.team === 'A') teamACollisions++;
                else teamBCollisions++;
            }
        });

        smallRects.forEach(rect => {
            if (ball.pos.x > rect.pos.x && ball.pos.x < rect.pos.x + rect.size.x &&
                ball.pos.y + ballRadius > rect.pos.y && ball.pos.y - ballRadius < rect.pos.y + rect.size.y) {
                ball.velocity.y *= -elasticity;
                ball.pos.y = rect.pos.y - ballRadius;
                ball.collisions++;
                if (ball.team === 'A') teamACollisions++;
                else teamBCollisions++;
            }
        });

        fill(ball.team === 'A' ? 186 : 148, 85, 211);
        ellipse(ball.pos.x, ball.pos.y, ballRadius * 2);
    });

    // Display collision counters
    fill(0);
    textSize(20);
    text(`Team A Collisions: ${teamACollisions}`, 10, 30);
    text(`Team B Collisions: ${teamBCollisions}`, 10, 60);
}
