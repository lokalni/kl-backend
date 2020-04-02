<template>
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Liczba uczniow</th>
          <th scope="col">Akcja</th>
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
          <td>
            <button type="button" class="btn btn-primary"
                    @click="$event => startAndJoin($event, group)"
            >Lekcja</button>
          </td>
        </tr>
      </tbody>
    </table>
</template>

<script>
import {Groups} from "../api";

export default {
    name: "GroupList",
    props: {
      groups:  {
        type: Array
      },
    },
    methods: {
      startAndJoin($event, group) {
        $event.stopPropagation();
        Groups.startLesson(group);
      }
    }
}
</script>

<style scoped>

</style>