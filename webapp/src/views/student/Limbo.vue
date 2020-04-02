<template>
    <div>
        <div class="row">
          <div class="col-md-12 my-3">
              <h2>Oczekiwanie na rozpoczęcie zajęć...</h2>
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
