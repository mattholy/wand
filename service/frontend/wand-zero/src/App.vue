<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import PageInitVue from './views/PageInit.vue';

const showRouterView = ref(false);

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8080/init')
    if (response.data.new_wand == false) {
      showRouterView.value = true
    }
    console.log(response.data.new_wand)
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