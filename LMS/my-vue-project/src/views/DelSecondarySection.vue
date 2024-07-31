<template>
  <div class="page-container">
    <h2>Delete Secondary Section</h2>
    <form @submit.prevent="deleteSecondarySection" class="form-container">
      <div class="form-floating mb-3">
        <label for="secondarySection"> Section Name</label>
        <select v-model="selectedSecondarySectionId" id="secondarySection" class="form-control" required>
          <option v-for="section in secondarySections" :key="section.section_id" :value="section.section_id">
            {{ section.section_name }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-danger mt-3">Delete Secondary Section</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'DeleteSecondarySection',
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
      secondarySections: [],
      selectedSecondarySectionId: ''
    };
  },
  computed: {
    numericBookId() {
      return parseInt(this.bookId);
    },
    numericSectionId() {
      return parseInt(this.sectionId);
    }
  },
  async mounted() {
    await this.fetchSecondarySections();
    console.log('Fetched secondary sections:', this.secondarySections);
  },
  methods: {
    async fetchSecondarySections() {
      try {
        const response = await fetch('http://localhost:5000/api/secondarysection', {
          method: 'GET',
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error fetching secondary sections: ${errorText}`);
        }
        const data = await response.json();
        // Log the data fetched from the API
        console.log('API response data:', data);
        // Filter secondary sections to get only those related to the current book
        this.secondarySections = data.filter(sec => sec.book_id === this.numericBookId);
      } catch (error) {
        console.error('Error fetching secondary sections:', error);
      }
    },
    async deleteSecondarySection() {
      try {
        const response = await fetch('http://localhost:5000/api/secondarysection', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
          body: JSON.stringify({
            book_id: this.numericBookId,
            section_id: this.selectedSecondarySectionId
          })
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error deleting secondary section: ${errorText}`);
        }

        const data = await response.json();
        if (response.status === 200) {
          alert('Secondary section deleted successfully');
          this.$router.push('/lib-dashboard');
        } else {
          alert(data);
        }
      } catch (error) {
        console.error('Error deleting secondary section:', error);
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

h2 {
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

.btn-danger {
  background-color: #dc3545; /* Bootstrap danger color */
  border: none;
  color: #fff; /* White text */
}

.btn-danger:hover {
  background-color: #c82333; /* Darker red on hover */
  color: #fff; /* White text */
}

.mt-3 {
  margin-top: 20px;
}
</style>
