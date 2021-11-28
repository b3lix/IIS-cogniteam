<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/vehicles/station" active>Aktuálna poloha</b-nav-item>
    </b-nav>
    <hr>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form-group>
      <label>Vyber spoj:</label>
      <b-select v-model="selected_route" @change="routeChanged()">
          <option :value="null" disabled>Zvoľ spoj</option>
          <option v-for="route in routes" :key="route.id" :value="route.id">{{ route.name }}</option>
      </b-select>
    </b-form-group>
    <b-form-group>
      <label>Vyber spoj:</label>
      <b-select v-model="selected_time" @change="timeChanged()" :disabled="selected_route_info == null">
          <option :value="null" disabled>Vyber čas</option>
          <option v-for="time in selected_route_info?.times ?? []" :key="time.id" :value="time.id">{{ time.time }}</option>
      </b-select>
    </b-form-group>
    <hr>
    <div v-if="selected_time != null">
      <font-awesome-icon icon="bus"></font-awesome-icon> {{ selected_time_vehicle_info?.name }} <br>
      <strong>Aktuálna stanica</strong>: {{ stations.find(x => x.id == selected_time_vehicle_info?.station)?.name ?? "Žiadna" }}
      <hr>
      <div v-for="stop in selected_route_info.stops" :key="stop.id">
        <b-button variant="primary" v-if="stop.station != selected_time_vehicle_info?.station" @click="update(stop.station)">
          <font-awesome-icon icon="arrow-right"></font-awesome-icon>
        </b-button>
        <template v-else>
          <font-awesome-icon icon="dot-circle"></font-awesome-icon>
        </template>
        {{ stationName(stop.station) }}
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
      if(this.selected_route == null)
        return;

      this.selected_time = null;
      this.$axios.get(`/routes/get/${this.selected_route}`).then(response => {
        this.selected_route_info = response.data;
      });
    },
    timeChanged() {
      if(this.selected_time == null)
        return;

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
        this.error = e.response?.data?.message ?? "Nepodarila sa aktualizovať poloha";
      });
    },
    stationName(id) {
      let station = this.stations.find(x => x.id == id);
      return `${station?.location} - ${station?.name}`;
    }
  }
}
</script>