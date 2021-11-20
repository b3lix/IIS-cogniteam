<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/users">Zoznam uživateľov</NuxtLink></li>
      <li><NuxtLink to="/users/create">Pridať uživateľa</NuxtLink></li>
    </ul>
    Uživatelia: 
    <div v-for="user in users" :key="user.id">
      Name: {{ user.username }}, Typ: {{ user.type }}, Meno: {{ user.name }}, Email: {{ user.email }}
      <NuxtLink :to="'/users/update/' + user.id">Upraviť</NuxtLink>
      <a href="#" @click="deleteUser(user.id)">Odstrániť</a>
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