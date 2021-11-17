<template>
  <b-container>
    <div v-if="$store.state.user.info != null">
      Welcome {{ $store.state.user.info.username }}, role: {{ $store.state.user.info.type }}
      <b-button variant="primary" @click="logout">Logout</b-button>
    </div>
    <div v-else>
      <b-alert variant="danger" v-show="error !== null" show>
        {{ error }}
      </b-alert>
      <b-form method="POST" @submit.prevent="login">
        <b-form-group>
          <b-form-input v-model="username" type="text" name="username" placeholder="Username" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <b-form-input v-model="password" type="password" name="password" placeholder="Password" required></b-form-input>
        </b-form-group>
        <b-form-group>
          <b-button variant="primary" type="submit">Login</b-button>
        </b-form-group>
      </b-form>
    </div>
  </b-container>
</template>

<style lang="scss">
</style>

<script>
export default {
  data() {
    return {
      username: null,
      password: null,

      error: null
    }
  },
  created() {
      this.fetchInfo();
  },
  methods: {
    async fetchInfo() {
      this.$axios.get("/auth/info").then(response => {
        this.$store.commit("user/setInfo", response.data);
      });
    },
    async login() {
      this.error = null;

      this.$axios.post("/auth/login", {
        username: this.username,
        password: this.password
      }).then(() => {
        this.fetchInfo();
      }).catch(e => {
        let status = e.response?.status;

        if(status == 401)
          this.error = "Invalid username or password";
        else
          this.error = "Could not contact the server";
      });
    },
    logout() {
      this.$axios.post("/auth/logout");
      this.$store.commit("user/setInfo", null);
    }
  }
}
</script>