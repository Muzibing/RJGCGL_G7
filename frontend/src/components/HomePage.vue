<template>
  <div class="home-page">
    <!-- 头部区域：整合标题和登录状态 -->
    <header class="header">
      <div class="header-content">
        <div class="title-section">
          <h1>AI辅助就医问诊引擎</h1>
          <p class="subtitle">智能医疗助手，为您的健康保驾护航</p>
        </div>
        <div class="auth-section">
          <div v-if="isLoggedIn">
            <span>欢迎，{{ username }}</span>
            <button @click="logout">退出</button>
          </div>
          <div v-else>
            <span>未登录</span>
            <button @click="navigateToLogin">登录</button>
            <button @click="navigateToRegister">注册</button>
          </div>
        </div>
      </div>
    </header>

    <!-- 健康信息输入窗 -->
    <HealthInfo v-if="isLoggedIn" />

    <!-- 聊天窗口 -->
    <div class="chat-container">
      <div class="messages-container">
        <div
          v-for="(message, index) in internalMessages"
          :key="index"
          :class="['chat-message', message.sender]"
        >
          <img :src="message.avatar" class="avatar" />
          <div class="message-content">{{ message.text }}</div>
        </div>
      </div>
      <div class="input-container">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="请输入您的问题..."
        />
        <button @click="sendMessage">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
// 引入自定义的 axios 实例
import axios from "../axios"; // 确保正确的路径，axios 实例位于 src/axios.js
import { inject } from "vue";
import HealthInfo from "./HealthInfo.vue"; // 引入健康信息组件

export default {
  props: ["messages"],
  components: {
    HealthInfo,
  },
  setup() {
    const isLoggedIn = inject("isLoggedIn", false);
    const username = inject("username", "");
    const setLogin = inject("setLogin");

    const navigateToLogin = () => {
      window.location.href = "/login";
    };

    const navigateToRegister = () => {
      window.location.href = "/register";
    };

    const logout = () => {
      setLogin(false, "");
      window.location.reload();
    };

    return {
      isLoggedIn,
      username,
      navigateToLogin,
      navigateToRegister,
      logout,
    };
  },
  data() {
    return {
      internalMessages: [],
      userInput: "",
    };
  },
  watch: {
    messages: {
      immediate: true,
      handler(newMessages) {
        this.internalMessages = [...newMessages];
      },
    },
  },
  methods: {
    // 修改 sendMessage 方法
    async sendMessage() {
      if (this.userInput.trim()) {
        // 创建用户消息
        const userMessage = {
          text: this.userInput,
          sender: "user",
          avatar: "../patient.jpg",
        };
        this.internalMessages.push(userMessage);
        this.userInput = "";

        // 调用后端 API
        try {
          const response = await axios.post("/deepseek/chat/", {
            message: userMessage.text,
            history: this.internalMessages.slice(0, -1), // 发送除了最新消息之外的所有历史记录
          });

          // 获取后端返回的消息，并生成 botMessage
          const botMessage = {
            text: response.data.reply,
            sender: "bot",
            avatar: "../doctor.png",
          };

          this.internalMessages.push(botMessage);
          this.$emit("update-messages", this.internalMessages); // 更新父组件中的消息
        } catch (error) {
          console.error("Error sending message to backend:", error);
          const errorMessage = {
            text: "服务器发生错误，请稍后再试。",
            sender: "bot",
            avatar: "../doctor.png",
          };
          this.internalMessages.push(errorMessage);
        }
      }
    },
  },
};
</script>

<style>
.home-page {
  flex: 1;
  padding: 2em;
  font-family: Arial, sans-serif;
}

.header {
  margin-bottom: 2em;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  padding: 1em 2em;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title-section {
  text-align: left;
}

.title-section h1 {
  color: #2c3e50;
  font-size: 1.8em;
  margin: 0;
}

.title-section .subtitle {
  color: #666;
  font-size: 0.9em;
  margin: 0.3em 0 0 0;
}

.auth-section {
  display: flex;
  align-items: center;
}

.auth-section span {
  margin-right: 1em;
}

.auth-section button {
  padding: 0.5em 1em;
  font-size: 1em;
  border: none;
  background-color: #3f51b5;
  color: white;
  cursor: pointer;
  border-radius: 4px;
  margin-left: 10px;
}

.chat-container {
  height: calc(100vh - 180px);
  margin-top: 1em;
  margin-bottom: 1em;
  border: 1px solid #ddd;
  padding: 1em;
  overflow-y: auto;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
}

.chat-message {
  display: flex;
  margin-bottom: 1em;
  align-items: flex-end;
}

.chat-message.user {
  flex-direction: row-reverse;
  text-align: right;
}

.avatar {
  margin: 0 1em;
  width: 40px;
  height: 40px;
}

.message-content {
  padding: 1em 1.5em;
  border-radius: 15px;
  background-color: #3f51b5;
  color: white;
  font-size: 0.95em;
}

.input-container {
  display: flex;
  max-width: 100%;
  margin: 1em 0 0 0;
  background-color: white;
  padding: 0.8em;
  border-top: 1px solid #ddd;
}

.input-container input {
  flex: 1;
  padding: 0.5em;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  background-color: transparent;
}

.input-container button {
  padding: 0.5em 1em;
  border: none;
  background-color: #3f51b5;
  color: white;
  cursor: pointer;
  border-radius: 0 4px 4px 0;
}
</style>