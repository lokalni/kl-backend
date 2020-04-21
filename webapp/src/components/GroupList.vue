<template>
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa klasy</th>
          <th scope="col">Liczba uczniów</th>
          <th scope="col">Szybki dostęp</th>
          <th scope="col">Akcje</th>
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
          <td class="text-left" @click="onQuickAccessUrlClicked">
            {{ group.quick_access_url }}
          </td>
          <td>
            <button type="button" class="btn btn-light ml-1"
            >Edytuj</button>
            <button type="button" class="btn btn-primary ml-1"
                    @click="$event => startAndJoin($event, group)"
            >Rozpocznij lekcję</button>
            <button type="button" class="btn btn-danger ml-1"
                      @click="$event => onDeleteClicked($event, group)"
              >Usuń</button>
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
      async startAndJoin($event, group) {
        $event.stopPropagation();
        const {redirect} = await Groups.startLesson(group);
        window.console.log("Received redirect url CHECK_DEPLOYMENT_CACHE", redirect);
        window.location = redirect;
      },
      onDeleteClicked($event, group) {
        $event.stopPropagation();
        this.$emit('deleteGroup', group);
      },
      onQuickAccessUrlClicked($event) {
        $event.stopPropagation();
        // TODO - add copying to clipboard, consider uniform component for links
      }
    }
}
</script>

<style scoped>

</style>
