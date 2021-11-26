<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/seats" active>Zoznam rezervácií</b-nav-item>
    </b-nav>
    <hr>
    <vue-good-table :columns="columns" :rows="seats" :search-options="{ enabled: true }" :pagination-options="{ enabled: true }">
      <template slot="table-row" slot-scope="props">
        <span v-if="props.column.field == 'tools'">
          <b-button class="tool" variant="danger" @click="deleteSeat(props.row.id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
          <b-button class="tool" variant="primary" @click="printSeat(props.row.id)"><font-awesome-icon icon="print"></font-awesome-icon></b-button>
          <b-button class="tool" variant="success" @click="setPaid(props.row.id)" v-if="!props.row.paid"><font-awesome-icon icon="euro-sign"></font-awesome-icon></b-button>
        </span>
        <span v-else>
          {{props.formattedRow[props.column.field]}}
        </span>
      </template>
    </vue-good-table>
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
      columns: [
        {
          label: "ID",
          field: "id",
          type: "number",
          width: "70px",
          filterOptions: {
            enabled: true,
            placeholder: "ID",
          }
        },
        {
          label: "Meno",
          field: "name",
          filterOptions: {
            enabled: true,
            placeholder: "Meno pasažiera",
          }
        },
        {
          label: "Dátum",
          field: "date",
          width: "110px",
          filterOptions: {
            enabled: true,
            placeholder: "Dátum",
          }
        },
        {
          label: "Čas",
          field: "route.time",
          width: "90px",
          filterOptions: {
            enabled: true,
            placeholder: "Dátum",
          }
        },
        {
          label: "Z",
          field: "from_station.name",
          width: "90px",
          filterOptions: {
            enabled: true,
            placeholder: "Zo stanice",
          }
        },
        {
          label: "Do",
          field: "to_station.name",
          width: "90px",
          filterOptions: {
            enabled: true,
            placeholder: "Do stanice",
          }
        },
        {
          label: "Spoj",
          field: "route.info.name",
          filterOptions: {
            enabled: true,
            placeholder: "Spoj",
          }
        },
        {
          label: "Počet",
          field: "amount",
          type: "number",
          width: "80px",
          filterOptions: {
            enabled: true,
            placeholder: "Počet",
          }
        },
        {
          label: "Cena",
          field: "price",
          type: "decimal",
          formatFn: this.formatPrice
        },
        {
          label: "Nástroje",
          field: "tools",
          width: "120px",
          sortable: false
        }
      ],
      seats: []
    }
  },
  async mounted() {
    this.fetchSeats();
  },
  methods: {
    formatPrice: function(value) {
      return value + "€";
    },
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
    },
    printSeat(id) {
      alert("Potvrdenka vytlačená");
    }
  }
}
</script>