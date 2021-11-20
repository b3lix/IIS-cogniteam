<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/routes">Zoznam spojov</NuxtLink></li>
      <li><NuxtLink to="/routes/create">Pridať spoj</NuxtLink></li>
    </ul>
    Upraviť spoj:
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="update">
      <b-form-group>
        <b-form-input v-model="name" type="text" placeholder="Názov spoju" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="price" type="number" step="0.01" placeholder="1.00€" required></b-form-input>
      </b-form-group>
      <b-form-group v-if="$store.state.user.info?.type == 3">
        <select v-model="selected_carrier">
          <option :value="0" disabled>Zvoľte dopravcu</option>
          <option v-for="carrier in carriers" :key="carrier.id" :value="carrier.id">{{ carrier.username }}</option>
        </select>
      </b-form-group>
      <hr>
      Nastavenie rozvrhu:
      <hr>
      <b-form-group v-for="item in sortedStops" :key="item.id">
        <b-input-group>
          <select v-model="stops[item.id].station">
            <option v-for="station in stations" :key="station.id" :value="station.id">{{ station.name }}</option>
          </select>
          <b-form-input v-model="stops[item.id].arrival" type="number" required></b-form-input>
          <b-form-input v-model="stops[item.id].departure" type="number" required></b-form-input>
          <b-button variant="primary" type="button" @click="$delete(stops, item.id)">x</b-button>
        </b-input-group>
      </b-form-group>
      <b-input-group>
        <select v-model="stop.station">
          <option :value="null" selected disabled>Zvoľte stanicu</option>
          <option v-for="station in stations" :key="station.id" :value="station.id">{{ station.name }}</option>
        </select>
        <b-form-input v-model="stop.arrival" type="number"></b-form-input>
        <b-form-input v-model="stop.departure" type="number"></b-form-input>
        <b-button variant="primary" type="button" @click="addStop()">Pridať zastávku</b-button>
      </b-input-group>
      <hr>
      Nastavenie  výskytu:
      <hr>
      <b-form-group v-for="(time, id) in times" :key="id">
        <b-input-group>
          <select v-model="times[id].vehicle">
            <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">{{ vehicle.name }}</option>
          </select>
          <b-form-timepicker v-model="times[id].time" type="time" required></b-form-timepicker>
          <b-form-checkbox v-model="times[id].repeat[0]" required>Pondelok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[1]" required>Utorok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[2]" required>Streda</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[3]" required>Štvrtok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[4]" required>Piatok</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[5]" required>Sobota</b-form-checkbox>
          <b-form-checkbox v-model="times[id].repeat[6]" required>Nedeľa</b-form-checkbox>
          <b-button variant="primary" type="button" @click="$delete(times, id)">x</b-button>
        </b-input-group>
      </b-form-group>
      <b-input-group>
        <select v-model="time.vehicle">
          <option :value="null" selected disabled>Zvoľte vozidlo</option>
          <option v-for="vehicle in vehicles" :key="vehicle.id" :value="vehicle.id">{{ vehicle.name }}</option>
        </select>
        <b-form-timepicker v-model="time.time" type="time" required></b-form-timepicker>
        <b-form-checkbox v-model="time.repeat[0]" required>Pondelok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[1]" required>Utorok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[2]" required>Streda</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[3]" required>Štvrtok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[4]" required>Piatok</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[5]" required>Sobota</b-form-checkbox>
        <b-form-checkbox v-model="time.repeat[6]" required>Nedeľa</b-form-checkbox>
        <b-button variant="primary" type="button" @click="addTime()">Pridať výskyt</b-button>
      </b-input-group>
      <b-form-group>
        <b-button variant="primary" type="submit">Upraviť spoj</b-button>
        <b-button variant="primary" type="button" @click="deleteRoute(id)">Zmazať spoj</b-button>
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
        id: this.$route.params.id,

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
    this.$axios.get(`/routes/get/${this.id}`).then(response => {
      this.price = response.data.price;
      this.selected_carrier = response.data.carrier;
      this.name = response.data.name;

      response.data.stops.forEach(stop => {
        let id = Math.random().toString(36).substring(2, 15);
        this.$set(this.stops, id, {
          station: stop.station,
          arrival: stop.arrival,
          departure: stop.departure,
          order: 0
        });
      });

      response.data.times.forEach(time => {
        let id = Math.random().toString(36).substring(2, 15);
        this.$set(this.times, id, {
          time: time.time,
          vehicle: time.vehicle,
          repeat: time.repeat
        })
      });
    });

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
    update() {
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

      this.$axios.post(`/routes/update/${this.id}`, formData).then(() => {
        this.$router.push("/routes");
      }).catch(e => {
        this.error = "Nepodarilo sa upraviť spoj";
      });
    },
    addStop() {
      let id = Math.random().toString(36).substring(2, 15);
      this.$set(this.stops, id, {
        station: this.stop.station,
        arrival: this.stop.arrival,
        departure: this.stop.departure,
        order: 0
      });
    },
    addTime() {
      let id = Math.random().toString(36).substring(2, 15);
      this.$set(this.times, id, {
        time: this.time.time,
        vehicle: this.time.vehicle,
        repeat: [...this.time.repeat]
      });
    },
    deleteRoute(id) {
      if(!confirm("Naozaj chcete vymazať tento spoj?"))
        return;

      this.$axios.post(`/routes/delete/${id}`).then(async () => {
        this.$router.push("/routes");
      });
    }
  }
}
</script>