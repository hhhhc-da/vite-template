import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router.js'

// 创建 App 并使用路由
createApp(App)
  .use(router)
  .mount('#app')