<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/stations">Zoznam staníc</NuxtLink></li>
      <li><NuxtLink to="/stations/create">Pridať stanicu</NuxtLink></li>
      <li v-if="$store.state.user.info?.type == 3"><NuxtLink to="/stations/approve">Žiadosti o zmenu</NuxtLink></li>
    </ul>
    Pridať stanicu:
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="create">
      <b-form-group>
        <b-form-input v-model="formData.name" type="text" placeholder="Názov stanice" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="formData.location" type="text" placeholder="Lokácia stanice" required></b-form-input>
      </b-form-group>
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