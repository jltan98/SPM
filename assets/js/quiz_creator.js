function sendToCreate(){
    quizName = document.getElementById("quizName").value
    questions = document.getElementById("questions").value
    course = document.getElementById("course").value
    section = document.getElementById("section").value

    sessionStorage.setItem("quizName",quizName)
    sessionStorage.setItem("questions",questions)
    sessionStorage.setItem("section",section)
    sessionStorage.setItem("course",course)
    window.location.href = "quiz_creation.html"
}
