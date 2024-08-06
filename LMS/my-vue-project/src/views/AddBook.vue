<template>
  <div class="page-container">
    <h3>ADD BOOK</h3>
    <form @submit.prevent="addBook" class="form-container">
      <div class="form-floating mb-3">
        <label for="bookName">Name</label>
        <input v-model="name" id="bookName" class="form-control" placeholder="Book name" required>
      </div>
      <div class="form-floating mb-3">
        <label for="bookContent">Content</label>
        <textarea v-model="content" id="bookContent" class="form-control content-textarea" placeholder="Content" required></textarea>
      </div>
      <div class="form-floating mb-3">
        <label for="bookAuthor">Author</label>
        <input v-model="author" id="bookAuthor" class="form-control" placeholder="Author" required>
      </div>
      <button type="submit" class="btn btn-primary mt-3">ADD BOOK</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "AddBook",
  props: {
    sectionId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      name: "",
      content: "",
      author: ""
    };
  },
  computed: {
    numericSectionId() {
      console.log("computed working")
      console.log(this.sectionId)
      return Number(this.sectionId); // Convert sectionId to number
    }
  },
  methods: {
    async addBook() {
      try {
        const response = await fetch("http://localhost:5000/api/books", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
          body: JSON.stringify({
            name: this.name,
            content: this.content,
            author: this.author,
            section_id: this.numericSectionId
          })
        });

        if (response.status === 200) {
          const data = await response.json();
          console.log(data);
          alert("Book added successfully.");
          this.$emit('book-added');
          this.$router.push('/lib-dashboard');
        }
        else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        }
        else if (response.status === 400) {
          alert("Book name already exists")
          this.$router.push('/lib-dashboard')
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log(err);
        alert("Book already exists");
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

/* Additional CSS to make the content block bigger */
.content-textarea {
  height: 200px; /* Adjust this value as needed to make the content block bigger */
}
</style>
