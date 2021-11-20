<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/routes">Zoznam spojov</NuxtLink></li>
      <li><NuxtLink to="/routes/create">Pridať spoj</NuxtLink></li>
    </ul>
    Zoznam spojov: 
    <div v-for="route in routes" :key="route.id">
      Názov: {{ route.name }}
      <NuxtLink :to="'/routes/update/' + route.id">Upraviť</NuxtLink>
      <a href="#" @click="deleteRoute(route.id)">Odstrániť</a>
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
      routes: []
    }
  },
  async mounted() {
    this.fetchRoutes();
  },
  methods: {
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