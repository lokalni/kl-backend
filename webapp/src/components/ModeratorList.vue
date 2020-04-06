<template>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nazwa</th>
          <th scope="col">Email</th>
          <th scope="col">Link dostępowy</th>
          <th scope="col">Akcja</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(moderator, idx) in moderators"
            :key="moderator.id"
        >
          <th scope="row">{{idx + 1}}</th>
          <td>{{moderator.display_name}}</td>
          <td>{{moderator.email}}</td>
          <td>{{moderator.access_url}}</td>
            <button type="button" class="btn btn-primary m-2"
                      @click="$event => actionAccessLink($event, moderator)"
              >Resetuj Dostęp</button>
            <button type="button" class="btn btn-danger m-2"
                      @click="$event => actionRemoveModerator($event, moderator)"
              >Usuń</button>
        </tr>
      </tbody>
    </table>
</template>

<script>
import {Moderators} from "@/api";

export default {
    name: "ModeratorList",
    props: {
      moderators:  {
        type: Array
      },
    },
    methods: {
      async actionAccessLink($event, moderator) {
        $event.stopPropagation();
        await Moderators.resetAccess(moderator);
        this.$emit('moderatorsUpdated', moderator);
      },
      async actionRemoveModerator($event, moderator) {
        $event.stopPropagation();
        await Moderators.delete(moderator.id);
        this.$emit('moderatorsUpdated', moderator);
      }
    }
}
</script>

<style scoped>

</style>
