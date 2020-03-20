const xlsx = require("node-xlsx").default;
let list = xlsx.parse("./excel/data.xlsx");
console.log(list[0].data);
