import Vue from 'vue'
import VueRouter from 'vue-router'
import App from "../App.vue"
import Login from "../components/login.vue"
import Search from "../components/search.vue"

Vue.use(VueRouter)

export default new VueRouter({
    routes: [
        {
            path: "/",
            redirect: {
                name: "App"
            }
        },
        {
            path: '/App',
            name: 'App',
            component: App
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/search',
            name: 'Search',
            component: Search
        },
    ]
})