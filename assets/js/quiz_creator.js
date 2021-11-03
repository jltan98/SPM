function get_classes(){
    axios.get('http://localhost:5002/classes/T001', {
    })
        .then(response => {
            console.log(response)
        })
        .catch(error => {
            console.log(error)
        });
}

window.onload = get_classes()
