const canvas = document.getElementById("confetti");

const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;

canvas.height = window.innerHeight;

let particles = [];

const cells = document.querySelectorAll(".cell");

const button = document.querySelector(".play-btn");

const modal = document.getElementById("winner-modal");

const winnerText = document.getElementById("winner-text");

const playAgain = document.getElementById("play-again");

let currentPlayer = "X";

let board = ["","","","","","","","",""];

let gameRunning = true;

const wins = [

    [0,1,2],
    [3,4,5],
    [6,7,8],

    [0,3,6],
    [1,4,7],
    [2,5,8],

    [0,4,8],
    [2,4,6]

];

createTurnLabel();

cells.forEach((cell,index)=>{

    cell.addEventListener("click",()=>play(index));

});

button.onclick=resetGame;

function play(index){

    if(!gameRunning) return;

    if(board[index]!="") return;

    board[index]=currentPlayer;

    cells[index].innerHTML=currentPlayer;

    cells[index].classList.add(currentPlayer.toLowerCase());

    cells[index].classList.add("pop");

    if(checkWinner()){

        winnerText.innerHTML="🏆 Player "+currentPlayer+" Wins!";

        modal.classList.add("show");
        launchConfetti();

        gameRunning=false;

        return;

    }

    if(board.every(cell=>cell!="")){

        winnerText.innerHTML="🤝 It's a Draw!";

        modal.classList.add("show");

        gameRunning=false;

        return;

    }

    currentPlayer=currentPlayer=="X"?"O":"X";

    document.getElementById("turn").innerHTML=
    "Player "+currentPlayer+"'s Turn";

}

function checkWinner(){

    for(let win of wins){

        const[a,b,c]=win;

        if(board[a]!=""&&
           board[a]==board[b]&&
           board[a]==board[c]){

            cells[a].classList.add("winner");
            cells[b].classList.add("winner");
            cells[c].classList.add("winner");

            return true;

        }

    }

    return false;

}

function resetGame(){

    board=["","","","","","","","",""];

    currentPlayer="X";

    gameRunning=true;

    cells.forEach(cell=>{

        cell.innerHTML="";

        cell.className="cell";

    });

    document.getElementById("turn").innerHTML=
    "Player X's Turn";

}

function createTurnLabel(){

    const board=document.querySelector(".board");

    const label=document.createElement("h2");

    label.id="turn";

    label.innerHTML="Player X's Turn";

    board.parentNode.insertBefore(label,board);

}

playAgain.onclick=()=>{

    modal.classList.remove("show");

    resetGame();

};

function launchConfetti(){

    particles=[];

    for(let i=0;i<180;i++){

        particles.push({

            x:canvas.width/2,

            y:120,

            size:Math.random()*8+4,

            speedX:(Math.random()-0.5)*12,

            speedY:Math.random()*-12,

            gravity:0.25,

            color:`hsl(${Math.random()*360},100%,60%)`

        });

    }

    animateConfetti();

}

function animateConfetti(){

    ctx.clearRect(0,0,canvas.width,canvas.height);

    particles.forEach(p=>{

        p.x+=p.speedX;

        p.y+=p.speedY;

        p.speedY+=p.gravity;

        ctx.fillStyle=p.color;

        ctx.fillRect(p.x,p.y,p.size,p.size);

    });

    particles=particles.filter(p=>p.y<canvas.height+30);

    if(particles.length){

        requestAnimationFrame(animateConfetti);

    }

}
