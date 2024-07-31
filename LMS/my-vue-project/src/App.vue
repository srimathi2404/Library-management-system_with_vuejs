
<script setup>
import {  RouterView } from 'vue-router'
//import HelloWorld from './views/HelloWorld.vue';
</script>
<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
<!-- <h1>welcome to LIB APP</h1> -->

  <RouterView />
</template>
<script>



export default {
  name: 'App',
  components: {

    
  },
  data(){
    return{}
  },
  methods:{},
  computed:{},
  // beforeCreate(){
  //   console.log("Creating app.");
  //   this.$store.commit("intialiseStore")
  // }
  
}


</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
