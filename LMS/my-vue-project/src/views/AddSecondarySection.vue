<template>
  <div class="page-container">
    <h2>Add Secondary Section</h2>
    <form @submit.prevent="addSecondarySection" class="form-container">
      <div class="form-floating mb-3">
        <label for="sectionName">Section Name</label>
        <select v-model="selectedSectionId" id="sectionName" class="form-control" required>
          <option v-for="section in availableSections" :key="section.id" :value="section.id">
            {{ section.name }}
          </option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary mt-3">Add Secondary Section</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AddSecondarySection',
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
      sections: [],
      secondarySectionIds: [],
      selectedSectionId: '',
      availableSections: []
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
    await this.fetchSections();
    await this.fetchSecondarySections();
    this.filterAvailableSections();
  },
  methods: {
    async fetchSections() {
      try {
        const response = await fetch("http://localhost:5000/api/sections", {
          method: "GET",
          headers: {
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          }
        });

        const data = await response.json();
        if (response.status === 200) {
          this.sections = data;
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
        // Filter secondary sections to get only those related to the current book
        this.secondarySectionIds = data
          .filter(sec => sec.book_id === this.numericBookId)
          .map(sec => sec.section_id);
      } catch (error) {
        console.error('Error fetching secondary sections:', error);
      }
    },
    filterAvailableSections() {
      this.availableSections = this.sections.filter(
        section => section.id !== this.numericSectionId && !this.secondarySectionIds.includes(section.id)
      );
    },
    async addSecondarySection() {
      try {
        const response = await fetch('http://localhost:5000/api/secondarysection', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
          body: JSON.stringify({
            book_id: this.numericBookId,
            section_id: this.selectedSectionId,
            section_name: this.sections.find(section => section.id === this.selectedSectionId).name
          })
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error adding secondary section: ${errorText}`);
        }

        const data = await response.json();
        if (response.status === 200) {
          alert('Secondary section added successfully');
          this.$router.push('/lib-dashboard');
        } else {
          alert(data);
        }
      } catch (error) {
        console.error('Error adding secondary section:', error);
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
