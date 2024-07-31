

// import App from './App.vue'
// import router from './router'
// import store from './store'

// new Vue({
//     router,
//     store,
//     render: h => h(App),
//   }).$mount('#app')

  import { createApp } from 'vue';
  import App from './App.vue';
  import router from './router'; // Ensure this import is correct
  const app = createApp(App);
// import Vue from 'vue'



import 'bootstrap/dist/css/bootstrap.css'



  
  app.use(router); // Ensure Vue Router is properly installed

  
  app.mount('#app');
  