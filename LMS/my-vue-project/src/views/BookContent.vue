<template>
  <div class="page-container">
    <h1>{{ book.name }}</h1>
    <h2>by {{ book.author }}</h2>
    <div v-html="book.content" class="book-content"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BookContent',
  props: {
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      book: {}
    };
  },
  created() {
    this.fetchBookContent();
  },
  methods: {
    async fetchBookContent() {
      try {
        const token = JSON.parse(sessionStorage.getItem('token'));
        const response = await axios.get(`http://localhost:5000/api/books/${this.id}`, {
          headers: {
            'Authentication-Token': token
          }
        });
        this.book = response.data;
      } catch (error) {
        console.error('Error fetching book content:', error);
      }
    }
  }
};
</script>

<style scoped>
.page-container {
  background-color: #000;
  color: #fff;
  padding: 20px;
}

h1, h2 {
  color: #fff;
}

.book-content {
  margin-top: 20px;
}
</style>
