<template>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Link dostępowy</th>
          <th scope="col">Ostatnie użycie</th>
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
          <td>{{fmtLastAccessed(student.last_accessed)}}</td>
            <button type="button" class="btn btn-primary m-2"
                      @click="$event => actionAccessLink($event, student)"
              >Resetuj Dostęp</button>
            <button type="button" class="btn btn-danger m-2"
                      @click="$event => actionRemoveStudent($event, student)"
              >Usuń</button>
        </tr>
      </tbody>
    </table>
</template>

<script>
    import {Students} from "../api";
    import {fmtTimestamp} from "../utils";

    export default {
        name: "StudentList",
        props: {
          students:  {
            type: Array
          },
        },
        methods: {
          async actionAccessLink($event, student) {
            $event.stopPropagation();
            const updatedStudent = await Students.resetAccess(student);
            this.$emit('updatedStudent', updatedStudent);
          },
          async actionRemoveStudent($event, student) {
            $event.stopPropagation();
            await Students.delete(student.id);
            this.$emit('updatedStudent', student);
          },
          fmtLastAccessed(timestamp) {
            return fmtTimestamp(timestamp) || 'Nigdy';
          }
        }
    }
</script>

<style scoped>

</style>
