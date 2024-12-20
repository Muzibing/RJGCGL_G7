// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 确保导入 router

const app = createApp(App);
app.use(router); // 使用 router
app.mount('#app');
