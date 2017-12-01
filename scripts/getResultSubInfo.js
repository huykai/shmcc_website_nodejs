var fs = require("fs");

var resultdir = "E:/PersonalProject/Code_Projects/Javascripts/AngularJS_Demo/shmcc/app/"

if (process.argv.length < 2) {
    console.log(JSON.stringify({"errorinfo":"getResultSubInfo need parameter!"}));
    process.exit(1);
}

params = process.argv[2];
var params_json ;
var resultFileName = '';
var page_str = "1";
var rows_str = "50";
var page = 1;
var rows = 50;
try {
    params_json = JSON.parse(params);
    resultFileName = resultdir + params_json.resultFile || '';
    page = parseInt(params_json.page || page_str);
    rows = parseInt(params_json.rows || rows_str); 
} catch (err) { 
    console.log(JSON.stringify({"errorinfo":"getResultSubInfo params have errors in json parse! \n" + err}));
    process.exit(1);
}

try {
    if (resultFileName === '') {
        console.log(JSON.stringify({"errorinfo":"getResultSubInfo params resultFileName should not be null!"}));
        process.exit(1);
    };
    //console.log(resultFileName);
    var resultFile = '';
    resultFile = fs.readFileSync(resultFileName)
    
    
    var jsonResult = JSON.parse(resultFile);
    var row_begin = (page - 1) * rows > jsonResult.rows.length ? jsonResult.rows.length: (page - 1) * rows; 
    var row_end = page * rows > jsonResult.rows.length ? jsonResult.rows.length: page * rows; 
    
    return_rows = jsonResult.rows.slice(row_begin, row_end);
    
    return_result = {"total":jsonResult.total, "rows" : return_rows};
    console.log(JSON.stringify(return_result));


} catch (err) {
    console.log(JSON.stringify({"errorinfo":"getResultSubInfo parse resultFile have error! \n" + err}));
    process.exit(1);
}
