<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/vehicles" active>Zoznam vozidel</b-nav-item>
      <b-nav-item to="/vehicles/create">Pridať vozidlo</b-nav-item>
      <b-nav-item disabled>Úprava vozidla</b-nav-item>
    </b-nav>
    <hr>
    <vue-good-table :columns="columns" :rows="vehicles" :search-options="{ enabled: true }" :pagination-options="{ enabled: true }">
      <template slot="table-row" slot-scope="props">
        <span v-if="props.column.field == 'tools'">
          <b-button class="tool" variant="success" :to="'/vehicles/update/'  + props.row.id"><font-awesome-icon icon="edit"></font-awesome-icon></b-button>
          <b-button class="tool" variant="danger" @click="deleteVehicle(props.row.id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
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
          label: "Názov vozidla",
          field: "name",
          filterOptions: {
            enabled: true,
            placeholder: "Názov vozidla",
          }
        },
        {
          label: "Dopravca",
          field: "carrier.name",
          filterOptions: {
            enabled: true,
            placeholder: "Dopravca",
          }
        },
        {
          label: "Kapacita",
          field: "capacity",
          type: "number"
        },
        {
          label: "Nástroje",
          field: "tools",
          width: "100px",
        }
      ],
      vehicles: []
    }
  },
  async mounted() {
    this.fetchVehicles();
  },
  methods: {
    async fetchVehicles() {
      let response = await this.$axios.get("/vehicles/get");
      this.vehicles = response.data.vehicles;
    },
    deleteVehicle(id) {
      if(!confirm("Naozaj chcete vymazať toto vozidlo?"))
        return;

      this.$axios.post(`/vehicles/delete/${id}`).then(async () => {
        this.fetchVehicles();
      });
    }
  }
}
</script>