<template>
  <div class="page-container">
    <h3>EDIT BOOK</h3>
    <form @submit.prevent="editBook" class="form-container">
      <div class="form-floating mb-3">
        <label for="bookName">Name</label>
        <input v-model="name" id="bookName" class="form-control" placeholder="Book name" required>
      </div>
      <div class="form-floating mb-3">
        <label for="bookContent">Content</label>
        <input v-model="content" id="bookContent" class="form-control" placeholder="Content" required>
      </div>
      <div class="form-floating mb-3">
        <label for="bookAuthor">Author</label>
        <input v-model="author" id="bookAuthor" class="form-control" placeholder="Author" required>
      </div>
      <button type="submit" class="btn btn-primary mt-3">EDIT BOOK</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "EditBook",
  props: {
    bookId: {
      type: String,
      required: true
    },
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
    numericBookId() {
      return Number(this.bookId);
    },
    numericSectionId() {
      return Number(this.sectionId);
    }
  },
  mounted() {
    this.fetchBookDetails();
  },
  methods: {
    async fetchBookDetails() {
      try {
        const response = await fetch(`http://localhost:5000/api/books/${this.numericBookId}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.name = data.name;
          this.content = data.content;
          this.author = data.author;
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("Error fetching book details:", err);
      }
    },
    async editBook() {
      try {
        const response = await fetch(`http://localhost:5000/api/books/${this.numericBookId}`, {
          method: "PUT",
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

        if (response.ok) {
          const data = await response.json();
          console.log(data);
          alert("Book edited successfully.");
          this.$emit('book-updated');
          this.$router.push('/lib-dashboard');
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("Error editing book:", err);
        alert("An error occurred while editing the book.");
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
