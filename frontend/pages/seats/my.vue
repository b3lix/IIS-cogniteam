<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/seats/my" active>Zoznam rezervácií</b-nav-item>
    </b-nav>
    <hr>
    <b-alert variant="info" v-show="seats.length == 0" show>
      Nemáte žiadne rezervácie
    </b-alert>
    <div v-for="seat in seats" :key="seat.id">
      <b-alert variant="info" v-show="seat.route == null || seat.from_station == null || seat.to_station == null || seat.route?.vehicle == null" show>
        <font-awesome-icon icon="info"></font-awesome-icon>
        Z dôvodu zmeny niektorých údajov v systéme dopravcom môžu byť niektoré údaje v tejto rezervácii neplatné alebo nedostupné. Pomocou ID si môžete nárokovať reklamáciu (Pokiaľ už rezervácia bola uhradená).
      </b-alert>
      <div>ID Rezervácie: <strong>{{ seat.id}}</strong>, Vytvorená: <i>{{ seat.created_at }}</i></div>
      <div><i>Rezervácia na meno: {{ seat.name}} ({{ seat.email}})</i></div>
      <div><strong>Dopravca:</strong> {{ seat.route?.vehicle?.carrier }}</div>
      <div><font-awesome-icon icon="dot-circle"></font-awesome-icon> <strong>Aktuálna poloha</strong>: {{ seat.route?.vehicle?.location }}</div>
      <div><font-awesome-icon icon="bus"></font-awesome-icon> {{ seat.route?.vehicle?.name }}</div>
      <div><font-awesome-icon icon="clock"></font-awesome-icon> {{ seat.date }}</div>
      <div><font-awesome-icon icon="calendar"></font-awesome-icon> {{ seat.route?.time }}</div>
      <div><font-awesome-icon icon="sign-in-alt"></font-awesome-icon> {{ seat.from_station?.location }} - {{ seat.from_station?.name }}</div>
      <div><font-awesome-icon icon="sign-out-alt"></font-awesome-icon> {{ seat.to_station?.location }} - {{ seat.to_station?.name }}</div>
      <br>
      <div><strong>Cena</strong>: {{ seat.price }}€, <strong>Počet miest</strong>: {{ seat.amount }}</div>
      <div><strong>Stav</strong>: {{ seat.paid ? "Uhradená" : "Neuhradená" }}</div>
      <hr>
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
      seats: []
    }
  },
  async mounted() {
    this.fetchSeats();
  },
  methods: {
    async fetchSeats() {
      let response = await this.$axios.get("/browser/get_my_seats");
      this.seats = response.data.seats;
    },
    deleteSeat(id) {
      if(!confirm("Naozaj chcete vymazať túto rezerváciu?"))
        return;

      this.$axios.post(`/browser/delete_seat/${id}`).then(async () => {
        this.fetchSeats();
      });
    }
  }
}
</script>