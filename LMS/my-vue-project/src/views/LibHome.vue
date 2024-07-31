<template>
  <div class="page-container">
    <form class="d-flex mx-auto search-form" @submit.prevent="searchProducts">
      <input v-model="searchQuery" class="form-control me-3 shadow-lg border-white text-white bg-black" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-light bg-black text-white" type="submit">
        <i class="bi bi-search"></i> Search
      </button>
    </form>
    <br>
    <br>
    <div class="container mt-4">
      <div class="section-container">
        <div v-for="section in section_item" :key="section.id" class="section-card mb-4">
          <div class="section-header">
            <h3 class="section-title">{{ section.name }}</h3>
            <div class="section-actions">
              <router-link :to="{ name: 'lib-edit-section', params: { id: section.id } }" class="btn btn-outline-light me-2">Edit section</router-link>
              <button type="button" @click="confirmDelete(section.id)" class="btn btn-outline-light me-2">Delete section</button>
              <router-link :to="{ name: 'lib-add-book', params: { sectionId: section.id } }" class="btn btn-outline-light ms-2">Add Book</router-link>
            </div>
          </div>
          <div class="card-container">
            <div v-for="book in filteredBooks(section.id)" :key="book.id" class="book-card">
              <div>
                <strong class="book-title">{{ book.name }}</strong>
                <div class="book-author"><i>- by {{ book.author }}</i></div>
                <div class="book-secondary-sections mt-2">
                  <span v-if="filteredSecondarySections(book.id).length">Also belongs to: </span>
                  <span v-for="(sec, index) in filteredSecondarySections(book.id)" :key="sec.id">
                    {{ sec.section_name }}<span v-if="index < filteredSecondarySections(book.id).length - 1">, </span>
                  </span>
                </div>
                <div class="d-flex justify-content-between mt-3 mb-3">
                  <router-link :to="{ name: 'lib-edit-book', params: { bookId: book.id, sectionId: book.section_id } }" class="btn btn-outline-light me-2">Edit Book</router-link>
                  <button type="button" @click="confirmDeleteBook(book.id)" class="btn btn-outline-light">Delete Book</button>
                </div>
                <div class="mt-2 text-center">
                  <router-link :to="{ name: 'lib-add-secondary-section', params: { bookId: book.id, sectionId: book.section_id } }" class="text-decoration-none">add ss</router-link>
                  <span> | </span>
                  <router-link :to="{ name: 'lib-del-secondary-section', params: { bookId: book.id, sectionId: book.section_id } }" class="text-decoration-none">delete ss</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view @section-updated="handleSectionUpdated" @book-added="handleSectionUpdated" @sec-created="handleSectionUpdated" @book-updated="handleSectionUpdated"></router-view>
    <router-link to="/lib-dashboard/Create-Section" class="create-section-btn">+</router-link>
  </div>
</template>

<script>
export default {
  name: "SectionName",
  data() {
    return {
      section_item: [],
      book_item: [],
      secondary_sec: [],
      searchQuery: ''
    };
  },
  mounted() {
    this.get_all_section();
    this.get_all_books();
    this.get_all_secondary_sec();
    console.log(this.secondary_sec);
  },
  computed: {
    filteredBooks() {
      return (sectionId) => this.book_item.filter(book => book.section_id === sectionId);
    },
    filteredSecondarySections() {
      return (bookId) => this.secondary_sec.filter(sec => sec.book_id === bookId);
    }
  },
  methods: {
    async searchProducts() {
      try {
        const response = await fetch(`http://localhost:5000/api/search/${this.searchQuery}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.section_item = data.sections;
          this.book_item = data.books;
          console.log(this.book_item);
          console.log(this.section_item);
        } else {
          console.error('Failed to fetch products');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    async get_all_secondary_sec() {
      try {
        const response = await fetch("http://localhost:5000/api/secondarysection", {
          method: "GET",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const data = await response.json();
        if (response.status === 200) {
          this.secondary_sec = data;
          console.log(this.secondary_sec);
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("error");
      }
    },
    async get_all_section() {
      try {
        const response = await fetch("http://localhost:5000/api/sections", {
          method: "GET",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const data = await response.json();
        if (response.status === 200) {
          this.section_item = data;
          console.log(this.section_item);
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("error");
      }
    },
    async get_all_books() {
      try {
        const response = await fetch("http://localhost:5000/api/books", {
          method: "GET",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const data = await response.json();
        if (response.status === 200) {
          this.book_item = data;
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("error");
      }
    },
    async del_section(id) {
      try {
        const response = await fetch(`http://localhost:5000/api/sections/${id}`, {
          method: "DELETE",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const message = await response.json();
        console.log(message);
        if (response.status === 200) {
          alert("Section deleted successfully");
          this.get_all_section();
          this.get_all_books();
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("error");
      }
    },
    confirmDelete(id) {
      if (window.confirm("Are you sure you want to delete this section?")) {
        this.del_section(id);
      }
    },
    handleSectionUpdated() {
      this.get_all_section();
      this.get_all_books();
    },
    confirmDeleteBook(id) {
      if (window.confirm("Are you sure you want to delete this book?")) {
        this.del_book(id);
      }
    },
    async del_book(id) {
      try {
        const response = await fetch(`http://localhost:5000/api/books/${id}`, {
          method: "DELETE",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const message = await response.json();
        console.log(message);
        if (response.status === 200) {
          alert("Book deleted successfully");
          this.get_all_section();
          this.get_all_books();
        } else if (response.status === 401 || response.status === 403) {
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("error");
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
  background-color: #000; /* Black background */
  color: #fff; /* White text */
  min-height: 100vh;
}

.search-form {
  margin: 20px 0;
  max-width: 600px; /* Keep the search bar short */
}

.form-control {
  background-color: #000; /* Black background for input */
  color: #fff; /* White text */
}

.btn-outline-light {
  border-color: #fff; /* White border */
  color: #fff; /* White text */
}

.section-container {
  display: flex;
  flex-direction: column;
  gap: 20px; /* Gap between section cards */
}

.section-card {
  background-color: #000; /* Black background */
  border: 1px solid #fff; /* White border */
  padding: 15px;
  margin-bottom: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px; /* Gap between section header and book cards */
}

.section-title {
  font-size: 1.8rem; /* Increased font size for section name */
  color: #fff; /* White text */
}

.section-actions .btn {
  margin-left: 10px; /* Increase horizontal gap */
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px; /* Gap between book cards */
}

.book-card {
  background-color: #000; /* Black background */
  border: 1px solid #fff; /* White border */
  padding: 15px;
  width: calc(33.333% - 20px); /* Three cards per row */
  box-sizing: border-box;
}

.book-title {
  font-size: 1.5rem; /* Larger font size for book name */
  color: #fff; /* White text */
}

.book-author {
  color: #fff; /* White text */
  font-style: italic;
  margin-top: 10px; /* Gap between author and next line */
}

.book-secondary-sections {
  color: #fff; /* White text */
  margin-top: 10px; /* Gap between author and secondary sections */
}

.d-flex {
  margin-bottom: 10px; /* Gap between Edit/Delete buttons and add/delete secondary section links */
}

.text-decoration-none {
  cursor: pointer;
  color: #fff; /* White text */
  text-decoration: underline;
}

.text-decoration-none:hover {
  color: #ccc; /* Lighter text on hover */
}

.create-section-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #fff;
  color: #000;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  text-decoration: none;
}
</style>
