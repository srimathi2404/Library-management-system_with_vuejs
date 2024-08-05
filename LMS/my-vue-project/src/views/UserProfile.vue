<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>Profile Page</h1>
    </div>

    <div class="profile-content">
      <div class="personal-details-section">
        <h3>Personal Details</h3>
        <div class="personal-details">
          <p><strong>User ID:</strong> {{ user_id }}</p>
          <p><strong>Email:</strong> {{ email }}</p>
          <p><strong>Mobile:</strong> {{ mobile }}</p>
          <p><strong>First Name:</strong> {{ fname }}</p>
          <p><strong>Last Name:</strong> {{ lname }}</p>
        </div>
      </div>

      <div class="profile-section">
        <div class="section-header">
          <h3>Currently Reading</h3>
        </div>
        <div class="card-container">
          <div v-for="bookAccess in currentlyReading" :key="bookAccess.book_id" class="book-card">
            <span v-if="bookAccess.bookDetails">
              <strong class="book-title">{{ bookAccess.bookDetails.name }}</strong>
              <div class="book-author"><i>- by {{ bookAccess.bookDetails.author }}</i></div>
              <div class="book-issue-return">
                Issued on: {{ bookAccess.issue_date }}<br>
                Return by: {{ bookAccess.return_date }}
              </div>
              <button @click="viewContent(bookAccess.bookDetails.id)" class="btn btn-outline-light">View Content</button>
              <button @click="returnBook(bookAccess.book_id)" class="btn btn-outline-light mt-2">Return Book</button>
              <div class="rating-container">
                <p>Rate your book</p>
                <star-rating :rating="bookAccess.userRating" @update:rating="setRating(bookAccess.bookDetails.id, $event)"></star-rating>
              </div>
            </span>
          </div>
          <div v-if="currentlyReading.length === 0">No books currently being read.</div>
        </div>
      </div>

      <div class="profile-section mt-5">
        <div class="section-header">
          <h3>Currently Requested</h3>
        </div>
        <div class="card-container">
          <div v-for="bookAccess in currentlyRequested" :key="bookAccess.book_id" class="book-card">
            <span v-if="bookAccess.bookDetails">
              <strong class="book-title">{{ bookAccess.bookDetails.name }}</strong>
              <div class="book-author"><i>- by {{ bookAccess.bookDetails.author }}</i></div>
              <div class="book-issue-return">
                Requested for {{ bookAccess.no_of_days }} days
              </div>
            </span>
          </div>
          <div v-if="currentlyRequested.length === 0">No books currently requested.</div>
        </div>
      </div>

      <div class="profile-section mt-5">
        <div class="section-header">
          <h3>Books Which Have Been Rejected</h3>
        </div>
        <div class="card-container">
          <div v-for="bookAccess in rejectedBooks" :key="bookAccess.book_id" class="book-card">
            <span v-if="bookAccess.bookDetails">
              <strong class="book-title">{{ bookAccess.bookDetails.name }}</strong>
              <div class="book-author"><i>- by {{ bookAccess.bookDetails.author }}</i></div>
            </span>
          </div>
          <div v-if="rejectedBooks.length === 0">No books have been rejected.</div>
        </div>
      </div>

      <div class="profile-section mt-5">
        <div class="section-header">
          <h3>Bought Books</h3>
        </div>
        <div class="card-container">
          <div v-for="bookAccess in boughtBooks" :key="bookAccess.book_id" class="book-card">
            <span v-if="bookAccess.bookDetails">
              <strong class="book-title">{{ bookAccess.bookDetails.name }}</strong>
              <div class="book-author"><i>- by {{ bookAccess.bookDetails.author }}</i></div>
              <button @click="viewContent(bookAccess.bookDetails.id)" class="btn btn-outline-light">View Content</button>
            </span>
          </div>
          <div v-if="boughtBooks.length === 0">No books bought.</div>
        </div>
      </div>

      <div class="profile-section mt-5">
        <div class="section-header">
          <h3>Past Read Books</h3>
        </div>
        <div class="card-container">
          <div v-for="history in pastReadBooks" :key="history.book_id" class="book-card">
            <strong class="book-title">{{ history.name }}</strong>
            <div class="book-author"><i>- by {{ history.author }}</i></div>
            <div class="book-issue-return">
              Read from: {{ history.issue_date }} to {{ history.return_date }}
            </div>
          </div>
          <div v-if="pastReadBooks.length === 0">No past read books.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import StarRating from '../components/StarRating.vue';

