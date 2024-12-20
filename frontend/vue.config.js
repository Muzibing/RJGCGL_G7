const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '':{
        target: 'http://127.0.0.1:8000', // Django 后端的地址
        changeOrigin: true,
        pathRewrite: { '^': '' }, // 保持路径一致
      },
      // Vue 项目的所有 API 请求都会转发到 Django 后端
      '/api': {
        target: 'http://127.0.0.1:8000', // Django 后端的地址
        changeOrigin: true,
        pathRewrite: { '^/api': '/api' }, // 保持路径一致
      },
      '/deepseek': {
        target: 'http://127.0.0.1:8000', // Django 后端的地址
        changeOrigin: true,
        pathRewrite: { '^/deepseek': '/deepseek' }, // 保持路径一致
      },
    },
  },
});
