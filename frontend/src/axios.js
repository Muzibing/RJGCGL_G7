// src/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',  // Django 后端地址
  timeout: 30000,  // 请求超时设置（可选）
});

export default instance;
