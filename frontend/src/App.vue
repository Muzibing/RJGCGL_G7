<template>
  <div id="app">
    <nav>
      <button @click="startNewChat">新建聊天</button>
    </nav>
    <div class="main-container">
      <!-- 左侧历史记录列表 -->
      <aside class="sidebar">
        <h2>历史对话记录</h2>
        <ul>
          <li v-for="(record, index) in chatHistory" :key="index">
            <button @click="loadChatHistory(index)" @dblclick="editChatName(index)">
              {{ record.name || `对话 ${index + 1}` }}
            </button>
          </li>
        </ul>
      </aside>

      <!-- 右侧聊天窗口 -->
      <router-view :key="activeChatIndex" :messages="activeMessages" @update-messages="updateMessages"/>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      chatHistory: [
        { name: "", messages: [] }, // 第一个对话初始化为空名称
      ],
      activeChatIndex: 0, // 从第一个对话开始
      isLoggedIn: false,
      username: '',
    };
  },
  provide() {
    return {
      isLoggedIn: this.isLoggedIn,
      username: this.username,
      setLogin: this.setLogin,
    };
  },
  computed: {
    activeMessages() {
      return this.chatHistory[this.activeChatIndex].messages;
    },
  },
  methods: {
    setLogin(status, username = "") {
      this.isLoggedIn = status;
      this.username = username;
    },
    startNewChat() {
      if (this.chatHistory[this.activeChatIndex].messages.length > 0) {
        this.chatHistory[this.activeChatIndex] = { ...this.chatHistory[this.activeChatIndex] };
      }

      this.chatHistory.push({ name: "", messages: [] });
      this.activeChatIndex = this.chatHistory.length - 1;
    },
    loadChatHistory(index) {
      this.activeChatIndex = index;
    },
    updateMessages(messages) {
      if (this.activeChatIndex >= 0) {
        this.chatHistory[this.activeChatIndex].messages = messages;
      }
    },
    editChatName(index) {
      const newName = prompt("请输入新的对话名称:", this.chatHistory[index].name || "");
      if (newName !== null) {
        this.chatHistory[index].name = newName.trim() || null;
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
}

nav {
  background-color: #3f51b5;
  padding: 1em;
  color: white;
  text-align: center;
}

button {
  background-color: #ff4081;
  color: white;
  border: none;
  padding: 0.5em 1em;
  cursor: pointer;
  font-size: 1em;
  border-radius: 4px;
  margin: 5px;
}

.main-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f1f1f1;
  padding: 1em;
  border-right: 1px solid #ddd;
  overflow-y: auto;
}

.sidebar h2 {
  margin-top: 0;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 0.5em;
}

.sidebar button {
  width: 100%;
  text-align: left;
  background-color: #fff;
  color: #333;
  border: 1px solid #ddd;
  padding: 0.5em;
  cursor: pointer;
}

.sidebar button:hover {
  background-color: #ddd;
}
</style>
