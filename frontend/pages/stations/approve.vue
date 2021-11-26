<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/stations">Zoznam staníc</b-nav-item>
      <b-nav-item to="/stations/create">Pridať stanicu</b-nav-item>
      <b-nav-item to="/stations/approve" v-if="$store.state.user.info?.type == 3" active>Žiadosti o zmenu</b-nav-item>
      <b-nav-item disabled>Úprava stanice</b-nav-item>
    </b-nav>
    <hr>
    <div v-for="update in updates" :key="update.id">
      [ {{ update.type }} ] Názov: {{ update.name }}, Lokácia: {{ update.location }}
      <a href="#" @click="approveUpdate(update.id)">Schváliť</a>
      <a href="#" @click="deleteUpdate(update.id)">Odstrániť</a>
    </div>
    <vue-good-table :columns="columns" :rows="updates" :search-options="{ enabled: true }" :pagination-options="{ enabled: true }">
      <template slot="table-row" slot-scope="props">
        <span v-if="props.column.field == 'tools'">
          <b-button class="tool" variant="success" @click="approveUpdate(props.row.id)"><font-awesome-icon icon="check"></font-awesome-icon></b-button>
          <b-button class="tool" variant="danger" @click="deleteUpdate(props.row.id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
        </span>
        <span v-else-if="props.column.field == 'type'">
          <template v-if="props.row.type == 0">Pridanie</template>
          <template v-else-if="props.row.type == 1">Úprava</template>
          <template v-else-if="props.row.type == 2">Zmazanie</template>
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
          label: "Typ",
          field: "type",
          filterOptions: {
            enabled: true,
            placeholder: "Typ",
            filterDropdownItems: [
              { value: '0', text: "Pridanie" },
              { value: '1', text: "Úprava" },
              { value: '2', text: "Zmazanie" }
            ]
          }
        },
        {
          label: "Názov stanice",
          field: "original_station.name",
          filterOptions: {
            enabled: true,
            placeholder: "Názov stanice",
          }
        },
        {
          label: "-> Nová hodnota",
          field: "name",
          filterOptions: {
            enabled: true,
            placeholder: "Názov stanice",
          }
        },
        {
          label: "Oblasť/Mesto",
          field: "original_station.location",
          filterOptions: {
            enabled: true,
            placeholder: "Oblasť/Mesto",
          }
        },
        {
          label: "-> Nová hodnota",
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
      updates: []
    }
  },
  async mounted() {
    this.fetchUpdates();
  },
  methods: {
    async fetchUpdates() {
      let response = await this.$axios.get("/stations/get_updates");
      this.updates = response.data.updates;
    },
    deleteUpdate(id) {
      if(!confirm("Naozaj chcete vymazať túto žiadosť?"))
        return;

      this.$axios.post(`/stations/delete_update/${id}`).then(async () => {
        this.fetchUpdates();
      });
    },
    approveUpdate(id) {
      if(!confirm("Naozaj chcete schváliť túto žiadosť?"))
        return;

      this.$axios.post(`/stations/approve_update/${id}`).then(async () => {
        this.fetchUpdates();
      });
    }
  }
}
</script>