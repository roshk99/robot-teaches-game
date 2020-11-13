var tID; //we will use this variable to clear the setInterval()

function stopAnimate() {
  clearInterval(tID);
} //end of stopAnimate()


function animateScript(initialposition, interval, diff, maxposition, image_id) {

  var position = initialposition; //start position for the image slicer
//   const interval = 100; //100 ms of interval for the setInterval()
//   const diff = 222; //diff as a variable for position offset
  
  tID = setInterval(() => {
  
    document.getElementById(image_id).style.backgroundPosition =
      `-${position}px 0px`;
    //we use the ES6 template literal to insert the variable "position"
    
    if (position < maxposition) {
      position = position + diff;
    }
    //we increment the position by 256 each time
    else {
      position = initialposition;
    }
    //reset the position to 256px, once position exceeds 1536px
    
  }, interval); //end of setInterval
} //end of animateScript()
