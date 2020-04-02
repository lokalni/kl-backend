<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12 my-3">
        <h2>Studenci grupa</h2>
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

  export default {
    name: 'app',
    components: {
      StudentList,
    },
    data() {
      // TODO - move to vuex, maybe at API call level
      return {
        students: [],
      };
    },
    computed: {
    },
    async mounted() {
      await this.loadStudents();
    },
    methods: {
      async loadStudents() {
        this.students = await Students.list({group: this.$route.params.id});
        window.console.log("Students Fetched", this.groups);
      },

      async onUpdatedStudent() {
        await this.loadStudents();
        this.$toasted.show('Suckes!', {
          duration: 3000,
          type: 'success',
        });
      }
    }
  };
</script>
