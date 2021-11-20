<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/stations">Zoznam staníc</NuxtLink></li>
      <li><NuxtLink to="/stations/create">Pridať stanicu</NuxtLink></li>
      <li v-if="$store.state.user.info?.type == 3"><NuxtLink to="/stations/approve">Žiadosti o zmenu</NuxtLink></li>
    </ul>
    Zoznam staníc: 
    <div v-for="station in stations" :key="station.id">
      Názov: {{ station.name }}, Lokácia: {{ station.location }} 
      <NuxtLink :to="'/stations/update/' + station.id">Upraviť</NuxtLink>
      <a href="#" @click="deleteStation(station.id)">Odstrániť</a>
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
      stations: []
    }
  },
  async mounted() {
    this.fetchStations();
  },
  methods: {
    async fetchStations() {
      let response = await this.$axios.get("/stations/get");
      this.stations = response.data.stations;
    },
    deleteStation(id) {
      if(!confirm("Naozaj chcete vymazať túto stanicu?"))
        return;

      this.$axios.post(`/stations/delete/${id}`).then(async () => {
        this.fetchStations();
      });
    }
  }
}
</script>