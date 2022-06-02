<template>
  <div :style="image" class="image"></div>

  <div id="app">
    <h1>Weatherify</h1>
    <p>music meets weather</p>
    <button type="button" v-on:click="start()">Start</button>
  </div>

    <div id="nav">
       <router-link v-if="authenticated" to="/login" v-on:click.native="logout()" replace>Logout</router-link>
    </div>
       <router-view @authenticated="setAuthenticated" />


</template>

<script>
export default {
  name: 'App',
   data() {
      return {
      image: {backgroundImage: "url(https://i.pinimg.com/originals/dd/14/ee/dd14ee38df85f17a1054668f74546c30.jpg)"},
      authenticated: false,
      mockAccount: {
      email: "xxx@bu.edu",
      password: "password"
                }
       };
        },

   start(){
      this.$router.push('/login');
      },
   mounted() {
            if(!this.authenticated) {
                this.$router.replace({ name: "login" });
            }
        },
      methods: {
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                this.authenticated = false;
            }
        }  
}
</script>

<style>
#app {
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
}
  .image {
        height: 500px;
        margin-left: 200px;
        margin-right: 200px;
        background-repeat: no-repeat;
    }
</style>
