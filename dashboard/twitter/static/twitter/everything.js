function form(input) {
    var ip = document.getElementById('input-word');
    ip.value = input;
    document.getElementById('content').value = input;
}

function impDate(str) {
    var impDate = new Date(str);
    document.getElementById('date').value = impDate;
    document.theForm.submit();
}

function changeDate(date) {
    document.getElementById('date').value = date;
    document.theForm.submit();
}

function resetFeatures() {
    document.getElementById('reset').value = "true";
    document.theForm.submit();
}

function changeWord(){
    word = document.getElementById('input-word').value;
    document.getElementById('content').value = word;
    document.theForm.submit();
}

