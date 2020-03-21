const fs = require("fs");
fs.readFile("./video/random.mp3",(err,data)=>{
    console.log(data);
    let bytes = new Uint8Array(data);
    let str = "";
    for(let i = 0;i < 10;i++){
       console.log(bytes[i])
    }
    console.log(bytes.length)
});

function randomInt(start,end){
    return start + Math.random()*(end - start);
}
let data = [73,68,51];
// let len = 20000;
// while(len > 0){
//     len--;
//     data.push(randomInt(0,256));
// }
// let buffer = Buffer.from(data);
// fs.writeFile("./video/random.mp3",buffer,()=>{
//     console.log("random write success")
// })
