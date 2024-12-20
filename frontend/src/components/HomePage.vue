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
      <!-- 添加症状提示词切换按钮 -->
      <div class="symptoms-toggle">
        <button @click="toggleSymptomsPanel">
          {{ showSymptoms ? "隐藏症状选择" : "展开症状选择" }}
          <span :class="['toggle-icon', { rotated: showSymptoms }]">▼</span>
        </button>
      </div>

      <!-- 症状提示词部分 -->
      <div class="symptoms-tags" v-show="showSymptoms">
        <div
          class="symptoms-category"
          v-for="(category, index) in symptomCategories"
          :key="index"
        >
          <h4>{{ category.name }}</h4>
          <div class="tag-container">
            <span
              v-for="(symptom, sIndex) in category.symptoms"
              :key="sIndex"
              :class="[
                'symptom-tag',
                { active: selectedSymptoms.includes(symptom) },
              ]"
              @click="toggleSymptom(symptom)"
            >
              {{ symptom }}
            </span>
          </div>
        </div>
      </div>

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

      <!-- 输入框部分 -->
      <div class="input-container">
        <div class="selected-symptoms" v-if="selectedSymptoms.length > 0">
          已选症状：{{ selectedSymptoms.join("、") }}
        </div>
        <div class="input-row">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            :placeholder="inputPlaceholder"
          />
          <button @click="sendMessage">发送</button>
        </div>
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
      selectedSymptoms: [],
      showSymptoms: false, // 添加控制症状面板显示的状态
      symptomCategories: [
        {
          name: "常见症状",
          symptoms: [
            "发热",
            "咳嗽",
            "头痛",
            "乏力",
            "咽痛",
            "腹痛",
            "恶心",
            "呕吐",
          ],
        },
        {
          name: "疼痛类型",
          symptoms: ["刺痛", "钝痛", "持续性疼痛", "间歇性疼痛", "胀痛"],
        },
        {
          name: "其他症状",
          symptoms: ["食欲不振", "失眠", "头晕", "心悸", "胸闷", "气短"],
        },
      ],
    };
  },
  computed: {
    inputPlaceholder() {
      return this.selectedSymptoms.length > 0
        ? "您可以继续描述症状的具体情况..."
        : "请描述您的症状，或点击上方的症状标签...";
    },
  },
  methods: {
    toggleSymptom(symptom) {
      const index = this.selectedSymptoms.indexOf(symptom);
      if (index === -1) {
        this.selectedSymptoms.push(symptom);
      } else {
        this.selectedSymptoms.splice(index, 1);
      }
    },
    async sendMessage() {
      if (this.userInput.trim() || this.selectedSymptoms.length > 0) {
        // 构建消息文本
        let messageText = "";
        if (this.selectedSymptoms.length > 0) {
          messageText += `我的症状包括：${this.selectedSymptoms.join("、")}。`;
        }
        if (this.userInput.trim()) {
          messageText += this.userInput.trim();
        }

        // 创建用户消息
        const userMessage = {
          text: messageText,
          sender: "user",
          avatar: "../patient.jpg",
        };
        this.internalMessages.push(userMessage);
        this.userInput = "";
        this.selectedSymptoms = []; // 清空已选症状

        // 调用后端 API
        try {
          const response = await axios.post("/deepseek/chat/", {
            message: userMessage.text,
            history: this.internalMessages.slice(0, -1),
          });

          const botMessage = {
            text: response.data.reply,
            sender: "bot",
            avatar: "../doctor.png",
          };

          this.internalMessages.push(botMessage);
          this.$emit("update-messages", this.internalMessages);
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
    // 添加切换症状面板的方法
    toggleSymptomsPanel() {
      this.showSymptoms = !this.showSymptoms;
    },
  },
  watch: {
    messages: {
      immediate: true,
      handler(newMessages) {
        this.internalMessages = [...newMessages];
      },
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

.symptoms-tags {
  padding: 1em;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
  margin-bottom: 1em;
}

.symptoms-category {
  margin-bottom: 1em;
}

.symptoms-category h4 {
  margin: 0.5em 0;
  color: #666;
  font-size: 0.9em;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em;
}

.symptom-tag {
  display: inline-block;
  padding: 0.3em 0.8em;
  background-color: #e9ecef;
  border-radius: 16px;
  font-size: 0.9em;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s ease;
}

.symptom-tag:hover {
  background-color: #dee2e6;
}

.symptom-tag.active {
  background-color: #3f51b5;
  color: white;
}

.selected-symptoms {
  padding: 0.5em;
  margin-bottom: 0.5em;
  font-size: 0.9em;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.input-container {
  display: flex;
  flex-direction: column;
  padding: 1em;
  background-color: white;
  border-top: 1px solid #eee;
}

.input-container input {
  flex: 1;
  padding: 0.8em;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 0.5em;
  font-size: 0.95em;
}

.input-container button {
  padding: 0.8em 1.5em;
  background-color: #3f51b5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  align-self: flex-end;
}

.input-container button:hover {
  background-color: #303f9f;
}

.symptoms-toggle {
  padding: 0.5em 1em;
  border-bottom: 1px solid #eee;
}

.symptoms-toggle button {
  background: none;
  border: none;
  color: #3f51b5;
  cursor: pointer;
  font-size: 0.9em;
  padding: 0.5em 1em;
  display: flex;
  align-items: center;
  gap: 0.5em;
}

.toggle-icon {
  display: inline-block;
  transition: transform 0.3s ease;
}

.toggle-icon.rotated {
  transform: rotate(180deg);
}

.symptoms-tags {
  padding: 1em;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
  transition: all 0.3s ease;
}

.input-container {
  padding: 1em;
  background-color: white;
  border-top: 1px solid #eee;
}

.input-row {
  display: flex;
  gap: 0.5em;
}

.input-row input {
  flex: 1;
  padding: 0.8em;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.95em;
}

.input-row button {
  padding: 0.8em 1.5em;
  background-color: #3f51b5;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-row button:hover {
  background-color: #303f9f;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1em;
}
</style>