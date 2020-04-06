<template>
    <div class="container">
        <Navbar/>
        <div class="row">
            <div class="col-md-6">
                <AddModeratorForm @moderatorSubmitted="onModeratorSubmitted"/>
            </div>
            <div class="col-md-6">
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

export default {
    name: "ManageModerators",
    data() {
        return {
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
            Moderators.create(moderator);
            await this.reload();
        },
        async reload() {
            this.moderators = await Moderators.list();
        }
    }
}
</script>

<style scoped>

</style>