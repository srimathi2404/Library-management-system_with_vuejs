<template>
  <div class="page-container">
    <h3>CREATE SECTION</h3>
    <form @submit.prevent="addsection" class="form-container">
      <div class="form-floating mb-3">
        <label for="sectionName">Name</label>
        <input v-model="name" id="sectionName" class="form-control" placeholder="Section name" required>
      </div>
      <div class="form-floating">
        <label for="sectionDescription">Description</label>
        <input v-model="desc" id="sectionDescription" class="form-control" placeholder="Description" required>
      </div>
      <button type="submit" class="btn btn-primary mt-3">ADD</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "CreateSection",
  data() {
    return {
      name: "",
      desc: ""
    };
  },
  methods: {
    async addsection() {
      // Check if name and desc are not empty
      if (!this.name.trim() || !this.desc.trim()) {
        alert("Name and Description are required fields.");
        return;
      }

      try {
        const response = await fetch("http://localhost:5000/api/sections", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
          body: JSON.stringify({
            "name": this.name,
            "desc": this.desc
          }),
        });

        const data = await response.json();
        if (response.status === 200) {
          console.log(data);
          alert("Section created successfully.");
          this.$emit('sec-created');
          this.$router.push('/lib-dashboard');
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log(err);
        // Set values to null in the form
        this.name = "";
        this.desc = "";

        alert("Section already exists");
      }
    }
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #000; /* Black background */
  color: #fff; /* White text */
}

h3 {
  margin-bottom: 20px;
  font-size: 2rem;
}

.form-container {
  width: 100%;
  max-width: 400px;
  background-color: #333; /* Dark background for form container */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.form-floating {
  margin-bottom: 15px;
}

.form-control {
  background-color: #000; /* Black background for input */
  color: #fff; /* White text */
  border: 1px solid #fff; /* White border */
}

.form-control::placeholder {
  color: #aaa; /* Lighter placeholder text */
}

label {
  color: #fff; /* White text */
}

.btn-primary {
  background-color: #6F4E37; /* Brown background for button */
  border: none;
  color: #fff; /* White text */
}

.btn-primary:hover {
  background-color: #fff; /* White background on hover */
  color: #000; /* Black text on hover */
}

.mt-3 {
  margin-top: 20px;
}
</style>
