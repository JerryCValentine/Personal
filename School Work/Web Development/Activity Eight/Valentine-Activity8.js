var names = ["Tom", "Lily", "Jose", "Sarah"];
var height = [65, 60, 72, 68];

var $ = function (id) { return document.getElementById(id); };

function showResult(){
    var tallestIndex = 0;
    var avg;
    avg = 0;
    for (let i = 0; i < height.length; i++) {
        avg += height[i];
        if(height[tallestIndex] < height[i]){
            tallestIndex = i;
        }
    }
    avg = avg / height.length;

    $("result").innerHTML = "<h2>Results</h2><p>Average Height = " + avg + "<br>Highest height = " + names[tallestIndex] + " with a height of " + height[tallestIndex] + "</p>";
};

function displayHeight(){
    var heightTable = $("height_table");
    heightTable.innerHTML = "<h2>Heights</h2><table><tr><td><b>Name<b></td><td><b>Heights<b></td></tr>";
    for (let i = 0; i < height.length; i++) {
        heightTable.innerHTML += "<tr><td>" + names[i] + "</td><td>" + height[i] + "</td></tr>"
    }
};

function addHeight(){
    var textName = $("name");
    var textHeight = $("height");

    if(textName.value === ""){
        window.alert("Name Field Is Empty");
        textName.focus();
    }else if(textHeight.value === ""){
        window.alert("Height Field Is Empty");
        textHeight.focus();
    }else if(isNaN(textHeight.value)){
        window.alert("Height Field Must Be A Number");
        textHeight.focus();
    }else if(textHeight.value < 0 || textHeight.value > 100){
        window.alert("Height Field Must Be Between 0 And 100");
        textHeight.focus();
    }else{
        names.push(textName.value);
        height.push(parseInt(textHeight.value));
    
        textName.value = "";
        textHeight.value = "";

        textName.focus();
    }
};

window.onload = function () {
    $("show_results").onclick = showResult;
    $("add").onclick = addHeight;
    $("display_height").onclick = displayHeight;
    $("name").focus();
};

