<template>
    <n-flex justify="center" class="full_height">
        <n-flex vertical justify="center" class="full_height">
            <n-form style="width: 1000px">
                <n-card :title="$t('ui.init.main_card.title')" :segmented="{
                    content: true,
                    footer: 'soft'
                }" size="huge">
                    <n-grid x-gap="12" :cols="2">
                        <n-gi><n-space vertical>
                                <n-form-item :label="$t('ui.init.main_card.item.name.title')" required>
                                    <n-input type="text" :placeholder="$t('ui.init.main_card.item.name.palceholder')" />
                                </n-form-item>
                                <n-form-item :label="$t('ui.init.main_card.item.desc.title')" required>
                                    <n-input type="text" :placeholder="$t('ui.init.main_card.item.desc.palceholder')" />
                                </n-form-item>
                                <n-form-item :label="$t('ui.init.main_card.item.icon.title')">
                                    <n-input type="text" :placeholder="$t('ui.init.main_card.item.icon.palceholder')" />
                                </n-form-item>
                                <n-form-item :label="$t('ui.init.main_card.item.image.title')">
                                    <n-input type="text" :placeholder="$t('ui.init.main_card.item.image.palceholder')" />
                                </n-form-item>
                            </n-space>
                        </n-gi>
                        <n-gi>
                            <n-space vertical>
                                <n-form-item :label="$t('ui.init.main_card.item.gpg.title')" required>
                                    <n-input type="textarea" :placeholder="$t('ui.init.main_card.item.gpg.palceholder')"
                                        :autosize="{
                                            minRows: 17,
                                            maxRows: 17
                                        }" />
                                </n-form-item>
                            </n-space>
                        </n-gi>
                    </n-grid>
                    <template #footer>
                        #footer
                    </template>
                    <template #action>
                        <n-flex justify="space-around">
                            <n-button type="primary" round>
                                {{ $t('ui.init.main_card.bnt_submit') }}
                            </n-button>
                        </n-flex>
                    </template>
                </n-card>
            </n-form>
        </n-flex>
    </n-flex>
</template>
  
<script>
export default {
    name: 'PageInitVue'
}
</script>
  
<style>
.full_height {
    height: 100%;
    /* width: 200px; */
}
</style>
  