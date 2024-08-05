<template>
  <div class="page-container">
    <nav class="navbar">
      <div class="navbar-logo">
        <img src="/logo.JPG" alt="Logo" class="logo-image">
      </div>
      <div class="navbar-title">USER DASHBOARD</div>
      <div class="navbar-links">
        <router-link to="/user-dashboard/profile" class="navbar-link">User Profile</router-link>
        <router-link to="/user-dashboard/" class="navbar-link">User Home</router-link>
        <router-link to="/user-dashboard/payment" class="navbar-link">Pay</router-link>
        <button @click="handleLogout" class="navbar-link">Logout</button>
      </div>
    </nav>
    <RouterView></RouterView>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userRole: null,
      authToken: null
    };
  },
  created() {
    this.checkAuthorization();
    console.log(this.userRole);
    console.log(this.authToken);
  },
  methods: {
    checkAuthorization() {
      this.authToken = sessionStorage.getItem('token'); // or this.$store.state.authToken
      this.userRole = sessionStorage.getItem('role'); // or this.$store.state.userRole

      if (!this.authToken || !this.userRole) {
        alert("unauthorized");
        this.$router.push({ name: 'login' });
      } 
    },
    handleLogout() {
      sessionStorage.clear(); // Clear all session storage
      this.$router.push({ name: 'HelloWorld' }); // Redirect to login page
    }
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #000; /* Black background */
  color: #fff; /* White text */
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #333; /* Grey background */
  box-sizing: border-box;
}

.navbar-logo {
  display: flex;
  align-items: center;
}

.logo-image {
  height: 40px; /* Adjust the size as needed */
  width: auto;
}

.navbar-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-links {
  display: flex;
  gap: 10px;
  margin-left: auto; /* Push links to the right */
}

.navbar-link {
  background: none;
  border: none;
  color: #fff; /* White text */
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 5px;
}

.navbar-link:hover {
  color: #000; /* Black text on hover */
  background-color: #fff; /* White background on hover */
}

.router-link-active {
  text-decoration: none;
}
</style>
