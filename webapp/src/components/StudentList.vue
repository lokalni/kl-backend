<template>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Link</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(student, idx) in students"
            :key="student.id"
        >
          <th scope="row">{{idx + 1}}</th>
          <td>{{student.display_name}}</td>
          <td>{{student.access_url}}</td>
        </tr>
      </tbody>
    </table>
</template>

<script>
    export default {
        name: "StudentList",
        props: {
          students:  {
            type: Array
          },
        },
    }
</script>

<style scoped>

</style>