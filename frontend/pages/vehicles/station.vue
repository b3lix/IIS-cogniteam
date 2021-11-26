<template>
  <b-container>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <select v-model="selected_route" @change="routeChanged()">
        <option v-for="route in routes" :key="route.id" :value="route.id">{{ route.name }}</option>
    </select>

    <div v-if="selected_route_info != null">
      <select v-model="selected_time" @change="timeChanged()">
          <option v-for="time in selected_route_info.times" :key="time.id" :value="time.id">{{ time.time }}</option>
      </select>

      <div v-if="selected_time != null">
        Vozidlo: {{ selected_time_vehicle_info?.name }} <br>
        Aktuálna stanica: {{ stations.find(x => x.id == selected_time_vehicle_info?.station)?.name ?? "Žiadna" }}
        <div v-for="stop in selected_route_info.stops" :key="stop.id">
          Stanica: {{ stations.find(x => x.id == stop.station)?.name }}
          <button @click="update(stop.station)">Nastaviť ako aktuálnu</button>
        </div>
      </div>
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
      error: null,

      routes: [],
      stations: [],

      selected_route: null,
      selected_time: null,

      selected_route_info: null,
      selected_time_vehicle_info: null
    }
  },
  async beforeMount() {
    let response = await this.$axios.get("/routes/get");
    this.routes = response.data.routes;

    response = await this.$axios.get("/stations/get");
    this.stations = response.data.stations;
  },
  methods: {
    routeChanged() {
      this.$axios.get(`/routes/get/${this.selected_route}`).then(response => {
        this.selected_route_info = response.data;
      });
    },
    timeChanged() {
      this.$axios.get(`/vehicles/get/${this.selected_route_info.times.find(x => x.id == this.selected_time).vehicle}`).then(response => {
        this.selected_time_vehicle_info = response.data;
      });
    },
    update(station) {
      let vehicle = this.selected_route_info.times.find(x => x.id == this.selected_time).vehicle;

      this.error = null;

      this.$axios.post(`vehicles/update_station/${vehicle}/${station}`).then(() => {
        this.timeChanged();
      }).catch(e => {
        this.error = e.response.data?.message ?? "Nepodarila sa aktualizovať poloha";
      });
    }
  }
}
</script>