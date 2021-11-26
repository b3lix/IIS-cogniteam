<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/vehicles">Zoznam vozidel</b-nav-item>
      <b-nav-item to="/vehicles/create">Pridať vozidlo</b-nav-item>
      <b-nav-item active>Úprava vozidla</b-nav-item>
    </b-nav>
    <hr>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="update">
      <b-form-group>
        <label>Názov vozidla:</label>
        <b-form-input v-model="formData.name" type="text" placeholder="Názov vozidla" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <label>Kapacita vozidla (Maximálny počet rezervácií):</label>
        <b-form-input v-model="formData.capacity" type="number" placeholder="Kapacita vozidla" required></b-form-input>
      </b-form-group>
      <b-form-group v-if="$store.state.user.info?.type == 3">
        <label>Majiteľ (Dopravca) vozidla</label>
        <b-select v-model="formData.carrier">
          <option :value="0" disabled>Zvoľte dopravcu</option>
          <option v-for="carrier in carriers" :key="carrier.id" :value="carrier.id">{{ carrier.name }}</option>
        </b-select>
      </b-form-group>
      <hr>
      <b-form-group>
        <b-button variant="primary" type="submit">Upraviť vozidlo</b-button>
        <b-button variant="danger" type="button" @click="deleteVehicle(id)">Zmazať vozidlo</b-button>
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
        capacity: null,
        carrier: 0
      },

      error: null,
      carriers: []
    }
  },
  async beforeMount() {
    let result = await this.$axios.get(`/vehicles/get/${this.id}`);
    this.formData = result.data;

    if(this.$store.state.user.info?.type != 3)
      return;

    result = await this.$axios.get("/users/get");
    this.carriers = result.data.users.filter(user => user.type == 2);
  },
  methods: {
    update() {
      this.$axios.post(`vehicles/update/${this.id}`, this.formData).then(() => {
        this.$router.push("/vehicles");
      }).catch(e => {
        this.error = e.response.data?.message ?? "Nepodarilo sa aktualizovať vozidlo";
      });
    },
    deleteVehicle(id) {
      if(!confirm("Naozaj chcete vymazať toto vozidlo?"))
        return;

      this.$axios.post(`/vehicles/delete/${this.id}`).then(async () => {
        this.$router.push("/vehicles");
      });
    }
  }
}
</script>