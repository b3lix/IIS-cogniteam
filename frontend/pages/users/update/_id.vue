<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/users">Zoznam uživateľov</b-nav-item>
      <b-nav-item to="/users/create">Pridať uživateľa</b-nav-item>
      <b-nav-item active>Úprava uživateľa</b-nav-item>
    </b-nav>
    <hr>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="update">
      <b-form-group>
        <label>Prihlasovacie meno:</label>
        <b-form-input v-model="formData.username" type="text" placeholder="Prihlasovacie meno" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <label>Heslo:</label>
        <b-form-input v-model="formData.password" type="password" placeholder="Heslo"></b-form-input>
      </b-form-group>
      <b-form-group>
        <label>E-mail:</label>
        <b-form-input v-model="formData.email" type="email" placeholder="E-mail" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <label v-if="formData.type == 2">Názov dopravcu</label>
        <label v-else>Meno a priezvisko:</label>
        <b-form-input v-model="formData.name" type="text" :placeholder="formData.type == 2 ? 'Názov dopravcu' : 'Meno a priezvisko'" required></b-form-input>
        <b-alert show v-show="formData.type == 2" variant="info" class="mt-2">
          <font-awesome-icon icon="info"></font-awesome-icon>
          V prípade dopravcu sa jedná o názov firmy/dopravcu
        </b-alert>
      </b-form-group>
      <b-form-group v-if="$store.state.user.info?.type == 3">
        <label>Typ uživateľa:</label>
        <b-select v-model="formData.type">
          <option :value="null">Zvoľte typ uživateľa</option>
          <option value="0">Pasažier</option>
          <option value="1">Personál</option>
          <option value="2">Dopravca</option>
          <option value="3">Administrátor</option>
        </b-select>
      </b-form-group>
      <b-form-group v-if="formData.type == 1 && $store.state.user.info?.type == 3">
        <label>Dopravca pre ktorého personál pracuje:</label>
        <b-select v-model="formData.carrier">
          <option :value="0" disabled>Zvoľte dopravcu</option>
          <option v-for="carrier in carriers" :key="carrier.id" :value="carrier.id">{{ carrier.name }}</option>
        </b-select>
      </b-form-group>
      <hr>
      <b-form-group>
        <b-button variant="primary" type="submit">Upraviť uživateľa</b-button>
        <b-button variant="danger" type="button" @click="deleteUser(id)">Zmazať uživateľa</b-button>
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
    this.formData.password = null;

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
        this.error = e.response?.data?.message ?? "Nepodarilo sa aktualizovať uživateľa";
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