const allconfig = require("./src/config");
const xlsx = require("node-xlsx").default;
const fs = require("fs");
const input = "./input/WB01_Data.xlsx";
const output = "./output/";
const seedfilename = "SD_AllSeeds_Copy.json";
const enumfilename = "GEnum.ts";

class main {
    rawdata = null;
    jsondata = {};
    jsonmap = new Map();
    constructor() {
        let ts = this;
        let date = new Date();
        ts.jsondata.version = (date.getTime() / 1000) >> 0;
        ts.jsondata.createTime = `${date.getFullYear()}/${date.getMonth()}/${date.getDay()} ${padleft(date.getHours())}:${padleft(date.getMinutes())}:${padleft(date.getSeconds())}`;
        ts.rawdata = xlsx.parse(input);
        for (let sheetindex in ts.rawdata) {
            let sheetdata = ts.rawdata[sheetindex];
            ts.parsesheet(sheetdata);
        }
        ts.map2json();
        ts.json2subjson();
        
        fs.writeFileSync(output + seedfilename, JSON.stringify(ts.jsondata))
        console.log("写入种子完成");
    }

    parsesheet(sheetdata) {
        let ts = this;
        let data = ts.parse2column(sheetdata.data);
        if(sheetdata.name == "枚举") {
            ts.generateEnum(data);
            return;
        }
        if(sheetdata.name == "音效表"){
            // ts.parseSound(data);
            return;
        }
        if(sheetdata.name == "克制表"){
            // ts.parserRtrictions(sheetdata.data);
            return;
        }
        let sheetnamestr = allconfig.sheetconfig[sheetdata.name];
        let configdata = ts.getsheetconfig(sheetnamestr);
        let config = configdata.config;
        let type = configdata.type;
        if(!config) return;
        ts.initsheetobj(data, sheetnamestr, type);
        let sheetmap = ts.jsonmap.get(sheetnamestr);
        for (let columnindex = 0; columnindex < data.length; columnindex++) {
            let columndata = data[columnindex];
            let itemname;
            let itemtype;
            let itemmap;
            let itemmapiter;
            for (let rowindex = 0; rowindex < columndata.length; rowindex++) {
                let item = columndata[rowindex];
                if (rowindex == 0) {
                    let itemconfig = config[item];
                    if (!itemconfig) {
                        console.log(item, "has no config");
                        break;
                    }
                    itemname = itemconfig[0];
                    itemtype = itemconfig[1];
                    itemmapiter = sheetmap.keys();
                    continue;
                }
                itemmap = sheetmap.get(itemmapiter.next().value);
                itemmap && itemmap.set(itemname, ts.format(item, itemtype))
            }
        }
    }

    /**枚举 */
    generateEnum(data) {
        let content = "";
        this.clearredundancy(data);
        for (let columnindex = 0; columnindex < data.length; columnindex++) {
            let columndata = data[columnindex];
            for (let rowindex = 0; rowindex < columndata.length; rowindex++) {
                let itemdata = columndata[rowindex];
                if (rowindex == 0) {
                    content += `const enum ${itemdata} {`;
                    continue;
                }
                let item2arr = itemdata.split(".");
                content += `\n    ${item2arr[1]} = ${item2arr[0]},`;
                if (rowindex == columndata.length - 1) {
                    content += `\n}\n\n`;
                }
            }
        }
        fs.writeFileSync(output + enumfilename, content);
        console.log("枚举写入完成")
    }

    /**音效 */
    parseSound(data){
        let ts = this;
        let dict = {};
        ts.jsondata.soundDict = {dict : dict};
        let firstcolumn = data[0];
        for (let columnindex = 1; columnindex < data.length; columnindex++) {
            let columndata = data[columnindex];
            let columnname = "";
            for (let rowindex = 0; rowindex < columndata.length; rowindex++) {
                let item = columndata[rowindex];
                let rowname = firstcolumn[rowindex];
                if(rowindex == 0){
                    columnname = item;
                    continue;
                }
                dict[columnname + "_" + rowname] = item;
            }
        }
    }

    /**
     * 克制表
     */
    parserRtrictions(data){
        let ts = this;
        let mainarr = []
        ts.jsondata.restrictions = mainarr;
        for(let i = 0;i<6;i++){
            mainarr[i] = [];
            for(let j = 0;j<6;j++){
                mainarr[i][j] = 0;
            }
        }
        for(let rowindex = 1;rowindex<data.length;rowindex++){
            let rowdata = data[rowindex];
            let index0 = 0;
            let index1 = 0;
            let value = 0;
            for(let columnindex=0;columnindex<rowdata.length;columnindex++){
                let item = rowdata[columnindex];
                if(columnindex == 0) index0 = ts.format(item,"int_split");
                if(columnindex == 1) index1 = ts.format(item,"int_split");
                if(columnindex == 2) value = ts.format(item,"number");
                mainarr[index0][index1] = value;
            }
        }
    }

    /**剧情表 */
    map2jsonPlotsdic(sheetmap,sheetjson){
        let ts = this;
        let datadealed = {};
        sheetmap.forEach((itemmap, itemkey) => {
            let itemjson = sheetjson[itemkey];
            itemmap.forEach((value, attr) => {
                itemjson[attr] = value;
            });
            let itemarr = datadealed[""+itemjson.id];
            if(!itemarr || typeof itemarr["length"] == "undefined"){
                itemarr = datadealed[""+itemjson.id] = [];
            } 
            itemarr.push(itemjson)
            delete sheetjson[itemkey];

        });
        ts.jsondata["plotsdic"] = datadealed;
    }

