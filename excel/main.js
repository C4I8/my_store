const xlsx = require("node-xlsx").default;
const fs = require("fs");

let list = xlsx.parse("./excel/data.xlsx");
fs.writeFile("./excel/json/data.json",JSON.stringify(list),(res)=>{
    console.log(`writeFile data.json success ${res}`);
})
