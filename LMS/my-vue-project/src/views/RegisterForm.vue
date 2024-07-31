<template>
  <div class="page-container">
    <nav class="navbar">
      <img src="/logo.JPG" alt="Logo" class="logo">
      <div class="navbar-title">BOOK HIVE - LMS</div>
    </nav>
    <div class="center-content">
      <h2>Sign Up</h2>
      <form @submit.prevent="handleSignup" class="form-container">
        <div class="form-floating mb-3">
          <label>Username</label>
          <input v-model="username" class="form-control" placeholder="username" required>
        </div>

        <div class="form-floating">
          <label for="floatingPassword">Password</label>
          <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Password" required>
        </div>
        
        <div class="form-floating">
          <label>First Name</label>
          <input v-model="fname" class="form-control" placeholder="first name" required>
        </div>
        
        <div class="form-floating">
          <label>Last Name</label>
          <input v-model="lname" class="form-control" placeholder="last name" required>
        </div>
        
        <div class="form-floating">
          <label>Email</label>
          <input v-model="email" type="email" class="form-control" placeholder="123@gmail.com" required>
        </div>
        
        <div class="form-floating">
          <label>Mobile number</label>
          <input v-model="mobile" class="form-control" placeholder="1111111111" required>
        </div>

        <br>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>

      <!-- Show error message if signup fails -->
      <p v-if="signupError" style="color: red;">{{ signupError }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignUp",
  data() {
    return {
      username: "",
      fname: "",
      lname: "",
      mobile: "",
      email: "",
      password: "",
      role: ["user"],
      signupError: null,
      isLoading: false
    };
  },
  methods: {
    async handleSignup() {
      // Validate mobile number
      if (this.mobile.length !== 10 || !/^\d{10}$/.test(this.mobile)) {
        alert("Mobile number must be exactly 10 digits.");
        return;
      }

      // Check if all fields are filled
      if (!this.username || !this.fname || !this.lname || !this.email || !this.password || !this.mobile) {
        alert("All fields must be filled.");
        return;
      }

      this.isLoading = true;

      try {
        const response = await fetch("http://localhost:5000/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            fname: this.fname,
            lname: this.lname,
            email: this.email,
            mobile: this.mobile,
            password: this.password,
            roles: this.role
          }),
        });

        const data = await response.json();
        if (response.status === 200) {
          console.log(data);
          alert("Account created successfully.");
          this.$router.push('/login');
        } else {
          this.signupError = data.message;
        }
      } catch (err) {
        console.log(err);
        this.signupError = "An error occurred. Please try again.";
      } finally {
        this.isLoading = false;
      }
    }
  },
};
</script>

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
