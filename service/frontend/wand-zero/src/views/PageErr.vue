<template>
    <n-result status="500" :title="$t('ui.err.title')" :description="$t('ui.err.desc')" style="padding: 200px;">
        <template #footer>
            <n-gradient-text type="info">
                {{ $t('ui.err.info') }}
            </n-gradient-text>
        </template>
    </n-result>
</template>

<script setup>
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<style></style>