<template>
    <div class="star-rating">
      <span
        v-for="star in 5"
        :key="star"
        class="star"
        :class="{ filled: star <= rating }"
        @click="setRating(star)"
      >
        ★
      </span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'StarRating',
    props: {
      rating: {
        type: Number,
        default: 0
      }
    },
    methods: {
      setRating(star) {
        this.$emit('update:rating', star);
      }
    }
  };
  </script>
  
  <style scoped>
  .star-rating {
    display: flex;
    flex-direction: row;
  }
  
  .star {
    font-size: 2em;
    color: grey;
    cursor: pointer;
  }
  
  .star.filled {
    color: gold;
  }
  </style>
  