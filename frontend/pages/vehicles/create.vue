<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/vehicles">Zoznam vozidel</NuxtLink></li>
      <li><NuxtLink to="/vehicles/create">Pridať vozidlo</NuxtLink></li>
    </ul>
    Pridať vozidlo:
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="create">
      <b-form-group>
        <b-form-input v-model="formData.name" type="text" placeholder="Názov vozidla" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="formData.capacity" type="number" placeholder="Kapacita vozidla" required></b-form-input>
      </b-form-group>
      <b-form-group v-if="$store.state.user.info?.type == 3">
        <select v-model="formData.carrier">
          <option :value="0" disabled>Zvoľte dopravcu</option>
          <option v-for="carrier in carriers" :key="carrier.id" :value="carrier.id">{{ carrier.username }}</option>
        </select>
      </b-form-group>
      <b-form-group>
        <b-button variant="primary" type="submit">Vytvoriť vozidlo</b-button>
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
            capacity: null,
            carrier: 0
        },

        error: null,
        carriers: []
    }
  },
  async beforeMount() {
    if(this.$store.state.user.info?.type != 3)
      return;

    let result = await this.$axios.get("/users/get");
    this.carriers = result.data.users.filter(user => user.type == 2);
  },
  methods: {
    create() {
      this.$axios.post("vehicles/create", this.formData).then(() => {
        this.$router.push("/vehicles");
      }).catch(e => {
        this.error = "Nepodarilo sa pridať vozidlo";
      });
    }
  }
}
</script>