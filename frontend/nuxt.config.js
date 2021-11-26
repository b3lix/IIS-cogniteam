export default {
    build: {
        loaders: {
            vue: {
                compiler: require("vue-template-babel-compiler")
            }
        },
    },
    modules: [
        ["@nuxtjs/axios"],
        ["bootstrap-vue/nuxt"],
        ["cookie-universal-nuxt", { alias: "cookies" }]
    ],
    plugins: [
        { src: '~/plugins/vue-good-table', ssr: false }
    ],
    buildModules: [
        "@nuxtjs/fontawesome",
    ],
    css: [
        "@/assets/styles/main.scss"
    ],
    axios: {
        baseUrl: "https://localhost:8000",
        credentials: true
    },
    bootstrapVue: {
        icons: true,
        bootstrapCSS: false,
        bootstrapVueCSS: false,
    },
    fontawesome: {
        icons: {
            solid: ["faBars", "faHome", "faCamera", "faTimes", "faEdit", "faInfo", 
                    "faCheck", "faClock", "faCalendar", "faSignInAlt", "faSignOutAlt", 
                    "faBus", "faSearch", "faEuroSign", "faPrint", "faArrowRight", "faDotCircle"]
        }
    }
}