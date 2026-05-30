import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVfm } from 'vue-final-modal'
import './style.css'
import App  from './App.vue'
const app = createApp(App)
const pinia = createPinia()
app.use(createVfm())  
app.use(pinia)
createApp(App).mount('#app').$nextTick(() => {
  window.ipcRenderer.on('main-process-message', (_event, message) => {
    console.log(message)
  })
})
