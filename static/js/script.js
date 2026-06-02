document.addEventListener("DOMContentLoaded", function(){

if(typeof chartLabels !== "undefined"){

const ctx = document.getElementById("stressChart");

new Chart(ctx,{

type:"line",

data:{
labels:chartLabels,
datasets:[{
label:"Stress Level Trend",
data:chartValues,
borderColor:"yellow",
backgroundColor:"rgba(255,255,0,0.2)",
tension:0.3
}]
}

});

}

});