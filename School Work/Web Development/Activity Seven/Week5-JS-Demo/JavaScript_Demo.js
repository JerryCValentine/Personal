/*Example of JS event handlers for handling various events connected to HTML DOM elements */

/*These onload event occurs when the web page has loaded all its content*/
window.onload = function() {

	document.getElementById("item").onmouseover = changeImage;
	document.getElementById("item").onclick = changeImage2;
	document.getElementById("foot").onmouseover = changeStyle;
	document.getElementById("foot").onmouseout = changeStyle2;
	document.getElementById("header").onclick = changeName; 
	//changeImage();
};


/*This function is called when we hoven our mouse over the image item2.jpg*/
function changeImage() {
	document.getElementById("item").src = "item3.jpg";
}
/*This function is called when we click on the image item3.jpg*/
function changeImage2() {
	document.getElementById("item").src = "item2.jpg";
}

/*This function is called when we click on the head of the webpage*/
function changeName() {
	var input = window.prompt("Enter your name:", "");
	
	if (input == "" ){
		document.getElementById("header").innerHTML = "My Photo Album";
	} else {
		document.getElementById("header").innerHTML = input + "`s Photo Album";
	}
}

/*This function is called when we hoven our mouse over the the footer section*/
function changeStyle() {
	document.getElementById("foot").style.border = "solid 10px white";
	document.getElementById("foot").style.backgroundColor = "blue";
}

/*This function is called when we hoven out our mouse from the the footer section*/
function changeStyle2() {
	document.getElementById("foot").style.border = "none";
	document.getElementById("foot").style.backgroundColor = "red";
}