    /**
     * 解析成列结构
     */
    parse2column(data) {
        let alldata = [];
        for (let rowindex = 0; rowindex < data.length; rowindex++) {
            let rowdata = data[rowindex];
            for (let columnindex = 0; columnindex < rowdata.length; columnindex++) {
                if (!alldata[columnindex]) {
                    alldata[columnindex] = [];
                }
                alldata[columnindex].push(rowdata[columnindex]);
            }
        }
        return alldata;
    }

    /**
     * 初始化sheet obj general
     */
    initsheetobj(data, sheetnamestr, type) {
        let ts = this;
        let sheetobj = {};
        let sheetmap = new Map();
        ts.jsonmap.set(sheetnamestr, sheetmap);
        ts.jsondata[sheetnamestr] = sheetobj;
        let ids = data[0];
        for (let columnindex = 0; columnindex < ids.length; columnindex++) {
            let item = ids[columnindex];
            if (columnindex == 0) continue;
            let itemname;
            if (type == "main") {
                itemname = item;
            }
            if (type == "sub" || type == "main_plotsdic") {
                itemname = columnindex;
            }
            sheetobj["" + itemname] = {};
            sheetmap.set("" + itemname, new Map());
        }
    }

    map2json() {
        let ts = this;
        ts.jsonmap.forEach((sheetmap, sheetkey) => {
            let sheetjson = ts.jsondata[sheetkey];
            if(sheetkey == "plotsdic"){
                ts.map2jsonPlotsdic(sheetmap,sheetjson);
                return;
            }
            sheetmap.forEach((itemmap, itemkey) => {
                let itemjson = sheetjson[itemkey];
                itemmap.forEach((value, attr) => {
                    itemjson[attr] = value;
                });
            });
        })
    }

    json2subjson() {
        let ts = this;
        let sheetconfigsub = allconfig.sheetconfigsub;
        for (let key in sheetconfigsub) {
            let config = sheetconfigsub[key];
            let parent = key;
            let son = config.sonsheetname;
            let parentindexname = config.parentindexname;
            let sonindexname = config.sonindexname;
            let attr = config.attr;
            ts.mergesheet(parent, son, parentindexname, sonindexname, attr);
        }
    }

    mergesheet(parent, son, parentindexname, sonindexname, attr) {
        let ts = this;
        let mainsheetobj = ts.jsondata[parent];
        let subsheetobj = ts.jsondata[son];
        for (let subkey in subsheetobj) {
            let subitem = subsheetobj[subkey];
            for (let mainkey in mainsheetobj) {
                let mainitem = mainsheetobj[mainkey];
                if (subitem[sonindexname] == mainitem[parentindexname]) {
                    if (!mainitem[attr]) {
                        mainitem[attr] = [];
                    }
                    mainitem[attr].push(subitem);
                    break;
                }
            }
        }
        delete ts.jsondata[son];
    }

    /**
     * 获取sheet配置
     */
    getsheetconfig(sheetnamestr) {
        let sheetconfigsub = allconfig.sheetconfigsub;
        let config = allconfig[sheetnamestr];
        let ret = {
            config: config,
            type: "main"
        };
        if (!config) {
            for (let key in sheetconfigsub) {
                let itemconfigsub = sheetconfigsub[key];
                if (itemconfigsub.sonsheetname == sheetnamestr) {
                    ret.config = allconfig[itemconfigsub.sonconfig];
                    ret.type = "sub";
                    break;
                }
            }
        }
        if(sheetnamestr == "plotsdic"){
            ret.type = "main_plotsdic"
        }
        return ret;
    }


    /**
     * 清除冗余
     */
    clearredundancy(data) {
        for (let columnindex = 0; columnindex < data.length; columnindex++) {
            let columndata = data[columnindex];
            let rowindex = columndata.length - 1;
            while (rowindex > -1 && typeof columndata[rowindex] == "undefined") {
                columndata.splice(rowindex, 1);
                rowindex--;
            }
        }
    }

    /**
     * 格式转换
     */
    format(item, itemtype) {
        let ret = "" + item;
        switch (itemtype) {
            case "number":
                ret = +item;
                if (typeof item == "undefined") {
                    ret = 0;
                }
                ret = +ret.toFixed(2);
                break;
            case "int_split":
                ret = +(item.split(".")[0]);
                if (typeof item == "undefined") {
                    ret = 0;
                }
                break;
            case "int_array":
                ret = ("" + item).split(",");
                for (let intarrindex = 0; intarrindex < ret.length; intarrindex++) {
                    ret[intarrindex] = +ret[intarrindex];
                }
                if (typeof item == "undefined") {
                    ret = [];
                }
                break;
            case "string":
                if (ret === "\\0") {
                    ret = "";
                }
                if (typeof item == "undefined") {
                    ret = "";
                }
                break;
            default:
                break;
        }
        return ret;
    }
}
new main();

function padleft(value) {
    if (value < 10)
        return "0" + value;
    return "" + value;
}