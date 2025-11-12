<template>
  <div class="main-container">
    <iframe style="height: 100vh;" src="http://192.168.1.72:81/" width="100%" height="100%" frameborder="0"
      allowfullscreen></iframe>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  alert("重定向到了 http://192.168.1.72:81/")
});
</script>

<style scoped>
.helmain-containerlo {
  margin: auto 0;
}
</style>
