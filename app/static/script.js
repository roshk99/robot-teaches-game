
function $(id) {
    return document.getElementById(id);
};

var bins = document.getElementsByClassName('bin');
dragArr = [$('staging')]
for (i=0; i < bins.length; i++) {
    dragArr[i+1] = $(bins[i].id);
}
dragula(dragArr);


