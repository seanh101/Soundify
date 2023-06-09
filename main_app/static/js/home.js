


// Based on The Coding Train: Coding Challenge #136.1: Polar Perlin Noise Loops
// https://www.youtube.com/watch?v=ZI1dmHv3MeM
let phase = 0;
let noiseMax = 1;
let slider;
let zOff = 0;

let canvasY = window.innerHeight * .8;
let canvasX = window.innerWidth * .6;


function setup() {
    let canvasLogin = createCanvas(canvasX, canvasY);
    canvasLogin.parent("home-soundwave");

    // let canvasHome = createCanvas(600, 200);
    // canvasHome.parent("home-soundwave");

    background("#e9e0f0");

    // slider = createSlider(2, 10, 0, 0.1);
    // strokeWeight(4);
}

function draw() {
    //noLoop();
    background("#9B71F6");
    translate(width / 2, height * 0.8);

    //stroke(255);
    stroke("#D6F050");
    strokeWeight(1.5)
    noFill();

    noiseMax = 10;
    // let xOff = 0;

    for (let i = 1; i < 10; i++) {
        beginShape();
        for (let a = 0; a < TWO_PI; a += 0.05) {
            //// let r = 100;//random (50, 100)

            let xOff = map(cos(a + phase), -1, 20, 0, noiseMax);
            let yOff = map(sin(a + phase), -1, 0.5, 0, noiseMax);
            let r = map(noise(xOff, yOff, zOff * .5), 0, 1, 100, 200) * (i * 0.1);
            let x = r * 4 * cos(a);
            let y = r * 2 * sin(a);
            vertex(x, y);
            // xOff = xOff + 0.01
        }
        endShape(CLOSE);
    }
    phase += 0.005;
    zOff += 0.1;
    //  xOff = xOff + 0.01
}


