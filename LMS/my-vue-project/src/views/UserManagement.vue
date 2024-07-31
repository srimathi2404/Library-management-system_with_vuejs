<template>
  <div class="page-container">
    <h1>User Management</h1>
    <div class="container mt-4">
      <div class="section-container">
        <div v-for="user in users" :key="user.id" class="section-card mb-4">
          <div class="section-header">
            <h3 class="section-title">{{ user.id }}</h3>
          </div>
          <div class="card-container">
            <div v-for="access in filteredBookAccesses(user.id)" :key="access.id" class="book-card">
              <div v-for="book in filteredBooks(access.book_id)" :key="book.id">
                <div>
                  <strong class="book-title">Book: {{ book.name }}</strong>
                  <div class="book-author"><i>Author: {{ book.author }}</i></div>
                  <div class="mt-2">
                    <br>
                    <div v-if="access.is_approved === 1">
                      Issued On: {{ access.issue_date }}<br>
                      Return By: {{ access.return_date }}
                    </div>
                    <div v-if="access.is_approved === 0">
                      <div>Book requested for {{ access.no_of_days }} days</div>
                      <br>
                      <button @click="updateApproval(access.book_id, 1, access.user_id)" class="btn btn-outline-light me-2">Grant</button>
                    
                      <button @click="updateApproval(access.book_id, -1, access.user_id)" class="btn btn-outline-light">Revoke</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserManagement',
  data() {
    return {
      bookAccesses: [],
      book_item: [],
      users: [],
      is_approved: 0
    };
  },
  mounted() {
    this.fetchBookAccesses();
    this.get_all_books();
    this.get_all_user();
  },
  computed: {
    filteredBookAccesses() {
      return (userId) => this.bookAccesses.filter(access => access.user_id === userId && access.is_approved !== -1);
    },
    filteredBooks() {
      return (bookId) => this.book_item.filter(book => book.id === bookId);
    }
  },
  methods: {
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
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log("error");
        console.log(err);
      }
    },
    fetchBookAccesses() {
      axios.get('http://localhost:5000/api/bookaccess', {
        headers: {
          'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
        }
      })
      .then(response => {
        this.bookAccesses = response.data;
      })
      .catch(error => {
        console.error("There was an error fetching the book accesses:", error);
      });
    },
    updateApproval(bookAccessId, approvalStatus, user_id) {
      // Update local data for immediate feedback
      this.is_approved = approvalStatus;

      // Send a PATCH request to update the server
      axios.patch('http://localhost:5000/api/bookaccess', {
        is_approved: approvalStatus,
        book_id: bookAccessId,
        user_id: user_id
      }, {
        headers: {
          'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
        }
      })
      .then(response => {
        console.log('Approval status updated:', response.data);
        this.fetchBookAccesses();
        this.get_all_books();
      })
      .catch(error => {
        console.error('Error updating approval status:', error);
        // Optionally revert the change in case of error
        this.is_approved = 0; // revert back to the original state if error occurs
      });
    },
    async get_all_user() {
      try {
        const response = await fetch("http://localhost:5000/api/users", {
          method: "GET",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });

        const data = await response.json();
        if (response.status === 200) {
          this.users = data;
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

.btn-outline-light {
  border-color: #fff; /* White border */
  color: #fff; /* White text */
}

.btn-outline-light:hover {
  background-color: #fff;
  color: #000;
}
</style>
