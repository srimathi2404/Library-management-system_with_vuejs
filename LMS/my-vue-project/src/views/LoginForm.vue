<template>
  <div class="page-container">
    <nav class="navbar">
      <img src="/logo.JPG" alt="Logo" class="logo">
      <div class="navbar-title">BOOK HIVE - LMS</div>
    </nav>
    <div class="center-content">
      <h2>Login</h2>

      <!-- Form for username and password -->
      <form @submit.prevent="submitForm" class="form-container">
        <div class="form-floating mb-3">
          <label>Username</label>
          <input v-model="username" class="form-control" placeholder="username" required>
        </div>

        <div class="form-floating">
          <label for="floatingPassword">Password</label>
          <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Password" required>
        </div>

        <br>

        <button
          @click="submitForm"
          :class="{ 'btn-block': isLoading, 'btn-lg': !isLoading, 'btn': !isLoading, 'btn-secondary': !isLoading, 'disabled': isLoading }"
          type="submit"
          style="background-color: #6F4E37; color: white;"
          :disabled="isLoading"
        >LOGIN</button>
      </form>

      <!-- Show error message if login fails -->
      <p v-if="loginError" style="color: red;">{{ loginError }}</p>
    </div>
  </div>
</template>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: #000; /* Black background */
  color: #fff; /* White text */
}

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
  padding: 1rem;
  background-color: #333; /* Grey background */
  width: 100%;
  box-sizing: border-box;
}

.logo {
  height: 40px; /* Adjust the size as needed */
  width: auto;
  margin-right: 1rem;
}

.navbar-title {
  flex-grow: 1;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.center-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.form-container {
  width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-floating {
  width: 100%;
  margin-bottom: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #fff;
  background-color: #333; /* Grey background for inputs */
  color: #fff; /* White text for inputs */
}

.form-control::placeholder {
  color: #aaa; /* Lighter placeholder text */
}

button {
  width: 100%;
  padding: 0.5rem;
  border: 2px solid #fff; /* White border */
  background-color: #6F4E37; /* Brown background */
  color: #fff; /* White text */
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s, color 0.3s; /* Smooth hover transition */
}

button:hover {
  background-color: #fff; /* White background on hover */
  color: #000; /* Black text on hover */
}
</style>


<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      role: '',
      isLoading: false,
      loginError: ''
    };
  },
  methods: {
    async submitForm() {
      // Check if username and password are not empty
      if (!this.username || !this.password) {
        alert('Username and Password are required.');
        return;
      }
      
      this.isLoading = true;
      const formData = {
        username: this.username,
        password: this.password,
      };
      console.log(formData);
      
      setTimeout(async () => {
        const response = await fetch('http://127.0.0.1:5000/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            // 'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
          },
          body: JSON.stringify(formData),
        });
        const data = await response.json();
        console.log(data);
        if (data.message === "Invalid user") {
          alert('Login Failed. Invalid Username');
          this.email = '';
          this.password = '';
          this.$router.push('/login');
          window.location.reload();
        } else if (data.message === 'Invalid password') {
          alert('Login Failed. Wrong Password');
          this.email = '';
          this.password = '';
          this.$router.push('/login');
          window.location.reload();
        } else {
          if (response.status === 200) {
            console.log('Login successful');
            sessionStorage.setItem("token", JSON.stringify(data.token));
            
            console.log(data.role[0]);
            sessionStorage.setItem("role", JSON.stringify(data.role));
            sessionStorage.setItem("email", JSON.stringify(data.email));
            sessionStorage.setItem("mobile", JSON.stringify(data.mobile));
            sessionStorage.setItem("fname", JSON.stringify(data.fname));
            sessionStorage.setItem("lname", JSON.stringify(data.lname));
            sessionStorage.setItem("user_id", data.username);
            
            if (data.role === 'user') {
              console.log("hey user");
              this.$router.push('/user-dashboard');
            } else {
              console.log("hey lib");
              this.$router.push('/lib-dashboard');
            }
          }
        }
      }, 2000);
    },
  },
};
</script>
