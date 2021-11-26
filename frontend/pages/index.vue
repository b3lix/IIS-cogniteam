<template>
  <b-container>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="search">
      <b-form-group>
        <label>Zo zastávky:</label>
        <b-select v-model="formData.from_station">
          <option :value="null" disabled>Vyber zastávku</option>
          <option v-for="station in stations" :key="station.id" :value="station.id">{{ station.location }} - {{ station.name }}</option>
        </b-select>
      </b-form-group>
      <b-form-group>
        <label>Do zastávky:</label>
        <b-select v-model="formData.to_station">
          <option :value="null" disabled>Vyber zastávku</option>
          <option v-for="station in stations" :key="station.id" :value="station.id">{{ station.location }} - {{ station.name }}</option>
        </b-select>
      </b-form-group>
      <b-form-group>
        <label>Dátum odchodu:</label>
        <b-form-datepicker v-model="formData.date" type="date" required></b-form-datepicker>
      </b-form-group>
      <b-form-group>
        <label>Čas odchodu:</label>
        <b-form-timepicker v-model="formData.time" type="time" required></b-form-timepicker>
      </b-form-group>
      <b-alert show variant="info" class="mt-2">
        <font-awesome-icon icon="info"></font-awesome-icon>
        Vyhľadávanie vyhľadáva spoje až do hodiny po zvolenom čase odchodu
      </b-alert>
      <b-form-group>
        <b-button variant="primary" type="submit">Vyhľadať spoje</b-button>
      </b-form-group>
    </b-form>
    <div v-for="(route, index) in routes" :key="index">
      <strong>Dopravca:</strong> {{ route.carrier }}, <strong>Vozidlo:</strong> {{ route.vehicle.name }}
      <p>Z: {{ route.stops[0].station.name }} - {{ route.stops[0].departure }}</p>
      <p>Do: {{ route.stops.at(-1).station.name }} - {{ route.stops.at(-1).arrival }}</p>
      <b-button v-if="$store.state.user.info == null || [0, 3].includes($store.state.user.info?.type)" variant="primary" type="button" @click="
        seatFormData.route = route.id; 
        seatFormData.date = formData.date;
        seatFormData.from_stop = route.stops[0].id;
        seatFormData.to_stop = route.stops.at(-1).id;" :disabled="route.vehicle.capacity - route.vehicle.seats <= 0" v-b-modal.seatform>
        <strong>{{ route.price }}€ </strong>
        Rezervovať lístok ({{ route.vehicle.seats }}/{{ route.vehicle.capacity }})
      </b-button>
      <hr>
    </div>
    <b-modal v-on:ok="createSeat($event)" id="seatform" title="Vytvoriť rezerváciu">
      <b-alert variant="danger" v-show="seatError !== null" show>
        {{ seatError }}
      </b-alert>
      <b-form method="POST" @submit.prevent="create">
        <b-form-group>
          <b-form-input v-model="seatFormData.name" type="text" placeholder="Meno a Priezvisko" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-input v-model="seatFormData.email" type="email" placeholder="email" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-input v-model="seatFormData.amount" type="number" min="1" max="5" placeholder="Počet miest 1-5" required></b-form-input>
        </b-form-group>
      </b-form>
    </b-modal>
  </b-container>
</template>

<style lang="scss">
</style>

<script>
export default {
  layout: "default",
  data() {
    return {    
      error: null,

      stations: [],
      routes: [],

      formData: {
        from_station: null,
        to_station: null,
        date: null,
        time: null
      },

      seatError: null,
      seatFormData: {
        date: null,
        route: null,
        from_stop: null,
        to_stop: null,
        name: this.$store.state.user.info?.name,
        email: this.$store.state.user.info?.email,
        amount: 1
      }
    }
  },
  created() {
    let date = new Date();
    this.formData.time = new Date().toTimeString().split(" ")[0];
    this.formData.date = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
  },
  async beforeMount() {
    let response = await this.$axios.get("/stations/get");
    this.stations = response.data.stations;
  },
  methods: {
    search() {
      this.error = null;
      this.$axios.post("browser/get", this.formData).then(response => {
        this.routes = response.data.routes;
      }).catch(e => {
        this.error = e.response.data?.message ?? "Nepodarilo sa získať spoje";
      });
    },
    createSeat(e) {
      e.preventDefault();

      this.seatError = null;

      this.$axios.post("browser/create_seat", this.seatFormData).then(response => {
        this.$router.push("seats/my");
      }).catch(e => {
        this.seatError = e.response.data?.message ?? "Nepodarilo sa vytvoriť rezerváciu";
      });
    }
  }
}
</script>