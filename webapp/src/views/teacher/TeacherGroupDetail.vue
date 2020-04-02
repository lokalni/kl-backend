<template>
  <div class="container">
    <TeacherNavbar/>
    <div class="row">
      <div class="col-md-12 my-3">
        <h2>Studenci grupa</h2>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <AddStudentForm @submittedStudent="onSubmittedStudent"/>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <StudentList
            :students="students"
            @updatedStudent="onUpdatedStudent"
        />
      </div>
    </div>
  </div>
</template>

<script>
  import {Students} from '@/api';
  import StudentList from '@/components/StudentList.vue';
  import TeacherNavbar from '@/components/TeacherNavbar.vue';
  import AddStudentForm from "../../components/AddStudentForm";

  export default {
    name: 'app',
    components: {
      AddStudentForm,
      TeacherNavbar,
      StudentList,
    },
    data() {
      // TODO - move to vuex, maybe at API call level
      return {
        students: [],
      };
    },
    computed: {
      groupId() {
        return this.$route.params.id;
      }
    },
    async mounted() {
      await this.loadStudents();
    },
    methods: {
      async loadStudents() {
        this.students = await Students.list({group: this.groupId});
        window.console.log("Students Fetched", this.groups);
      },

      async onUpdatedStudent() {
        await this.loadStudents();
        this.$toasted.show('Sukces!', {duration: 3000, type: 'success'});

      },

      async onSubmittedStudent(student) {
        await Students.create({
          display_name: student.name,
          group: this.groupId
        });
        await this.loadStudents();
        this.$toasted.show('Dodano!', {duration: 3000, type: 'success'});
      },
    }
  };
</script>
