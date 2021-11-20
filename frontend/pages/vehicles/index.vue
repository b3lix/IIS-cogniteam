<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/vehicles">Zoznam vozidel</NuxtLink></li>
      <li><NuxtLink to="/vehicles/create">Pridať vozidlo</NuxtLink></li>
    </ul>
    Zoznam vozidiel: 
    <div v-for="vehicle in vehicles" :key="vehicle.id">
      Názov: {{ vehicle.name }}, Kapacita: {{ vehicle.capacity }}
      <NuxtLink :to="'/vehicles/update/' + vehicle.id">Upraviť</NuxtLink>
      <a href="#" @click="deleteVehicle(vehicle.id)">Odstrániť</a>
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
      vehicles: []
    }
  },
  async mounted() {
    this.fetchVehicles();
  },
  methods: {
    async fetchVehicles() {
      let response = await this.$axios.get("/vehicles/get");
      this.vehicles = response.data.vehicles;
    },
    deleteVehicle(id) {
      if(!confirm("Naozaj chcete vymazať toto vozidlo?"))
        return;

      this.$axios.post(`/vehicles/delete/${id}`).then(async () => {
        this.fetchVehicles();
      });
    }
  }
}
</script>