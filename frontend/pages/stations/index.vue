<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/stations" active>Zoznam staníc</b-nav-item>
      <b-nav-item to="/stations/create">Pridať stanicu</b-nav-item>
      <b-nav-item to="/stations/approve" v-if="$store.state.user.info?.type == 3">Žiadosti o zmenu</b-nav-item>
      <b-nav-item disabled>Úprava stanice</b-nav-item>
    </b-nav>
    <hr>
    <b-alert  variant="info" v-show="$store.state.user.info?.type == 2" show>
      Novo pridané stanice sa nezobrazia okamžite, najprv musia prejsť schválením administrátora
    </b-alert>
    <vue-good-table :columns="columns" :rows="stations" :search-options="{ enabled: true }" :pagination-options="{ enabled: true }">
      <template slot="table-row" slot-scope="props">
        <span v-if="props.column.field == 'tools'">
          <b-button class="tool" variant="success" :to="'/stations/update/'  + props.row.id"><font-awesome-icon icon="edit"></font-awesome-icon></b-button>
          <b-button class="tool" variant="danger" @click="deleteStation(props.row.id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
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
          width: "60px"
        },
        {
          label: "Názov stanice",
          field: "name",
          filterOptions: {
            enabled: true,
            placeholder: "Názov stanice",
          }
        },
        {
          label: "Oblasť/Mesto",
          field: "location",
          filterOptions: {
            enabled: true,
            placeholder: "Oblasť/Mesto",
          }
        },
        {
          label: "Nástroje",
          field: "tools",
          width: "100px",
          sortable: false
        }
      ],
      stations: []
    }
  },
  async mounted() {
    this.fetchStations();
  },
  methods: {
    async fetchStations() {
      let response = await this.$axios.get("/stations/get");
      this.stations = response.data.stations;
    },
    deleteStation(id) {
      if(!confirm("Naozaj chcete vymazať túto stanicu?"))
        return;

      this.$axios.post(`/stations/delete/${id}`).then(async () => {
        this.fetchStations();
      });
    }
  }
}
</script>