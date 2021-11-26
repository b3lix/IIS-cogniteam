<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/routes">Zoznam spojov</b-nav-item>
      <b-nav-item to="/routes/create" active>Pridať spoj</b-nav-item>
      <b-nav-item disabled>Úprava spoju</b-nav-item>
    </b-nav>
    <hr>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="create">
      <b-form-group>
        <label>Názov spoju:</label>
        <b-form-input v-model="name" type="text" placeholder="Názov spoju" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <label>Cena za zastávku:</label>
        <b-form-input v-model="price" type="number" step="0.01" placeholder="1.00€" required></b-form-input>
      </b-form-group>
      <b-form-group v-if="$store.state.user.info?.type == 3">
        <label>Dopravca prevádzkujúci spoj:</label>
        <b-select v-model="selected_carrier">
          <option :value="null" disabled>Zvoľte dopravcu</option>
          <option v-for="carrier in carriers" :key="carrier.id" :value="carrier.id">{{ carrier.name }}</option>
        </b-select>
      </b-form-group>
      <hr>
      <font-awesome-icon icon="clock"></font-awesome-icon> Nastavenie rozvrhu:
      <hr>
      <b-alert variant="info" show>
        Nastavenie príchodu a odchodu z jednotlivých staníc. Čas je relatívny a začína od minúty 0
      </b-alert>
      <hr>
      <b-form-group v-for="item in sortedStops" :key="item.id">
        <b-input-group>
          <select v-model="stops[item.id].station">
            <option v-for="station in stations" :key="station.id" :value="station.id">{{ station.location }} - {{ station.name }}</option>
          </select>
          <b-form-input v-model="stops[item.id].arrival" placeholder="Minúta príchodu" type="number"></b-form-input>
          <b-form-input v-model="stops[item.id].departure" placeholder="Minúta odchodu" type="number"></b-form-input>
          <b-button variant="primary" type="button" @click="$delete(stops, item.id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
        </b-input-group>
      </b-form-group>
      <hr>
      <b-input-group>
        <select v-model="stop.station">
          <option :value="null" selected disabled>Zvoľte stanicu</option>
          <option v-for="station in stations" :key="station.id" :value="station.id">{{ station.location }} - {{ station.name }}</option>
        </select>
        <b-form-input v-model="stop.arrival" placeholder="Minúta príchodu" type="number" required></b-form-input>
        <b-form-input v-model="stop.departure" placeholder="Minúta odchodu" type="number" required></b-form-input>
        <b-button variant="primary" type="button" @click="addStop()">Pridať zastávku</b-button>
      </b-input-group>
      <hr>
      <font-awesome-icon icon="calendar"></font-awesome-icon> Nastavenie  výskytu:
      <hr>
      <b-alert variant="info" show>
        Nastavenia opakovania spoju v danom čase s daným vozidlom
      </b-alert>
      <hr>
      <b-form-group v-for="(time, id) in times" :key="id">
        <b-input-group>
          <select v-model="times[id].vehicle">
            <option v-for="vehicle in vehicles.filter(x => selected_carrier != null && x.carrier.id == selected_carrier)" :key="vehicle.id" :value="vehicle.id">{{ vehicle.name }}</option>
          </select>
          <b-form-timepicker v-model="times[id].time" type="time" required class="mr-2"></b-form-timepicker>
          <b-form-checkbox v-model="times[id].repeat[0]" required class="mt-2">Pondelok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[1]" required class="mt-2">Utorok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[2]" required class="mt-2">Streda</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[3]" required class="mt-2">Štvrtok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[4]" required class="mt-2">Piatok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[5]" required class="mt-2">Sobota</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[6]" required class="mt-2">Nedeľa</b-form-checkbox>
          <b-button variant="primary" type="button" @click="$delete(times, id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
        </b-input-group>
      </b-form-group>
      <hr>
      <b-input-group>
        <select v-model="time.vehicle">
          <option :value="null" selected disabled>Zvoľte vozidlo</option>
          <option v-for="vehicle in vehicles.filter(x => selected_carrier != null && x.carrier.id == selected_carrier)" :key="vehicle.id" :value="vehicle.id">{{ vehicle.name }}</option>
        </select>
        <b-form-timepicker v-model="time.time" type="time" required class="mr-2"></b-form-timepicker>
        <b-form-checkbox v-model="time.repeat[0]" required class="mt-2">Pondelok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[1]" required class="mt-2">Utorok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[2]" required class="mt-2">Streda</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[3]" required class="mt-2">Štvrtok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[4]" required class="mt-2">Piatok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[5]" required class="mt-2">Sobota</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[6]" required class="mt-2">Nedeľa</b-form-checkbox>
        <b-button variant="primary" type="button" @click="addTime()">Pridať výskyt</b-button>
      </b-input-group>
      <hr>
      <b-form-group>
        <b-button variant="primary" type="submit">Vytvoriť spoj</b-button>
      </b-form-group>
    </b-form>
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
        stop: {
          station: null,
          arrival: null,
          departure: null,
          order: 0
        },

        time: {
          time: null,
          vehicle: null,
          repeat: [false, false, false, false, false, false, false]
        },

        price: null,
        name: null,
        selected_carrier: null,
        stops: {},
        times: {},

        error: null,
        vehicles: [],
        stations: [],
        carriers: []
    }
  },
  async beforeMount() {
    let response = await this.$axios.get("/vehicles/get");
    this.vehicles = response.data.vehicles;

    response = await this.$axios.get("/stations/get");
    this.stations = response.data.stations;

    if(this.$store.state.user.info?.type != 3)
      return;

    let result = await this.$axios.get("/users/get");
    this.carriers = result.data.users.filter(user => user.type == 2);
  },
  computed: {
    sortedStops() {
      var sortable = [];
      for (let id in this.stops)
          sortable.push({ id: id, stop: this.stops[id] });

      sortable.sort(function(a, b) {
          return a.stop.arrival - b.stop.departure;
      });

      for(let i = 0; i < sortable.length; i++)
        sortable[i].stop.order = i;
      
      return sortable;
    }
  },
  methods: {
    create() {
      let formData = {
        price: this.price,
        carrier: this.selected_carrier ?? 0,
        name: this.name,
        stops: [],
        times: []
      };
      this.sortedStops.forEach(item => {
        formData.stops.push({
          station: item.stop.station,
          arrival: parseInt(item.stop.arrival),
          departure: parseInt(item.stop.departure)
        });
      });

      Object.values(this.times).forEach(time => {
        formData.times.push(time);
      });

      this.$axios.post("/routes/create", formData).then(() => {
        this.$router.push("/routes");
      }).catch(e => {
        this.error = e.response.data?.message ?? "Nepodarilo sa pridať spoj";
      });
    },
    addStop() {
      if(this.stop.station == null)
        return;

      let id = Math.random().toString(36).substring(2, 15);
      this.$set(this.stops, id, {
        station: this.stop.station,
        arrival: this.stop.arrival,
        departure: this.stop.departure,
        order: 0
      });
    },
    addTime() {
      if(this.time.vehicle == null || this.time.time == null)
        return;

      let id = Math.random().toString(36).substring(2, 15);
      this.$set(this.times, id, {
        time: this.time.time,
        vehicle: this.time.vehicle,
        repeat: [...this.time.repeat]
      });
    }
  }
}
</script>