<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/stations">Zoznam staníc</b-nav-item>
      <b-nav-item to="/stations/create" active>Pridať stanicu</b-nav-item>
      <b-nav-item to="/stations/approve" v-if="$store.state.user.info?.type == 3">Žiadosti o zmenu</b-nav-item>
      <b-nav-item disabled>Úprava stanice</b-nav-item>
    </b-nav>
    <hr>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="create">
      <b-form-group>
        <label>Názov stanice:</label>
        <b-form-input v-model="formData.name" type="text" placeholder="Názov stanice" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <label>Oblasť/Mesto v ktorej sa stanica nachádza:</label>
        <b-form-input v-model="formData.location" type="text" placeholder="Oblasť/Mesto" required></b-form-input>
      </b-form-group>
      <hr>
      <b-form-group>
        <b-button variant="primary" type="submit">Vytvoriť stanicu</b-button>
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
        formData: {
            name: null,
            location: null
        },

        error: null
    }
  },
  methods: {
    create() {
      this.$axios.post("stations/create", this.formData).then(() => {
        this.$router.push("/stations");
      }).catch(e => {
        this.error = e.response.data?.message ?? "Nepodarilo sa pridať stanicu";
      });
    }
  }
}
</script>