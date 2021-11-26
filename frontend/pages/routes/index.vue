<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/routes" active>Zoznam spojov</b-nav-item>
      <b-nav-item to="/routes/create">Pridať spoj</b-nav-item>
      <b-nav-item disabled>Úprava spoju</b-nav-item>
    </b-nav>
    <hr>
    <vue-good-table :columns="columns" :rows="routes" :search-options="{ enabled: true }" :pagination-options="{ enabled: true }">
      <template slot="table-row" slot-scope="props">
        <span v-if="props.column.field == 'tools'">
          <b-button class="tool" variant="success" :to="'/routes/update/'  + props.row.id"><font-awesome-icon icon="edit"></font-awesome-icon></b-button>
          <b-button class="tool" variant="danger" @click="deleteRoute(props.row.id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
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
          label: "Názov spoju",
          field: "name",
          filterOptions: {
            enabled: true,
            placeholder: "Názov spoju",
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
          label: "Počet zastávok",
          field: "stops",
          type: "number"
        },
        {
          label: "Cena za zastávku",
          field: "price",
          type: "decimal",
          formatFn: this.formatPrice
        },
        {
          label: "Nástroje",
          field: "tools",
          width: "100px",
          sortable: false
        }
      ],
      routes: []
    }
  },
  async mounted() {
    this.fetchRoutes();
  },
  methods: {
    formatPrice: function(value) {
      return value + "€";
    },
    async fetchRoutes() {
      let response = await this.$axios.get("/routes/get");
      this.routes = response.data.routes;
    },
    deleteRoute(id) {
      if(!confirm("Naozaj chcete vymazať tento spoj?"))
        return;

      this.$axios.post(`/routes/delete/${id}`).then(async () => {
        this.fetchRoutes();
      });
    }
  }
}
</script>