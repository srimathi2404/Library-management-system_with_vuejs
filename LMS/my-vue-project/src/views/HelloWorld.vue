<template>
  <div class="page-container">
    <nav class="navbar">
      <img src="/logo.JPG" alt="Logo" class="logo">
      <div class="navbar-title">BOOK HIVE - LMS</div>
    </nav>
    <div class="center-content">
      <b><router-link to="/login" class="button">Login</router-link></b>
      <b><router-link to="/register" class="button">Register</router-link></b>
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

.button {
  display: inline-block;
  margin: 1rem;
  padding: 0.5rem 1rem;
  border: 2px solid #fff; /* White border */
  background-color: #000; /* Black background */
  color: #fff; /* White text */
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s, color 0.3s; /* Smooth hover transition */
}

.button:hover {
  background-color: #fff; /* White background on hover */
  color: #000; /* Black text on hover */
}
</style>
