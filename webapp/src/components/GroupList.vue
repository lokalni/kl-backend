<template>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Liczba uczniow</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(group, idx) in groups"
            :key="group.id"
            @click="$emit('groupClicked', group)"
        >
          <th scope="row">{{idx + 1}}</th>
          <td>{{group.display_name}}</td>
          <td>{{group.students_count}}</td>
        </tr>
      </tbody>
    </table>
</template>

<script>
    export default {
        name: "GroupList",
        props: {
          groups:  {
            type: Array
          },
        },
    }
</script>

<style scoped>

</style>