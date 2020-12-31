const xlsx = require("node-xlsx").default;
const fs = require("fs");

let list = xlsx.parse("./excel/data.xlsx");
fs.writeFileSync("./excel/json/data.json",JSON.stringify(list))
