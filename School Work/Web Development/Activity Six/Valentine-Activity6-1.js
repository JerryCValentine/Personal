function displayGrades(){
    var input;
    do{
        input = prompt("Enter number grade from 0 through 120\nOr enter -1 to end entries");
        if(isNaN(input)){ // Skip if not a number
            alert("ERROR: DIDN'T ENTER A NUMBER");
            continue;
        }
        else if(input < -1 || input > 120){ // Skip if not between 0 and 120
            alert("ERROR: NUMBER WASN'T BETWEEN 0 AND 120");
            continue;
        }
        else if(input == -1){// Skip grading alert if input is -1
            continue;
        }

        alert("Number grade = " + input + "\nLetter grade = " + replaceGrades(input));

    }while(input != -1)
}

function replaceGrades(grade){
    if(grade >= 90){ // Grade A
        return "A";
    }
    else if(grade >= 80){ // Grade B
        return "B";
    }
    else if(grade >= 70){ // Grade C
        return "C";
    }
    else if(grade >= 60){ // Grade D
        return "D";
    }
    else{ // Grade F
        return "F";
    }
}