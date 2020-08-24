import "https://d3js.org/d3.v5.min.js"

Promise.all([
    d3.json("/data/cards.json"),
    
]).then(function([cards]) {
    console.log(cards)
});