<template>
    <form @submit="groupSubmitted">
      <div class="form-row">
        <div class="col-4">
          <input v-model="name" type="text" class="form-control" placeholder="Nazwa grupy">
        </div>
        <div class="col-2">
           <select v-model="selectedRegion" class="form-control">
              <option value="">Wybierz region...</option>
              <option v-for="region in regionOptions" :key="region" :value="region">{{region}}</option>
           </select>
        </div>
        <div class="col-auto">
          <button type="submit" class="btn btn-primary mb-2"
                  :disabled="!formValid"
          >Dodaj</button>
        </div>
      </div>
    </form>
</template>

<script>

import {REGIONS} from "../../constants";

export default {
    name: "AddGroupForm",
    data() {
        return {
          name: '',
          selectedRegion: '',
        };
    },
    computed: {
      formValid() {
          window.console.log(this.name, this.selectedRegion);
          return this.name && this.regionOptions.includes(this.selectedRegion);
      },
      regionOptions() {
        return Object.values(REGIONS);
      }
    },
    methods: {
        groupSubmitted() {
            const group = {name: this.name, region: this.selectedRegion};
            this.$emit('submittedGroup', group);
            this.name = this.selectedRegion = '';
            console.log("Group Submitted", group);
        }
    }
}
</script>

<style scoped>

</style>