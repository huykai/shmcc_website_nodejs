var fs = require("fs");
var path = require("path");
//var resultdir = "E:/PersonalProject/Code_Projects/Javascripts/AngularJS_Demo/shmcc/app/"

var resultFileParams = '';
var resultFileName = '';
var resultFileDir = '';

if (process.argv.length < 3) {
    console.log(JSON.stringify({"errorinfo":"getCgCdr need parameter! getCgCdr resultfilename"}));
    process.exit(1);
} else {
    resultFileParams = process.argv[2];
    resultFileDir = path.dirname(resultFileName)
    resultFileName = path.basename(resultFileName)
}

var resultData = [];
var resultFiles = [];
try {
    fs.readdir(resultFileDir, (err, files) => {
        if (err) { 
            console.log(JSON.stringify({"errorinfo":"getCgCdr resultfiledir have errors ! \n" + err}));
            process.exit(1);
        };
        resultFiles = files;
    })
     
} catch (err) { 
    console.log(JSON.stringify({"errorinfo":"getCgCdr params have errors ! \n" + err}));
    process.exit(1);
}

try {
    if (resultFiles.length <= 0) {
        console.log(JSON.stringify({"errorinfo":"getCgCdr resultFile can not found!"}));
        process.exit(1);
    } else {
        for (let resultFile of resultFiles) {
            let resultFileStr = resultFile.split('-')
            if (resultFileStr[0] === resultFileName && resultFileStr[1] != '') {
                console.log('resultFile: ', resultFile);
                let resultDataRecord = {};
                resultDataRecord.hostname = resultFileStr[1];
                getResultDataInfo(resultData, resultFile, resultDataRecord)
            }
        }
    }
    
} catch (err) {
    console.log(JSON.stringify({"errorinfo":"getCgCdr parse resultFile have error! \n" + err}));
    process.exit(1);
}

getResultDataInfo = function(resultData, resultFile, resultDataRecord) {
    try {
        let data = fs.readFileSync(resultFile, data)
        let result = JSON.parse(data)
        resultDataRecord.columns = result[0].keys();
        resultDataRecord.datas = result;
        resultData.push(resultDataRecord);
        return;
    } catch (err) {
        console.log(JSON.stringify({"errorinfo":"getCgCdr parse " + resultFile + " have error! \n" + err}));
        return;
    }
}

