<template>
  <div class="dashboard">
    <div class="chart-container">
      <apexchart v-if="bookSecSeries[0].data.length" type="bar" :options="bookSecOptions" :series="bookSecSeries"></apexchart>
      <p v-else>No data available for books by section</p>
    </div>
    <div class="chart-container">
      <apexchart v-if="topUserSeries[0].data.length" type="bar" :options="topUserOptions" :series="topUserSeries"></apexchart>
      <p v-else>No data available for user activity</p>
    </div>
    <div class="chart-container">
      <apexchart v-if="popularBooksSeries[0].data.length" type="donut" :options="popularBooksOptions" :series="popularBooksSeries"></apexchart>
      <p v-else>No popular books</p>
    </div>
    <div class="chart-container">
      <apexchart v-if="issuesReturnsSeries[0].data.length || issuesReturnsSeries[1].data.length" type="line" :options="issuesReturnsOptions" :series="issuesReturnsSeries"></apexchart>
      <p v-else>No data available for book issues and returns</p>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

export default {
  components: {
    apexchart: VueApexCharts
  },
  setup() {
    const bookSecSeries = ref([{ name: 'Books', data: [] }]);
    const topUserSeries = ref([{ name: 'Activity Count', data: [] }]);
    const popularBooksSeries = ref([{ name: 'Ratings', data: [] }]);
    const issuesReturnsSeries = ref([{ name: 'Issues', data: [] }, { name: 'Returns', data: [] }]);

    const bookSecOptions = reactive({
      chart: { type: 'bar', background: '#000' },
      title: { text: 'Number of Books by Section', style: { color: '#fff' } },
      xaxis: { categories: [], labels: { style: { colors: '#fff' } } },
      yaxis: { labels: { style: { colors: '#fff' } } },
      tooltip: {
        theme: 'dark'
      }
    });

    const topUserOptions = reactive({
      chart: { type: 'bar', background: '#000' },
      title: { text: 'User Activity', style: { color: '#fff' } },
      xaxis: { categories: [], labels: { style: { colors: '#fff' } } },
      yaxis: { labels: { style: { colors: '#fff' } } },
      tooltip: {
        theme: 'dark'
      }
    });

    const popularBooksOptions = reactive({
      chart: { type: 'donut', background: '#000' },
      title: { text: 'Most Popular Books', style: { color: '#fff' } },
      labels: [],
      tooltip: {
        theme: 'dark'
      }
    });

    const issuesReturnsOptions = reactive({
      chart: { type: 'line', background: '#000' },
      title: { text: 'Book Issues and Returns Over Time', style: { color: '#fff' } },
      xaxis: { categories: [], labels: { style: { colors: '#fff' } } },
      yaxis: { labels: { style: { colors: '#fff' } } },
      tooltip: {
        theme: 'dark'
      }
    });

    const isDataLoaded = ref(false);
    const topUserLoaded = ref(false);
    const popularBooksLoaded = ref(false);
    const issuesReturnsLoaded = ref(false);

    const fetchData = async () => {
      try {
        // Fetch Number of Books by Section
        const bookSecRes = await fetch('http://localhost:5000/api/no_of_book_sec');
        const bookSecData = await bookSecRes.json();
        bookSecOptions.xaxis.categories = Object.keys(bookSecData).filter(key => key);
        bookSecSeries.value[0].data = Object.values(bookSecData).filter(value => value !== null);

        // Fetch User Activity
        const topUserRes = await fetch('http://localhost:5000/api/user_activity');
        const topUserData = await topUserRes.json();
        console.log('User Activity Data:', topUserData);
        if (topUserData.message) {
          topUserOptions.title.text = topUserData.message;
          topUserOptions.xaxis.categories = ["No Data"];
          topUserSeries.value[0].data = [1];
        } else {
          topUserOptions.xaxis.categories = Object.keys(topUserData);
          topUserSeries.value[0].data = Object.values(topUserData);
        }

        // Fetch Most Popular Books
        const popularBooksRes = await fetch('http://localhost:5000/api/popular_books');
        const popularBooksData = await popularBooksRes.json();
        if (popularBooksData.message) {
          popularBooksOptions.title.text = popularBooksData.message;
          popularBooksOptions.labels = ["No Data"];
          popularBooksSeries.value[0].data = [1];
        } else {
          popularBooksOptions.labels = popularBooksData.map(book => book.book_name);
          popularBooksSeries.value[0].data = popularBooksData.map(book => book.avg_rating);
        }

        // Fetch Book Issues and Returns Over Time
        const issuesReturnsRes = await fetch('http://localhost:5000/api/book_issues_returns');
        const issuesReturnsData = await issuesReturnsRes.json();
        if (issuesReturnsData.message) {
          issuesReturnsOptions.title.text = issuesReturnsData.message;
        } else {
          issuesReturnsOptions.xaxis.categories = Array.from(new Set([
            ...Object.keys(issuesReturnsData.issues),
            ...Object.keys(issuesReturnsData.returns)
          ])).sort();
          issuesReturnsSeries.value[0].data = issuesReturnsOptions.xaxis.categories.map(date => issuesReturnsData.issues[date] || 0);
          issuesReturnsSeries.value[1].data = issuesReturnsOptions.xaxis.categories.map(date => issuesReturnsData.returns[date] || 0);
        }

        isDataLoaded.value = true;
        topUserLoaded.value = true;
        popularBooksLoaded.value = true;
        issuesReturnsLoaded.value = true;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    onMounted(fetchData);

    return {
      bookSecSeries,
      bookSecOptions,
      topUserSeries,
      topUserOptions,
      popularBooksSeries,
      popularBooksOptions,
      issuesReturnsSeries,
      issuesReturnsOptions,
      isDataLoaded,
      topUserLoaded,
      popularBooksLoaded,
      issuesReturnsLoaded
    };
  }
};
</script>

<style scoped>
.dashboard {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-container {
  background-color: #000;
  color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  min-height: 300px;  /* Adjust this value as needed to make the charts smaller */
}
</style>
