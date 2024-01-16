import './assets/css/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import naive from "naive-ui"

import App from './App.vue'
import router from './router'

import enUS from '../i18n/en-US.json'
import zhCN from '../i18n/zh-CN.json'

const browserLanguage = navigator.language.replace('-','')

const app = createApp(App)
const i18n = createI18n({
    locale: browserLanguage,
    messages: {
        zhCN,
        enUS
    }
})

app.use(createPinia())
app.use(router)
app.use(naive)

app.use(i18n)
app.mount('#app')
