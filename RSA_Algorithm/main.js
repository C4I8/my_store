let fs = require("fs");
/**大质数发生器 */
function primeGenerate(N){
    let primes = [];
    for(let i = 2;i<=N;i++){
        let prime = true;
        for(let j = 2;j<i;j++){
            if(i % j == 0){
                prime = false;
                break;
            }
        }
        if(prime){
            primes.push(i);
        }
    }
    fs.writeFile("./json/prime.json",primes.toString(),()=>{
        console.log(`prime.json write success`);
    });
    return primes;
}
let startTime = Date.now();
primeGenerate(99999999999);
let endTime = Date.now();
console.log(`duration: ${endTime - startTime}`);