export default {
  name: 'UserProfile',
  components: {
    StarRating
  },
  data() {
    return {
      currentlyReading: [],
      currentlyRequested: [],
      rejectedBooks: [],
      boughtBooks: [],
      pastReadBooks: [],
      books: {},
      lname: '',
      fname: '',
      email: '',
      mobile: '',
      user_id: ''
    };
  },
  created() {
    this.fetchBooks();
    this.personaldetails();
  },
  methods: {
    async personaldetails() {
      this.lname = sessionStorage.getItem('lname');
      this.fname = sessionStorage.getItem('fname');
      this.email = sessionStorage.getItem('email');
      this.mobile = sessionStorage.getItem('mobile');
      this.user_id = sessionStorage.getItem('user_id');
    },
    async fetchBooks() {
      try {
        const response = await axios.get('http://localhost:5000/api/books', {
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const booksArray = response.data;

        // Convert booksArray to an object for easier lookup
        this.books = booksArray.reduce((acc, book) => {
          acc[book.id] = book;
          return acc;
        }, {});

        // Now fetch book access data
        this.fetchBookAccess();
        this.fetchHistory();
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async fetchBookAccess() {
      try {
        const userId = sessionStorage.getItem('user_id');
        const response = await axios.get('http://localhost:5000/api/bookaccess', {
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const bookAccesses = response.data;

        // Filter book access data based on user_id
        const filteredBookAccesses = bookAccesses.filter(bookAccess => bookAccess.user_id === userId);

        // Attach book details and user rating to each filtered book access entry
        for (let bookAccess of filteredBookAccesses) {
          bookAccess.bookDetails = this.books[bookAccess.book_id];
          const ratingResponse = await axios.get(`http://localhost:5000/api/ratings/${bookAccess.book_id}/${userId}`, {
            headers: {
              'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
            }
          });
          bookAccess.userRating = ratingResponse.data.rating || 0;
        }

        this.currentlyReading = filteredBookAccesses.filter(bookAccess => bookAccess.is_approved === 1);
        this.currentlyRequested = filteredBookAccesses.filter(bookAccess => bookAccess.is_approved === 0);
        this.rejectedBooks = filteredBookAccesses.filter(bookAccess => bookAccess.is_approved === -1);
        this.boughtBooks = filteredBookAccesses.filter(bookAccess => bookAccess.is_approved === 2);
      } catch (error) {
        console.log(error)
        console.error('Error fetching book access data:', error);
      }
    },
    async fetchHistory() {
      try {
        const userId = sessionStorage.getItem('user_id');
        const response = await axios.get('http://localhost:5000/api/history', {
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        const histories = response.data;

        // Filter histories based on user_id
        this.pastReadBooks = histories.filter(history => history.user_id === userId);
      } catch (error) {
        console.error('Error fetching history data:', error);
      }
    },
    async setRating(bookId, rating) {
      try {
        const userId = sessionStorage.getItem('user_id');
        await axios.post('http://localhost:5000/api/ratings', {
          book_id: bookId,
          user_id: userId,
          rating: rating
        }, {
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });

        // Update the user's rating locally after successful submission
        const bookAccess = this.currentlyReading.find(b => b.bookDetails.id === bookId);
        if (bookAccess) {
          bookAccess.userRating = rating;
        }

        alert('Rating submitted successfully');
      } catch (error) {
        console.error('Error submitting rating:', error);
      }
    },
    async returnBook(bookId) {
      try {
        const userId = sessionStorage.getItem('user_id');
        const response = await axios.delete('http://localhost:5000/api/bookaccess', {
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
          data: {
            book_id: bookId,
            user_id: userId
          }
        });

        if (response.status === 200) {
          alert('Book returned successfully.');
          this.fetchBookAccess(); // Refresh the book access data
        } else {
          alert('Failed to return the book.');
        }
      } catch (error) {
        console.error('Error returning book:', error);
      }
    },
    viewContent(bookId) {
      // Navigate to the BookContent component
      this.$router.push({ name: 'BookContent', params: { id: bookId } });
    }
  }
};
</script>

<style scoped>
.profile-container {
  background-color: #000; /* Black background */
  color: #fff; /* White text */
  padding: 20px;
  font-family: Arial, sans-serif;
}

.profile-header {
  text-align: center;
  margin-bottom: 40px;
}

.profile-content {
  display: flex;
  flex-direction: column;
}

.personal-details-section {
  margin-bottom: 40px;
}

.profile-section {
  margin-bottom: 40px;
  background-color: #222; /* Darker background for sections */
  padding: 20px;
  border-radius: 8px;
  position: relative;
}

.section-header {
  position: absolute;
  top: -30px;
  left: 20px;
  background-color: #222;
  padding: 0 10px;
  border-radius: 5px;
}

.personal-details p {
  margin: 5px 0;
}

h1, h3 {
  color: #fff; /* White text */
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 30px; /* Gap to avoid overlap with section header */
}

.book-card {
  background-color: #333; /* Dark background for book cards */
  border: 1px solid #fff; /* White border */
  padding: 15px;
  width: calc(33.333% - 20px); /* Three cards per row */
  box-sizing: border-box;
  border-radius: 8px;
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

.book-issue-return {
  color: #fff; /* White text */
  margin-top: 10px; /* Gap between author and issue/return dates */
}

.btn-outline-light {
  border-color: #fff; /* White border */
  color: #fff; /* White text */
  margin-top: 10px;
}

.btn-outline-light:hover {
  background-color: #fff; /* White background on hover */
  color: #000; /* Black text on hover */
}

.rating-container {
  display: flex;
  align-items: center;
  margin-top: 10px; /* Gap between button and rating */
}

.rating-container p {
  margin-right: 10px; /* Space between text and star rating */
}

.mt-5 {
  margin-top: 3rem;
}

ul {
  padding: 0;
}

li {
  list-style: none;
}
</style>
