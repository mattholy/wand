<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import PageInitVue from './views/PageInit.vue';

const showRouterView = ref(false);

onMounted(async () => {
  try {
    const apiBaseUrl = import.meta.env.VITE_API_URL;
    const response = await axios.get(`${apiBaseUrl}/init`);
    if (response.data.new_wand == false) {
      showRouterView.value = true
    }
  } catch (error) {
    console.error(error)
  }
});
</script>

<template>
  <n-message-provider>
    <RouterView v-if="showRouterView" />
    <PageInitVue v-else />
  </n-message-provider>
</template>

<style scoped></style>