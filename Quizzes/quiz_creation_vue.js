// Vue instance
const main = Vue.createApp({

// Data Properties
    data() {
        return {
            number: 0,
            quizName:null,
            questions:null,
            course:null,
            section:null
        }
    },
    mounted(){
        this.quizName = sessionStorage.getItem("quizName")
        this.questions = Number(sessionStorage.getItem("questions"))
        this.section = sessionStorage.getItem("section")
        this.course = sessionStorage.getItem("course")
        console.log(this.quizName)
    },

})

main.component("radios",{
    template:'#radios',

    props:['q_no','op_no'],
    data(){
        return{
            opp_no:this.op_no
        }
    },
    template:
        `
        <div class="form-check">
        <input type="radio" 
        class="form-check-input ml-1 mt-3" 
        :name='\"Q\"+q_no'
        :value=1
        :checked="op_no === value"
        @change="updateValue(op_no)"
        >

        <input class="ml-4 mb-2 border-0 w-50 border-bottom form-control" type="text" id="exampleInputEmail1" :placeholder='\"Option \"+op_no'>
         </div>
        </div>
        `,
    methods: {
        updateValue(value) {
            this.$emit("change", value);
        },
        },
    
})

main.component('q_component', {
    props:["q_no"],
    data(){
        return{
            q_type:"MCQ",
            option_no:1,
            options:1,
            answer:null,
           answers:[],
           question:null
           
        }
    },

    template:  `
    <div class="col-8">
        <label for="Q1" class="form-label">Question {{q_no}}</label>
        <input type="text" class="form-control" id="Q1" aria-describedby="emailHelp" v-model="answer">
    </div>

    <div class="col-4">
        <label for="question_type" class="form-label">Question Type</label>
        <select class="form-select" id="question_type" v-model="q_type">
            <option value="MCQ">Multiple Choice</option>
            <option value="TF">True or False</option>
        </select>
    </div>
    <div v-if='q_type === "MCQ"'>
        <radios v-for="i in options" :op_no=i v-model="answer" :value=i></radios>
    </div>
    <div v-if='q_type === "TF"'>
        <div class="form-check">
            <input type="radio" class="form-check-input ml-1" name="q1" id="q{{q_no}}T" :value="t">
            <label class="form-check-label ml-4"for="q{{q_no}}T">True</label>
        </div>
        <div class="form-check">
            <input type="radio" class="form-check-input ml-1" name="q1" id="q{{q_no}}F" value="f">
            <label class="form-check-label ml-4"for="q{{q_no}}F">False</label>
        </div>
    </div>
    <button class="btn btn-warning" v-if='q_type === "MCQ"' @click="addOptions">Add option</button>
   `,
   methods:{
       addOptions(){
           this.options++
       },
       editArr(){

       }
   },
   computed:{
        placeholder(){
            return "Option" + option_no
        } 
   }
})


  
  
// Link this Vue instance with <div id="main">
main.mount("#main")
  



