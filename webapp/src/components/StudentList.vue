<template>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Link Dostępowy</th>
          <th scope="col">Akcja</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(student, idx) in students"
            :key="student.id"
        >
          <th scope="row">{{idx + 1}}</th>
          <td>{{student.display_name}}</td>
          <td>{{student.access_url}}</td>
          <button type="button" class="btn btn-primary"
                    @click="$event => resetAccessLink($event, student)"
            >Resetuj Dostęp</button>
        </tr>
      </tbody>
    </table>
</template>

<script>
    import {Students} from "../api";

    export default {
        name: "StudentList",
        props: {
          students:  {
            type: Array
          },
        },
        methods: {
          resetAccessLink($event, student) {
            $event.stopPropagation();
            const updatedStudent = Students.resetAccess(student);
            this.$emit('updatedStudent', updatedStudent);
          }
        }
    }
</script>

<style scoped>

</style>