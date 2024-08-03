<template>
    <div>
      <button @click="triggerExport" class="export-button">Export E-book Access Details</button>
      <p v-if="responseMessage">{{ responseMessage }}</p>
      <a v-if="downloadLink" :href="downloadLink" download>Download CSV</a>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        responseMessage: '',
        downloadLink: ''
      };
    },
    methods: {
      triggerExport() {
        fetch('http://localhost:5000/api/trigger_export', {
          method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
          this.responseMessage = data.message;
          if (data.file) {
            this.downloadLink = data.file;
          }
        })
        .catch(error => {
          this.responseMessage = 'Error: ' + error;
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .export-button {
    background-color: #000; /* Black background */
    border: 1px solid #fff; /* White border */
    color: #fff; /* White text */
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 10px 2px;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .export-button:hover {
    background-color: #333; /* Darker black background */
    color: #fff; /* White text */
  }
  
  p, a {
    color: #fff; /* White text for the response message and download link */
  }
  </style>
  