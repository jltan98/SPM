function get_quiz(){
    console.log("start")
    axios.get('http://localhost:5002/quiz', {
    })
        .then(response => {
            console.log(response)
        })
        .catch(error => {
            console.log(error)
        });

}

window.onload = get_quiz()