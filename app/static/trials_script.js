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

function $(id) {
    return document.getElementById(id);
};

var bins = document.getElementsByClassName("bin");
dragArr = [$("staging")]
for (i = 0; i < bins.length; i++) {
    dragArr[i + 1] = $(bins[i].id);
}
var drake = dragula(dragArr).on("drop", function(el) {
    var chosen_bin = document.getElementById("chosen_bin");
    chosen_bin.value = el.parentElement.id;
    console.log("Moved to " + el.parentElement.id);
})

var submit_trial_btn = document.getElementById("submit_trial");
submit_trial_btn.disabled = true;

function showFeedback() {
    var feedback_box = document.getElementById("feedback_text");
    var feedback_image = document.getElementById("feedback_image");
    var chosen_bin = document.getElementById("chosen_bin").value;
    var submit_choice_btn = document.getElementById("submit_choice_btn");
    var submit_trial_btn = document.getElementById("submit_trial");

    if (chosen_bin == "staging" || chosen_bin == "") {
        feedback_box.innerHTML = "Please choose a bin for the card!";
        feedback_image.innerHTML = "image";
    } else {
        feedback_box.innerHTML = $("bin_feedback" + chosen_bin[3]).innerHTML + " Go to the next trial.";
        feedback_image.src = $("bin_image" + chosen_bin[3]).innerHTML;
        submit_choice_btn.disabled = true;
        submit_trial_btn.disabled = false;
        drake.destroy();
    }
}