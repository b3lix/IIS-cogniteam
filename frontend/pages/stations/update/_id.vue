<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/stations">Zoznam staníc</NuxtLink></li>
      <li><NuxtLink to="/stations/create">Pridať stanicu</NuxtLink></li>
      <li v-if="$store.state.user.info?.type == 3"><NuxtLink to="/stations/approve">Žiadosti o zmenu</NuxtLink></li>
    </ul>
    Upraviť stanicu:
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="update">
      <b-form-group>
        <b-form-input v-model="formData.name" type="text" placeholder="Názov stanice" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="formData.location" type="text" placeholder="Lokácia stanice" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-button variant="primary" type="submit">Upraviť stanicu</b-button>
        <b-button variant="primary" type="button" @click="deleteStation(id)">Zmazať stanicu</b-button>
      </b-form-group>
    </b-form>
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
      id: this.$route.params.id,

      formData: {
        name: null,
        location: null
      },

      error: null
    }
  },
  async beforeMount() {
    let result = await this.$axios.get(`/stations/get/${this.id}`);
    this.formData = result.data;
  },
  methods: {
    update() {
      this.$axios.post(`/stations/update/${this.id}`, this.formData).then(() => {
        this.$router.push("/stations");
      }).catch(e => {
        this.error = "Nepodarilo sa aktualizovať stanicu";
      });
    },
    deleteStation(id) {
      if(!confirm("Naozaj chcete vymazať túto stanicu?"))
        return;

      this.$axios.post(`/stations/delete/${id}`).then(async () => {
        this.$router.push("/stations");
      });
    }
  }
}
</script>