<template>
  <b-container>
    Rezervácie: 
    <div v-for="seat in seats" :key="seat.id">
        {{ seat }}
        <a href="#" @click="deleteSeat(seat.id)">Odstrániť</a>
        <a v-if="!seat.paid" href="#" @click="setPaid(seat.id)">Zaplatené</a>
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
      let response = await this.$axios.get("/browser/get_seats");
      this.seats = response.data.seats;
    },
    deleteSeat(id) {
      if(!confirm("Naozaj chcete vymazať túto rezerváciu?"))
        return;

      this.$axios.post(`/browser/delete_seat/${id}`).then(async () => {
        this.fetchSeats();
      });
    },
    setPaid(id) {
      if(!confirm("Naozaj chcete potvrdiť platbu tejto rezervácie?"))
        return;

      this.$axios.post(`/browser/set_seat_paid/${id}`).then(async () => {
        this.fetchSeats();
      });
    }
  }
}
</script>