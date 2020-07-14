function form(input) {
    var ip = document.getElementById('input-word');
    ip.value = input;
    document.getElementById('variable').value = 'content';
    document.getElementById('value').value = input;
}

function impDate(str) {
    var impDate = new Date(str);
    document.getElementById('variable').value = 'date';
    document.getElementById('value').value = impDate;
    document.theForm.submit();
}

function changeDate(date) {
    document.getElementById('variable').value = 'date';
    document.getElementById('value').value = date;
    document.theForm.submit();
}

function changeLoc(word){
    $.ajax({
        url: '/ajax/',
        data: {
          'loc': word
        },
        dataType: 'json',
        error: function (request, error) {
        console.log(" Can't do because: " + error);
         },
        success: function (data) {
          }
        
    });      
}

function resetFeatures() {
    document.getElementById('variable').value = 'reset';
    document.theForm.submit();
}

function changeWord(){
    word = document.getElementById('input-word').value;
    document.getElementById('variable').value = 'content';
    document.getElementById('value').value = word;
    document.theForm.submit();
}

// var y = document.getElementsByTagName('path');
//     for(var i = 0 ; i< y.length ; i++) 
//     {
        
//         const currentDom1 = y[i];
//         if (currentDom1.className.baseVal!="active")
//         currentDom1.className.baseVal="";
//         console.log("currentDOM!");
//         parent.document.theForm.submit();
//     }
//     currentDom.className.baseVal="selected";
//     changeLoc(id);
