<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/stations">Zoznam staníc</NuxtLink></li>
      <li><NuxtLink to="/stations/create">Pridať stanicu</NuxtLink></li>
      <li v-if="$store.state.user.info?.type == 3"><NuxtLink to="/stations/approve">Žiadosti o zmenu</NuxtLink></li>
    </ul>
    Zoznam žiadostí o zmenu:
    <div v-for="update in updates" :key="update.id">
      [ {{ update.type }} ] Názov: {{ update.name }}, Lokácia: {{ update.location }}
      <a href="#" @click="approveUpdate(update.id)">Schváliť</a>
      <a href="#" @click="deleteUpdate(update.id)">Odstrániť</a>
    </div>
  </b-container>
</template>

<style lang="scss">
</style>

<script>
export default {
  layout: "default",
  middleware: "authenticated",
  data() {
    return {
      updates: []
    }
  },
  async mounted() {
    this.fetchUpdates();
  },
  methods: {
    async fetchUpdates() {
      let response = await this.$axios.get("/stations/get_updates");
      this.updates = response.data.updates;
    },
    deleteUpdate(id) {
      if(!confirm("Naozaj chcete vymazať túto žiadosť?"))
        return;

      this.$axios.post(`/stations/delete_update/${id}`).then(async () => {
        this.fetchUpdates();
      });
    },
    approveUpdate(id) {
      if(!confirm("Naozaj chcete schváliť túto žiadosť?"))
        return;

      this.$axios.post(`/stations/approve_update/${id}`).then(async () => {
        this.fetchUpdates();
      });
    }
  }
}
</script>