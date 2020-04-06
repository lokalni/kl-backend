<template>
    <div>
        <div class="row">
          <div class="col-md-12 my-3">
              <h2>Twoje lekcje rozpoczną się wkrótce</h2>
              <h4>Pozostaw tą stronę otwartą i poczekaj na nauczyciela</h4>
          </div>
        </div>
    </div>
</template>

<script>
import {Students} from "@/api";

export default {
    name: 'app',
    async mounted() {
        setTimeout(this.attemptJoin, 10000);
    },
    methods: {
      attemptJoin() {
          window.location = Students.buildJoinUrl(this.$route.query.token);
      }
    }
};
</script>
