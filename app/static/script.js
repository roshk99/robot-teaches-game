
function $(id) {
    return document.getElementById(id);
};

var bins = document.getElementsByClassName("bin");
dragArr = [$("staging")]
for (i=0; i < bins.length; i++) {
    dragArr[i+1] = $(bins[i].id);
}
var drake = dragula(dragArr).on("drop", function (el) {
    var chosen_bin = document.getElementById("chosen_bin");
    chosen_bin.value = el.parentElement.id;
    console.log("Moved to " + el.parentElement.id);
})
var submit_btn = document.getElementById("submit");
submit_btn.disabled = true;

function showFeedback() {
    var feedback_box = document.getElementById("feedback_text");
    var chosen_bin = document.getElementById("chosen_bin").value;
    var submit_choice_btn = document.getElementById("submit_choice_btn");
    var submit_btn = document.getElementById("submit");

    if (chosen_bin == "staging" || chosen_bin == "") {
        feedback_box.innerHTML = "Please choose a bin for the card!";
    }
    else {
        feedback_box.innerHTML = $("bin_feedback" + chosen_bin[3]).innerHTML + " Go to the next trial.";
        submit_choice_btn.disabled = true;
        submit_btn.disabled = false;
        drake.destroy();
    }
}