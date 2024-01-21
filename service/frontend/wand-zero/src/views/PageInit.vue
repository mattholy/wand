

<template>
    <div class="full_height background_color">
        <n-flex justify="center" class="full_height">
            <n-flex vertical justify="center" class="full_height">
                <n-form :rules="rules" ref="form_init" :model="init_table" :disabled="loading_submit">
                    <n-card :title="$t('ui.init.main_card.title')" :segmented="{
                        content: true,
                        footer: 'soft'
                    }" size="huge">
                        <n-scrollbar style="max-height: 550px">
                            <n-flex vertical>
                                <n-grid cols="2" x-gap="12">
                                    <n-gi>
                                        <n-form-item path="service_name" :label="$t('ui.init.main_card.item.name.title')"
                                            required>
                                            <n-input v-model:value="init_table.service_name" type="text"
                                                :placeholder="$t('ui.init.main_card.item.name.palceholder')" />
                                        </n-form-item>
                                    </n-gi>
                                    <n-gi>
                                        <n-form-item path="service_desc" :label="$t('ui.init.main_card.item.desc.title')"
                                            required>
                                            <n-input v-model:value="init_table.service_desc" type="text"
                                                :placeholder="$t('ui.init.main_card.item.desc.palceholder')" />
                                        </n-form-item>
                                    </n-gi>
                                </n-grid>
                                <n-form-item path="admin_gpg_public_key"
                                    :label="$t('ui.init.main_card.item.admin_gpg_public_key.title')" required>
                                    <n-input v-model:value="init_table.admin_gpg_public_key" type="textarea"
                                        :placeholder="$t('ui.init.main_card.item.admin_gpg_public_key.palceholder')"
                                        :autosize="{
                                            minRows: 17,
                                            maxRows: 17
                                        }" style="width: 600px;" />
                                </n-form-item>
                            </n-flex>
                        </n-scrollbar>
                        <template #footer>
                            <n-form-item path="agreements" :label="$t('ui.init.main_card.item.agreements.title')" required>
                                <n-checkbox v-model:checked="init_table.agreements" />
                                <span class="item_span">{{ $t('ui.init.main_card.item.agreements.desc') }}</span>
                            </n-form-item>
                        </template>
                        <template #action>
                            <n-flex justify="space-around">
                                <n-button type="primary" round :disabled="!init_table.agreements" @click="submit"
                                    :loading="loading_submit">
                                    {{ $t('ui.init.main_card.bnt_submit') }}
                                </n-button>
                            </n-flex>
                        </template>
                    </n-card>
                </n-form>
            </n-flex>
        </n-flex>
    </div>
</template>
  
<script setup>
import { ref } from 'vue';
import { useMessage } from "naive-ui";
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';


const { t } = useI18n();
const form_init = ref(null);
const loading_submit = ref(false);
const init_table = ref({
    service_name: '',
    service_desc: '',
    admin_gpg_public_key: '',
    agreements: false

});

const router = useRouter();
const apiBaseUrl = import.meta.env.VITE_API_URL;
const message = useMessage();
const rules = {
    service_name: [{
        required: true,
        message: t('ui.init.main_card.item.name.err'),
        trigger: "blur"
    }],
    service_desc: [{
        required: true,
        message: t('ui.init.main_card.item.desc.err'),
        trigger: "blur"
    }],
    agreements: [{
        validator: i_am_agree,
        message: t('ui.init.main_card.item.agreements.err'),
        trigger: "blur"
    }],
    admin_gpg_public_key: [{
        validator: validate_name,
        message: t('ui.init.main_card.item.admin_gpg_public_key.err'),
        trigger: "blur"
    }]
}

function validate_name(rule, value) {
    if (value.startsWith("-----BEGIN PGP PUBLIC KEY BLOCK-----") && value.endsWith("-----END PGP PUBLIC KEY BLOCK-----")) {
        return true;
    } else {
        return false;
    }
};

function i_am_agree(rule, value) {
    return value;
}

function submit(e) {
    e.preventDefault()
    form_init.value?.validate()
        .then(() => {
            loading_submit.value = true
            message.loading(t('message.init.submit.can_submit'))
            fetch(
                `${apiBaseUrl}/init`,
                {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(init_table.value)
                }
            )
                .then((res) => {
                    if (res.status >= 400 && res.status < 500) {
                        return res.json().then(body => {
                            if (body.detail == 'can_not_init_again') {
                                setTimeout(() => {
                                    router.push('/')
                                }, 1000)
                            }
                            throw new Error(body.detail);
                        });
                    } else if (res.status >= 500 && res.status < 600) {
                        throw new Error('server_error');
                    } else {
                        return res.json()
                    }
                })
                .then((data) => {
                    message.success(t('message.init.server.' + data.wand_msg));
                    loading_submit.value = false;
                    setTimeout(() => {
                        router.push('/')
                    }, 1000)
                })
                .catch((e) => {
                    loading_submit.value = false;
                    message.error(t('message.init.server.' + e.message));
                })
        })
        .catch(() => {
            message.error(t('message.init.submit.can_not_submit'))
        });

};

</script>
  
<style scoped>
.full_height {
    height: 100%;
}

.item_span {
    padding: 0px 10px;
}

.background_color {
    background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
}
</style>
  