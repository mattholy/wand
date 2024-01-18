<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

import PageErr from './views/PageErr.vue';

const router = useRouter();
const showRouterView = ref(false);

onMounted(async () => {
  try {
    const apiBaseUrl = import.meta.env.VITE_API_URL;
    const response = await axios.get(`${apiBaseUrl}/init`);
    showRouterView.value = true;
    if (response.data.new_wand == true) {
      router.push('/init')
    }
  } catch (error) {
    if (error.code == "ERR_NETWORK") {
      showRouterView.value = false
    }
  }
});
</script>

<template>
  <n-message-provider>
    <RouterView v-if="showRouterView" />
    <PageErr v-else />
  </n-message-provider>
</template>

<style scoped></style>