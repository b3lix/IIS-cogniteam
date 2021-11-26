<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/users" active>Zoznam uživateľov</b-nav-item>
      <b-nav-item to="/users/create">Pridať uživateľa</b-nav-item>
      <b-nav-item disabled>Úprava uživateľa</b-nav-item>
    </b-nav>
    <hr>
    <vue-good-table :columns="columns" :rows="users" :search-options="{ enabled: true }" :pagination-options="{ enabled: true }">
      <template slot="table-row" slot-scope="props">
        <span v-if="props.column.field == 'tools'">
          <b-button class="tool" variant="success" :to="'/users/update/'  + props.row.id"><font-awesome-icon icon="edit"></font-awesome-icon></b-button>
          <b-button class="tool" variant="danger" @click="deleteUser(props.row.id)"><font-awesome-icon icon="times"></font-awesome-icon></b-button>
        </span>
        <span v-else-if="props.column.field == 'type'">
          <template v-if="props.row.type == 0">Pasažier</template>
          <template v-else-if="props.row.type == 1">Personál</template>
          <template v-else-if="props.row.type == 2">Dopravca</template>
          <template v-else-if="props.row.type == 3">Admin</template>
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
          label: "Prihlasovacie meno",
          field: "username",
          filterOptions: {
            enabled: true,
            placeholder: "Prihlasovacie meno",
          }
        },
        {
          label: "Meno",
          field: "name",
          filterOptions: {
            enabled: true,
            placeholder: "Meno",
          }
        },
        {
          label: "Typ",
          field: "type",
          filterOptions: {
            enabled: true,
            placeholder: "Typ",
            filterDropdownItems: [
              { value: '0', text: "Pasažier" },
              { value: '1', text: "Personál" },
              { value: '2', text: "Dopravca" },
              { value: '3', text: "Admin" },   
            ],
          }
        },
        {
          label: "Email",
          field: "email",
          filterOptions: {
            enabled: true,
            placeholder: "Email",
          }
        },
        {
          label: "Nástroje",
          field: "tools",
          width: "100px",
          sortable: false
        }
      ],
      users: []
    }
  },
  async mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      let response = await this.$axios.get("/users/get");
      this.users = response.data.users;
    },
    deleteUser(id) {
      if(!confirm("Naozaj chcete vymazať tohto uživateľa?"))
        return;

      this.$axios.post(`/users/delete/${id}`).then(async () => {
        this.fetchUsers();
      });
    }
  }
}
</script>