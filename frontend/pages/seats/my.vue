<template>
  <b-container>
    Moje rezervácie: 
    <div v-for="seat in seats" :key="seat.id">
        {{ seat }}
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