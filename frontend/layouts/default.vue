<template>
  <b-container v-if="loaded">
    <div>
      <b-navbar toggleable="lg">
        <b-navbar-brand to="/">Domov</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item v-if="[2, 3].includes($store.state.user.info?.type)" to="/users">Uživatelia</b-nav-item>
            <b-nav-item v-if="[2, 3].includes($store.state.user.info?.type)" to="/stations">Stanice</b-nav-item>
            <b-nav-item v-if="[2, 3].includes($store.state.user.info?.type)" to="/vehicles">Vozidlá</b-nav-item>
            <b-nav-item v-if="[2, 3].includes($store.state.user.info?.type)" to="/routes">Spoje</b-nav-item>
            <b-nav-item v-if="[1, 3].includes($store.state.user.info?.type)" to="/seats">Rezervácie</b-nav-item>
            <b-nav-item v-if="[1, 3].includes($store.state.user.info?.type)" to="/vehicles/station">Režim vodiča</b-nav-item>
            <b-nav-item v-if="[0, 3].includes($store.state.user.info?.type)" to="/seats/my">Moje rezervácie</b-nav-item>
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <template v-if="$store.state.user.info == null">
              <b-button size="sm" variant="primary" class="m-1" v-b-modal.modal-login>Prihlásiť</b-button>
              <b-button size="sm" variant="primary" class="m-1" v-b-modal.modal-register>Vytvoriť účet</b-button>
            </template>
            <b-nav-item-dropdown v-else right>
              <template #button-content>
                {{ $store.state.user.info.username }}
              </template>
              <b-dropdown-item @click="logout">Odhlásiť sa</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <b-modal ref="modal_login" id="modal-login" title="Prihlásenie" hide-footer>
      <b-alert variant="danger" v-show="login_error !== null" show>
        {{ login_error }}
      </b-alert>
      <b-form method="POST" @submit.prevent="login">
        <b-form-group>
          <label>Prihlasovacie meno:</label>
          <b-form-input v-model="loginFormData.username" type="text" name="username" placeholder="Prihlasovacie meno" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <label>Prihlasovacie heslo:</label>
          <b-form-input v-model="loginFormData.password" type="password" name="password" placeholder="Heslo" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <b-button class="form-control" variant="primary" type="submit" >Prihlásiť</b-button>
        </b-form-group>
      </b-form>
    </b-modal>
    <b-modal id="modal-register" title="Registrácia" hide-footer>
      <b-alert variant="danger" v-show="register_error !== null" show>
        {{ register_error }}
      </b-alert>
      <b-form method="POST" @submit.prevent="register">
        <b-form-group>
          <label>Prihlasovacie meno:</label>
          <b-form-input v-model="registerFormData.username" type="text" name="username" placeholder="Prihlasovacie meno (Viac ako 3 znaky)" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <label>Heslo:</label>
          <b-form-input v-model="registerFormData.password" type="password" name="password" placeholder="Heslo (Viac ako 3 znaky)" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <label>*Meno a priezvisko:</label>
          <b-form-input v-model="registerFormData.name" type="text" name="name" placeholder="Meno a priezvisko"></b-form-input>
        </b-form-group>
        <b-form-group>
          <label>E-mail:</label>
          <b-form-input v-model="registerFormData.email" type="email" placeholder="E-mail" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <b-button class="form-control" variant="primary" type="submit">Vytvoriť účet</b-button>
        </b-form-group>
      </b-form>
    </b-modal>
    <hr>
    <Nuxt/>
  </b-container>
</template>

<script>

export default {
  data() {
    return {
      loginFormData: {
        username: null,
        password: null,
      },

      registerFormData: {
        username: null,
        password: null,
        name: null,
        email: null
      },

      login_error: null,
      register_error: null,

      loaded: false
    }
  },
  async created() {
    await this.fetchInfo();
  },
  methods: {
    async fetchInfo() {
      this.$axios.get("/users/info").then(response => {
        this.$store.commit("user/setInfo", response.data);

        if(!this.loaded)
          this.loaded = true;
      }).catch(() => {
        if(!this.loaded)
          this.loaded = true; 
      })
    },
    async login() {
      this.login_error = null;

      this.$axios.post("/auth/login", this.loginFormData).then(() => {
        this.fetchInfo();
        this.$refs.modal_login.hide();
      }).catch(e => {
        this.login_error = e.response?.data?.message ?? "Neočakávaná chyba";
      });
    },
    async register() {
      this.register_error = null;

      this.$axios.post("/auth/register", this.registerFormData).then(() => {
        this.register_error = "Účet bol úspešne vytvorený";
      }).catch(e => {
        this.register_error = e.response?.data?.message ?? "Neočakávaná chyba";
      });
    },
    logout() {
      this.$axios.post("/auth/logout");
      this.$store.commit("user/setInfo", null);
      this.$router.push("/");
    }
  }
}
</script>
