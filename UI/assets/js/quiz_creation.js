function get_info(){
    quizName = sessionStorage.getItem("quizName")
    questions = sessionStorage.getItem("questions")
    section = sessionStorage.getItem("section")
    course = sessionStorage.getItem("course")
    console.log(quizName)
    // document.getElementById("session").innerHTML = info
}

window.onload = get_info()