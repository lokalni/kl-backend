<template>
    <div class="container">
        <Navbar/>
        <div class="row">
            <div class="col-md-12 my-3">
                <h2>Zarządzanie moderatorami</h2>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <AddModeratorForm @moderatorSubmitted="onModeratorSubmitted"/>
            </div>
            <div class="col-md-6">
                <input v-model="searchQuery" @input="onSearchQueryChange" class="form-control" type="text" placeholder="Szukaj...">
                <ModeratorList :moderators="moderators" @moderatorsUpdated="reload"/>
            </div>
        </div>
    </div>
</template>

<script>
import ModeratorList from '@/components/ModeratorList.vue';
import {Moderators} from '@/api';
import AddModeratorForm from "../../components/AddModeratorForm";
import Navbar from '@/components/Navbar.vue';
import {debounce} from "lodash";

export default {
    name: "ManageModerators",
    data() {
        return {
            searchQuery: '',
            moderators: [],
        }
    },
    async beforeMount() {
        await this.reload();
    },
    components: {
        AddModeratorForm,
        ModeratorList,
        Navbar,
    },
    methods: {
        async onModeratorSubmitted(moderator) {
            await Moderators.create(moderator);
            await this.reload();
        },
        async reload() {
            this.moderators = await Moderators.list({search: this.searchQuery});
        },
        onSearchQueryChange: debounce( async function() {
            if (this.searchQuery && this.searchQuery.length <= 3) {
                return;
            }
            await this.reload();
        }, 1000)
    }
}
</script>

<style scoped>

</style>