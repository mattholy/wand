<script setup>
import { ref } from 'vue';
import { useMessage } from "naive-ui";
import { useI18n } from 'vue-i18n';

const { t } = useI18n();


const init_table = ref({
    service_name: '',
    service_desc: '',
    service_icon: '',
    service_image: '',
    admin_gpg_public_key: ''

});
const agree = ref(false);
const message = useMessage();
const rules = {
    service_name: {
        required: true,
        message: t('ui.init.main_card.item.name.err'),
        trigger: "blur"
    },
    service_desc: {
        required: true,
        message: t('ui.init.main_card.item.desc.err'),
        trigger: "blur"
    },
    service_icon: {
        required: true,
        message: t('ui.init.main_card.item.icon.err'),
        trigger: "blur"
    },
    service_image: {
        required: true,
        message: t('ui.init.main_card.item.image.err'),
        trigger: "blur"
    },
    agreements: {
        required: true,
        message: t('ui.init.main_card.item.agree.err'),
        trigger: "blur"
    },
    gpg: {
        required: true,
        message: t('ui.init.main_card.item.gpg.err'),
        trigger: "blur"
    }
}

function handleClick() {
    message.info("Button Clicked");
};

</script>

<template>
    <n-flex justify="center" class="full_height">
        <n-flex vertical justify="center" class="full_height">
            <n-form :rules="rules">
                <n-card :title="$t('ui.init.main_card.title')" :segmented="{
                    content: true,
                    footer: 'soft'
                }" size="huge">
                    <n-flex>
                        <n-flex vertical justify="space-between" style="width: 300px">
                            <n-form-item path="service_name" :label="$t('ui.init.main_card.item.name.title')" required>
                                <n-input v-model:value="init_table.service_name" type="text"
                                    :placeholder="$t('ui.init.main_card.item.name.palceholder')" />
                            </n-form-item>
                            <n-form-item path="service_desc" :label="$t('ui.init.main_card.item.desc.title')" required>
                                <n-input v-model:value="init_table.service_desc" type="text"
                                    :placeholder="$t('ui.init.main_card.item.desc.palceholder')" />
                            </n-form-item>
                            <n-form-item path="service_icon" :label="$t('ui.init.main_card.item.icon.title')">
                                <n-input v-model:value="init_table.service_icon" type="text"
                                    :placeholder="$t('ui.init.main_card.item.icon.palceholder')" />
                            </n-form-item>
                            <n-form-item path="service_image" :label="$t('ui.init.main_card.item.image.title')">
                                <n-input v-model:value="init_table.service_image" type="text"
                                    :placeholder="$t('ui.init.main_card.item.image.palceholder')" />
                            </n-form-item>
                            <n-form-item path="agreements" :label="$t('ui.init.main_card.item.agree.title')" required>
                                <n-checkbox v-model:checked="agree" />
                                <span class="item_span">{{ $t('ui.init.main_card.item.agree.desc') }}</span>
                            </n-form-item>
                        </n-flex>
                        <n-flex vertical style="width: 600px">
                            <n-form-item path="gpg" :label="$t('ui.init.main_card.item.gpg.title')" required>
                                <n-input v-model:value="init_table.admin_gpg_public_key" type="textarea"
                                    :placeholder="$t('ui.init.main_card.item.gpg.palceholder')" :autosize="{
                                        minRows: 17,
                                        maxRows: 17
                                    }" />
                            </n-form-item>
                        </n-flex>
                    </n-flex>
                    <template #action>
                        <n-flex justify="space-around">
                            <n-button type="primary" round :disabled="!agree" @click="handleClick">
                                {{ $t('ui.init.main_card.bnt_submit') }}
                            </n-button>
                        </n-flex>
                    </template>
                </n-card>
            </n-form>
        </n-flex>
    </n-flex>
</template>
  

  
<style scoped>
.full_height {
    height: 100%;
}

.item_span {
    padding: 0px 10px;
}
</style>
  