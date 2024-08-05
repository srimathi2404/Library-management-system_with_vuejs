<template>
    <div class="page-container">
      <div class="content-container">
        <h1 class="page-title">Payment Page</h1>
        <form class="payment-form" @submit.prevent="submitPayment">
          <div class="mb-3">
            <label for="book" class="form-label">Select Book</label>
            <select v-model="selectedBook" class="form-control" id="book" required>
              <option v-for="book in unpaidBooks" :key="book.id" :value="book.id">
                {{ book.name }}
              </option>
            </select>
          </div>
          <div class="mb-3">
            <label for="upiId" class="form-label">UPI ID</label>
            <input v-model="upiId" type="text" class="form-control" id="upiId" placeholder="Enter UPI ID" required>
          </div>
          <button type="submit" class="btn btn-outline-light bg-black text-white">Submit Payment</button>
        </form>
        <div v-if="message" class="alert alert-info mt-3">{{ message }}</div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        books: [],
        paidBooks: [],
        selectedBook: null,
        upiId: '',
        message: ''
      };
    },
    mounted() {
      this.getBooks();
      this.getPaidBooks();
      this.getUPIId();
    },
    computed: {
      unpaidBooks() {
        const paidBookIds = this.paidBooks.map(book => book.book_id);
        return this.books.filter(book => !paidBookIds.includes(book.id));
      }
    },
    methods: {
      async getBooks() {
        try {
          const response = await fetch('http://localhost:5000/api/books', {
            headers: {
              'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
            }
          });
          const data = await response.json();
          if (response.status === 200) {
            this.books = data;
          } else {
            console.error("Failed to fetch books");
          }
        } catch (error) {
          console.error("Error:", error);
        }
      },
      async getPaidBooks() {
        const user_id = sessionStorage.getItem('user_id');
        try {
          const response = await fetch(`http://localhost:5000/api/payment/${user_id}`, {
            headers: {
              'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
            }
          });
          const data = await response.json();
          if (response.status === 200) {
            this.paidBooks = data.paid_books || [];
          } else {
            console.error("Failed to fetch paid books");
          }
        } catch (error) {
          console.error("Error:", error);
        }
      },
      async getUPIId() {
        const user_id = sessionStorage.getItem('user_id');
        try {
          const response = await fetch(`http://localhost:5000/api/payment/${user_id}`, {
            headers: {
              'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
            }
          });
          const data = await response.json();
          if (response.status === 200) {
            this.upiId = data.upi_id || '';
          } else {
            console.error("Failed to fetch UPI ID");
          }
        } catch (error) {
          console.error("Error:", error);
        }
      },
      async submitPayment() {
        if (!this.selectedBook || !this.upiId) {
          this.message = 'Please fill in all the fields.';
          return;
        }
  
        const user_id = sessionStorage.getItem('user_id');
        const section_id = this.books.find(book => book.id === this.selectedBook).section_id;
  
        try {
          const response = await fetch('http://localhost:5000/api/payment', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
            },
            body: JSON.stringify({
              user_id,
              book_id: this.selectedBook,
              section_id,
              upi_id: this.upiId
            })
          });
          const data = await response.json();
          this.message = data.message;
        } catch (error) {
          console.error("Error:", error);
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
  
  .content-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 400px;
    padding: 20px;
  }
  
  .page-title {
    margin-bottom: 20px;
  }
  
  .payment-form {
    width: 100%;
  }
  
  .form-control, .form-select {
    background-color: #222; /* Darker background for input */
    color: #fff; /* White text */
    width: 100%;
  }
  
  .form-control:focus, .form-select:focus {
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
  
  .alert-info {
    color: #000;
    background-color: #d1ecf1;
    border-color: #bee5eb;
    margin-top: 20px;
  }
  </style>
  