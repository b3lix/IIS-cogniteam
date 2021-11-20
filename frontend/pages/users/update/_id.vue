<template>
  <b-container>
    <ul>
      <li><NuxtLink to="/users">Zoznam uživateľov</NuxtLink></li>
      <li><NuxtLink to="/users/create">Pridať uživateľa</NuxtLink></li>
    </ul>
    Upraviť uživateľa:
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="update">
      <b-form-group>
        <b-form-input v-model="formData.username" type="text" placeholder="Meno uživateľa" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="formData.password" type="password" placeholder="Heslo"></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="formData.email" type="email" placeholder="E-mail" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <b-form-input v-model="formData.name" type="text" placeholder="Meno a priezvisko" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <select v-model="formData.type" v-if="$store.state.user.info?.type == 3">
          <option :value="null">Zvoľte typ uživateľa</option>
          <option value="0">Pasažier</option>
          <option value="1">Personál</option>
          <option value="2">Dopravca</option>
          <option value="3">Administrátor</option>
        </select>
      </b-form-group>
      <b-form-group v-if="formData.type == 1 && $store.state.user.info?.type == 3">
        <select v-model="formData.carrier">
          <option :value="0" disabled>Zvoľte dopravcu</option>
          <option v-for="carrier in carriers" :key="carrier.id" :value="carrier.id">{{ carrier.username }}</option>
        </select>
      </b-form-group>
      <b-form-group>
        <b-button variant="primary" type="submit">Upraviť uživateľa</b-button>
        <b-button variant="primary" type="button" @click="deleteUser(id)">Zmazať uživateľa</b-button>
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
        email: null,
        username: null,
        password: null,
        carrier: 0,
        type: 0,
      },

      error: null,
      carriers: []
    }
  },
  async beforeMount() {
    let result = await this.$axios.get(`/users/get/${this.id}`);
    this.formData = result.data;
    this.formData.password = "";

    if(this.$store.state.user.info?.type != 3)
      return;

    result = await this.$axios.get("/users/get");
    this.carriers = result.data.users.filter(user => user.type == 2);
  },
  methods: {
    update() {
      this.$axios.post(`users/update/${this.id}`, this.formData).then(() => {
        this.$router.push("/users");
      }).catch(e => {
        this.error = "Nepodarilo sa aktualizovať uživateľa";
      });
    },
    deleteUser(id) {
      if(!confirm("Naozaj chcete vymazať tohto uživateľa?"))
        return;

      this.$axios.post(`/users/delete/${this.id}`).then(async () => {
        this.$router.push("/users");
      });
    },
  }
}
</script>