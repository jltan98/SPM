const app = Vue.createApp({
    data(){
        return{
            classes:[],
            selected:null,
            selected_sections:[],
            section:null,
            questions:null
            
        }
    },
    methods:{
        get_sections(){
            this.selected_sections = []
            for(sections of this.classes){
                if(sections["course"] == this.selected){
                this.selected_sections.push(sections["section"])
                }
            }
        }
    },
    mounted () {
        console.log("start")
        axios.get('http://ec2-44-196-228-15.compute-1.amazonaws.com:5003/classes/T001', {
    })
        .then(response => {
            console.log(response)
            data = response.data.data
            for(sections of data){
                section = sections.classID
                course = sections.courseID
                const obj = {course:course,section:section}
                this.classes.push(obj)
            }

            console.log(this.classes[0].course)

        })
        .catch(error => {
            console.log(error)
        });
      }

})

const vm = app.mount("#app");