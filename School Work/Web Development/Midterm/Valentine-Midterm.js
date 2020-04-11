var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
var expenditure = [20, 12, 15, 10, 30, 25, 40 ];

var $ = function(id) { return document.getElementById(id); };

function updateExpenditure(){
    var day = $("day");
    var number = $("expenditure");

    if(isNaN(parseInt(number.value))){
        alert("Enter a valid number");
    }
    else
    {
        for (let index = 0; index < days.length; index++) {
            if(day.value == days[index]){
                day = index;
            }
        }

        expenditure[day] += parseInt(number.value);
        number.value = "";
        alert("Your updated expenditures are: "  + expenditure);
    }
}

function showTotalExp(){
    var heightTable = $("totalExpenditure");
    var total = 0;
    for (let i = 0; i < expenditure.length; i++) {
        total += expenditure[i];
    }
    heightTable.value = total;
    heightTable.style.color = "red";
}

function showMax(){
    var showsMax = $("showMax");
    var max = expenditure[0];
    var maxIndex = 0;
    for (let i = 1; i < expenditure.length; i++) {
        if(max < expenditure[i]){
            max = expenditure[i];
            maxIndex = i;
        }
    }
    var textnode = document.createTextNode("Your maximum expenditure is $" + max + " on " + days[maxIndex]);
    showsMax.appendChild(textnode)
}

window.onload = function() {
    $("update").onclick = updateExpenditure;
    $("total").onclick = showTotalExp;
    $("show_max").onmouseover = showMax;
};
