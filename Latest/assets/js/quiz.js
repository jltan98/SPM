function get_quiz(){
    console.log("start")
    axios.get('http://ec2-44-196-228-15.compute-1.amazonaws.com:5003/quiz', {
    })
        .then(response => {
            console.log(response)
        })
        .catch(error => {
            console.log(error)
        });

}

window.onload = get_quiz()

//retrieve sessionStorage
var name = sessionStorage.getItem("name");
 document.getElementById("name").innerHTML = name
