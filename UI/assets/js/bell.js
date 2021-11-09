/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function dropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
function remove_taken(courses){
    not_taken = []
    for(course in courses){
        curr = courses[course]
        if(!taken.includes(curr["CourseID"])){
            not_taken.push(curr)
        }
    }

    return not_taken
}

  function get_user(name) {

    axios.get('http://localhost:5002/learner/'+name, {
    })
        .then(response => {
            check_enrol(response.data.data)
        })
        .catch(error => {
            this.error = error.response.data.message
        });
}

function check_enrol(user_data){
    var monthArr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
    var currentdate = new Date(); 
    curr_time = currentdate.getHours()+":"+currentdate.getMinutes()+":"+currentdate.getSeconds()
    month = monthArr[currentdate.getMonth()]
    date = currentdate.getDate() + " " + month + " " + currentdate.getFullYear() + " " + curr_time


    axios.get('http://localhost:5002/enrolDates', {
    })
        .then(response => {
            res = response.data.data
            curr_time = new Date().getTime()
            for(items in res){
                //Get time since epoch for both start and end date
                startDate = new Date(res[items]["enrolmentStartDate"]).getTime()
                endDate = new Date(res[items]["enrolmentEndDate"]).getTime()
                
                if(curr_time > startDate & curr_time < endDate){
                    get_courses(user_data)
                }
            }
        })
        .catch(error => {
            this.error = error.response.data.message
        });
}

function get_courses(user_data){

    axios.get('http://localhost:5002/courses', {
    })
        .then(response => {
            taken = user_data["coursesTaken"].split(", ")
            courses = response.data.data
            courses = remove_taken(courses)
            to_desplay = get_eligible(courses,taken,user_data)
            
        })
        .catch(error => {
            console.log(error)
        });
}




function get_eligible(courses,taken,user_data){
    eligible = []

    for(course in courses){
        curr = courses[course]
        prereq = curr["prerequisite"].split(", ")
        satisfied = 0
        for(let i=0; i<prereq.length; i++){
            if(taken.includes(prereq[i])){
                satisfied++
            }
        }
        if(satisfied == prereq.length){
            eligible.push(curr)
        }
    }


    for(course in eligible){
        document.getElementById("dropdown-contents").innerHTML+=`
        <a href="">${eligible[course]["CourseID"]} is available for enrolment</a>
        `
    }

    check_application(eligible.length,user_data)
}

function check_application(eligible_length, user_data){
    user_id = user_data.learnerID
    notif = 0
    axios.get('http://localhost:5002/applications/'+user_id, {
    })
        .then(response => {
            applications = response.data.data
            for(application of applications){
                if(application.applicationStatus == "Successful" || application.applicationStatus == "Unsuccessful"){
                    document.getElementById("dropdown-contents").innerHTML+=`
                        <a href="">Your application for ${application.applicationCourseID} is ${application.applicationStatus}</a>
                    `
                    notif++
                }
            }
    
    document.getElementById("bell").innerHTML = `<i class='dropbtn far fa-bell'></i> ${eligible_length + notif}`

        })
        .catch(error => {
            console.log(error)
        });
}




window.onload = get_user("Alivia")