<template>
  <b-container>
    <b-nav pills>
      <b-nav-item to="/users">Zoznam uživateľov</b-nav-item>
      <b-nav-item to="/users/create" active>Pridať uživateľa</b-nav-item>
      <b-nav-item disabled>Úprava uživateľa</b-nav-item>
    </b-nav>
    <hr>
    <b-alert variant="danger" v-show="error !== null" show>
      {{ error }}
    </b-alert>
    <b-form method="POST" @submit.prevent="create">
      <b-form-group>
        <label>Prihlasovacie meno:</label>
        <b-form-input v-model="formData.username" type="text" placeholder="Prihlasovacie meno" required></b-form-input>
      </b-form-group>
      <b-form-group>
        <label>Heslo:</label>
        <b-form-input v-model="formData.password" type="password" placeholder="Heslo" required></b-form-input>
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
      <b-form-group>
        <label>Typ uživateľa:</label>
        <b-select v-model="formData.type" v-if="$store.state.user.info?.type == 3">
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
          <option v-for="carrier in carriers" :key="carrier.id" :value="carrier.id">{{ carrier.username }}</option>
        </b-select>
      </b-form-group>
      <b-form-group>
        <b-button variant="primary" type="submit">Vytvoriť uživateľa</b-button>
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
    if(this.$store.state.user.info?.type != 3)
      return;

    let result = await this.$axios.get("/users/get");
    this.carriers = result.data.users.filter(user => user.type == 2);
  },
  methods: {
    create() {
      this.$axios.post("users/create", this.formData).then(() => {
        this.$router.push("/users");
      }).catch(e => {
        this.error = e.response.data?.message ?? "Nepodarilo sa pridať uživateľa";
      });
    }
  }
}
</script>