<template>
    <h1>HOME</h1>
    <form class="d-flex mx-auto" @submit.prevent="searchProducts" >
        <input v-model="searchQuery" class="form-control me-3 shadow-lg border-black" type="search" placeholder="Search" aria-label="Search">
         <button class="btn btn-outline-success" type="submit">
           <i class="bi bi-search"></i> Search
         </button>
        </form>
    <div>
   
      
      <b><router-link to="/lib-dashboard/Create-Section">Create section</router-link></b>
      <ul class="list-group">
        <!-- Iterate through sections -->
        <li v-for="section in section_item" :key="section.id" class="list-group-item">
          <strong>{{ section.name }}</strong>
          <router-link :to="{ name: 'lib-edit-section', params: { id: section.id } }">Edit section</router-link>
        <button type="submit" @click="confirmDelete(section.id)" class="btn btn-primary">Delete</button>
        <router-link :to="{ name: 'lib-add-book', params: { sectionId: section.id } }">Add Book</router-link>
          <ul>
            <!-- Iterate through books for the current section -->
            <li v-for="book in book_item" :key="book.id" class="list-group-item"  >
                <div v-if="section.id === book.section_id && book.name">{{ book.name }} - {{ book.author }} 
                
               <div v-for="sec in secondary_sec" :key="sec.id">
                <div v-if="sec.book_id === book.id">{{ sec.section_name }}
            
                </div>
                
               </div>
                <router-link :to="{ name: 'lib-edit-book', params: { bookId: book.id,sectionId:book.section_id} }">edit Book</router-link>
                <router-link :to="{ name: 'lib-add-secondary-section', params: { bookId: book.id,sectionId:book.section_id} }">add secondary  section</router-link>
                <router-link :to="{ name: 'lib-del-secondary-section', params: { bookId: book.id,sectionId:book.section_id} }">del secondary  section</router-link>
                <button type="submit" @click="confirmDeleteBook(book.id)" class="btn btn-primary">Delete Book</button>
              </div>
            </li>
          </ul>
        </li>
      </ul>
      <router-view @section-updated="handleSectionUpdated" @book-added="handleSectionUpdated" @sec-created="handleSectionUpdated" @book-updated="handleSectionUpdated"></router-view>
    </div>
  </template>
    
  <script>
  export default{
      name:"SectionName",
      data(){
          return{
              section_item : [],
              book_item:[],
              secondary_sec:[],
              searchQuery:''
  
          }
      },
      mounted() {
  
      this.get_all_section();
      this.get_all_books();
      this.get_all_secondary_sec();
      console.log(this.secondary_sec)
      
  },
      methods:{
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
        console.log(this.book_item)
        console.log(this.section_item)
      } else {
        console.error('Failed to fetch products');
      }
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  },
        async get_all_secondary_sec(){
          try{
                  const response = await fetch("http://localhost:5000/api/secondarysection", {
            method: "GET",
            headers: {
        
              'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
            }
          
          });
  
          const data = await response.json();
          if (response.status === 200) {
            this.secondary_sec=data
            console.log(this.secondary_sec)
            
          }else if (response.status === 401 || response.status ===403){
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
  
        } else {
            console.log("Something went wrong");
          }
  
              }
              catch(err){
                  console.log("error")
  
              }
          
  
        },
          async get_all_section(){
              try{
                  const response = await fetch("http://localhost:5000/api/sections", {
            method: "GET",
            headers: {
        
              'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
            }
          
          });
  
          const data = await response.json();
          if (response.status === 200) {
            this.section_item=data
            
            console.log(this.section_item)
          }else if (response.status === 401 || response.status ===403){
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
  
        } else {
            console.log("Something went wrong");
          }
  
              }
              catch(err){
                  console.log("error")
  
              }
          },
  
          async get_all_books(){
              try{
                  const response = await fetch("http://localhost:5000/api/books", {
            method: "GET",
            headers: {
  
              'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
            }
          
          });
  
          const data = await response.json();
          if (response.status === 200) {
            this.book_item=data
            
          }else if (response.status === 401 || response.status ===403){
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
  
        } else {
            console.log("Something went wrong");
          }
  
              }
              catch(err){
                  console.log("error")
  
              }
          },
          async del_section(id){
          
              try{
                  const response = await fetch (`http://localhost:5000/api/sections/${id}`, {
            method: "DELETE",
            headers: {
                'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
              }
          
          })
          const message = await response.json();
          console.log(message)
          if (response.status === 200) {
            alert("section deleted successfully")
            this.get_all_section()
            this.get_all_books()
            
          }
          else if (response.status === 401 || response.status ===403){
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
  
        } else {
            console.log("Something went wrong");
          }
  
              }
              catch(err){
                  console.log("error")
  
              }
          },
          confirmDelete(id) {
        if (window.confirm("Are you sure you want to delete this section?")) {
          this.del_section(id);
        }
      },
      handleSectionUpdated() {
        this.get_all_section();
        this.get_all_books() // Refresh the list of sections when an update event is received
      },
      confirmDeleteBook(id){
        if (window.confirm("Are you sure you want to delete this book?")) {
          this.del_book(id);
        }
  
      },
      async del_book(id){
        try{
                  const response = await fetch (`http://localhost:5000/api/books/${id}`, {
            method: "DELETE",
            headers: {
               
                'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
              }
           
          
          })
          const message = await response.json();
          console.log(message)
          if (response.status === 200) {
            alert("book deleted successfully")
            this.get_all_section()
            this.get_all_books()
            
          }
          else if (response.status === 401 || response.status ===403){
          alert('UNAUTHORIZED TO ACCESS THIS SECTION.');
          this.$router.push('/login');
  
        } else {
            console.log("Something went wrong");
          }
  
              }
              catch(err){
                  console.log("error")
  
              }
  
      }
      }
  
  
  }
  </script>
  <style>
  
  </style>
  
  