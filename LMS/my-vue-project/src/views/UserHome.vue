<template>
  <div class="page-container">
    <form class="d-flex mx-auto search-form">
      <input v-model="searchQuery" class="form-control me-3 shadow-lg border-white text-white bg-black" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-light bg-black text-white" type="button" @click="clearSearch">Clear</button>
    </form>

    <div class="container mt-4">
      <div class="section-container">
        <div v-for="section in filteredSections" :key="section.id" class="section-card mb-4">
          <div class="section-header">
            <h3 class="section-title">{{ section.name }}</h3>
          </div>
          <div class="card-container">
            <div v-for="book in filteredBooks(section)" :key="book.id" class="book-card">
              <div>
                <strong class="book-title">{{ book.name }}</strong>
                <div class="book-author"><i>- by {{ book.author }}</i></div>
                <div>
                  <star-rating :rating="book.avg_rating" :read-only="true"></star-rating>
                </div>
                <div class="mt-3">
                  <template v-if="book.accessStatus === 'currentlyAccessed'">
                    <span>Already Reading</span>
                  </template>
                  <template v-else-if="book.accessStatus === 'requested'">
                    <span>Requested</span>
                  </template>
                  <template v-else-if="book.accessStatus === 'rejected'">
                    <button type="button" @click="requestBook(book.id)" class="btn btn-outline-light">Request Again</button>
                  </template>
                  <template v-else>
                    <button type="button" @click="requestBook(book.id)" class="btn btn-outline-light">Request Book</button>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view @section-updated="handleSectionUpdated" @book-added="handleSectionUpdated"></router-view>
  </div>
</template>

<script>
import StarRating from '../components/StarRating.vue';

export default {
  name: "UserHome",
  components: {
    StarRating
  },
  data() {
    return {
      section_item: [],
      book_item: [],
      book_access: [],
      searchQuery: ''
    };
  },
  computed: {
    filteredSections() {
      if (!this.searchQuery) return this.section_item;
      return this.section_item.filter(section => section.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        this.filteredBooks(section).length > 0);
    },
    filteredBooks() {
      return (section) => {
        if (section.name.toLowerCase().includes(this.searchQuery.toLowerCase())) {
          return this.book_item.filter(book => book.section_id === section.id);
        }
        return this.book_item.filter(book => book.section_id === section.id && (book.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || book.author.toLowerCase().includes(this.searchQuery.toLowerCase())));
      };
    }
  },
  mounted() {
    this.get_all_section();
    this.get_all_books();
    this.get_book_access();
  },
  methods: {
    clearSearch() {
      this.searchQuery = '';
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
          this.updateBookAccessStatus();
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
    async get_book_access() {
      try {
        const response = await fetch("http://localhost:5000/api/bookaccess", {
          method: "GET",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });

        const data = await response.json();
        if (response.status === 200) {
          this.book_access = data;
          this.updateBookAccessStatus();
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
    updateBookAccessStatus() {
      this.book_item.forEach(book => {
        const access = this.book_access.find(ba => ba.book_id === book.id && ba.user_id === sessionStorage.getItem('user_id'));
        if (access) {
          if (access.is_approved === 1) {
            book.accessStatus = 'currentlyAccessed';
          } else if (access.is_approved === 0) {
            book.accessStatus = 'requested';
          } else if (access.is_approved === -1) {
            book.accessStatus = 'rejected';
          }
        } else {
          book.accessStatus = null;
        }
      });
    },
    async requestBook(bookId) {
      const days = prompt("Enter the number of days you need the book:");
      if (!days || isNaN(days)) {
        alert("Please enter a valid number of days.");
        return;
      }

      try {
        const response = await fetch(`http://localhost:5000/api/bookaccess`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
          body: JSON.stringify({
            no_of_days: Number(days),
            book_id: bookId,
            user_id: sessionStorage.getItem('user_id')
          })
        });

        if (!response.ok) {
          throw new Error('Failed to request book');
        }

        const result = await response.json();
        if (result.message !== "") {
          alert(`Response: ${result.message}`);
        } else {
          alert(`Book requested for ${days} days.`);
        }

        this.get_book_access(); // Refresh book access data
      } catch (error) {
        console.error('Error requesting book:', error);
        alert('There was an error processing your request.');
      }
    },
    handleSectionUpdated() {
      this.get_all_section();
      this.get_all_books(); // Refresh the list of sections when an update event is received
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

.search-form {
  margin: 20px 0;
  max-width: 600px; /* Keep the search bar short */
}

.form-control {
  background-color: #222; /* Darker background for input */
  color: #fff; /* White text */
}

.form-control:focus {
  background-color: #222; /* Maintain dark background on focus */
  color: #fff; /* Maintain white text on focus */
}

.btn-outline-light {
  border-color: #fff; /* White border */
  color: #fff; /* White text */
}

.btn-outline-light:hover {
  background-color: #444; /* Darker background on hover */
  color: #fff; /* White text on hover */
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

.text-decoration-none {
  cursor: pointer;
  color: #fff; /* White text */
  text-decoration: underline;
}

.text-decoration-none:hover {
  color: #ccc; /* Lighter text on hover */
}

.mt-3 {
  margin-top: 20px;
}
</style>
