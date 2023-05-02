<template>
  <div class="home">
    <nav-home />
    <router-view />
  </div>
</template>

<script>
import NavHome from "@/components/NavHome";
export default {
  name: "HomePage",
  components: {NavHome},
  methods: {
  }
}
</script>

<style scoped>
.home {
  display: flex;
}
</style>
