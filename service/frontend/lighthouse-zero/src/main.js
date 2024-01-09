import './assets/css/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import router from './router'

import enUS from '../i18n/enUS.json'
import zhCN from '../i18n/zhCN.json'

const app = createApp(App)
const i18n = createI18n({
    locale: 'zhCN',
    messages: {
        zhCN,
        enUS
    }
})

app.use(createPinia())
app.use(router)

app.use(i18n)
app.mount('#app')
