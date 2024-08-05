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
        <!-- <button @click="createDesktopShortcut" class="navbar-link">Create Shortcut</button> -->
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
  },
  methods: {
    checkAuthorization() {
      this.authToken = sessionStorage.getItem('token');
      this.userRole = sessionStorage.getItem('role');

      if (!this.authToken || !this.userRole) {
        alert("unauthorized");
        this.$router.push({ name: 'login' });
      }
    },
    handleLogout() {
      sessionStorage.clear();
      this.$router.push({ name: 'HelloWorld' });
    },
    async createDesktopShortcut() {
      try {
        const response = await fetch('http://localhost:5000/add-to-desktop', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
          body: JSON.stringify({
            name: 'MyApp',
            icon: 'C:\\Users\\18049\\Desktop\\icon.ico',  // Adjust this path to your .ico file
            url: 'http://localhost:8080/'    // The URL of your web application
          })
        });

        const data = await response.json();
        alert(data.Message || data.Error);
      } catch (error) {
        console.error("Error creating shortcut:", error);
      }
    }
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #000;
  color: #fff;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #333;
  box-sizing: border-box;
}

.navbar-logo {
  display: flex;
  align-items: center;
}

.logo-image {
  height: 40px;
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
  margin-left: auto;
}

.navbar-link {
  background: none;
  border: none;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 5px;
}

.navbar-link:hover {
  color: #000;
  background-color: #fff;
}

.router-link-active {
  text-decoration: none;
}
</style>
