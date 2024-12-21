<template>
  <div id="app">
    <div class="main-container">
      <!-- 左侧历史记录列表 -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <h2>历史对话记录</h2>
          <button
            class="add-chat-btn"
            @click="showPatientDialog"
            title="新建对话"
          >
            <span>+</span>
          </button>
        </div>
        <ul class="chat-list">
          <li
            v-for="(record, index) in chatHistory"
            :key="index"
            class="chat-item"
          >
            <div class="chat-item-content">
              <button
                @click="loadChatHistory(index)"
                :class="['chat-button', { active: index === activeChatIndex }]"
              >
                {{ record.name || `对话 ${index + 1}` }}
              </button>
              <div class="chat-actions">
                <button
                  class="action-btn"
                  @click.stop="editChatName(index)"
                  title="重命名"
                >
                  <span>✎</span>
                </button>
                <button
                  class="action-btn delete"
                  @click.stop="deleteChat(index)"
                  title="删除"
                >
                  <span>×</span>
                </button>
              </div>
            </div>
          </li>
        </ul>
      </aside>

      <!-- 右侧聊天窗口 -->
      <router-view
        :key="activeChatIndex"
        :messages="activeMessages"
        :patientInfo="activePatientInfo"
        @update-messages="updateMessages"
      />
    </div>

    <!-- 患者信息对话框 -->
    <PatientInfoDialog
      :show="showDialog"
      @submit="createNewChat"
      @cancel="cancelDialog"
    />
  </div>
</template>

<script>
import PatientInfoDialog from "./components/PatientInfoDialog.vue";

export default {
  components: {
    PatientInfoDialog,
  },
  data() {
    return {
      chatHistory: [{ name: "", messages: [], patientInfo: null }],
      activeChatIndex: 0,
      isLoggedIn: false,
      username: "",
      showDialog: false,
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
    activePatientInfo() {
      return this.chatHistory[this.activeChatIndex].patientInfo;
    },
  },
  methods: {
    setLogin(status, username = "") {
      this.isLoggedIn = status;
      this.username = username;
    },
    showPatientDialog() {
      this.showDialog = true;
    },
    cancelDialog() {
      this.showDialog = false;
    },
    createNewChat(patientInfo) {
      this.showDialog = false;
      const chatName = `${patientInfo.name}的问诊`;
      this.chatHistory.push({
        name: chatName,
        messages: [],
        patientInfo: patientInfo,
      });
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
      const currentName = this.chatHistory[index].name || `对话 ${index + 1}`;
      const newName = prompt("请输入新的对话名称:", currentName);
      if (newName !== null) {
        this.chatHistory[index].name = newName.trim() || null;
      }
    },
    deleteChat(index) {
      if (confirm("确定要删除这个对话吗？此操作不可恢复。")) {
        this.chatHistory.splice(index, 1);
        // 如果删除的是当前活动的对话，或者删除后没有对话了
        if (this.chatHistory.length === 0) {
          // 如果没有对话了，创建一个新的
          this.chatHistory.push({ name: "", messages: [], patientInfo: null });
          this.activeChatIndex = 0;
        } else if (index <= this.activeChatIndex) {
          // 如果删除的是当前对话或之前的对话，需要调整当前索引
          this.activeChatIndex = Math.max(
            0,
            Math.min(this.activeChatIndex - 1, this.chatHistory.length - 1)
          );
        }
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  height: 100vh;
}

.main-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #f5f7fa;
  padding: 1em;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;
  padding-bottom: 0.5em;
  border-bottom: 1px solid #e0e0e0;
}

.sidebar-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2em;
}

.add-chat-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  border-radius: 50%;
  background-color: #3f51b5;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5em;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.add-chat-btn:hover {
  background-color: #303f9f;
  transform: scale(1.05);
}

.add-chat-btn span {
  line-height: 1;
  margin-top: -2px;
}

.chat-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.chat-item {
  margin: 0.5em 0;
}

.chat-item-content {
  display: flex;
  align-items: center;
  gap: 0.5em;
}

.chat-button {
  flex: 1;
  text-align: left;
  padding: 0.8em 1em;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-button:hover {
  background-color: #f8f9fa;
}

.chat-button.active {
  background-color: #e8eaf6;
  border-color: #3f51b5;
  color: #3f51b5;
}

.chat-actions {
  display: flex;
  gap: 0.3em;
}

.action-btn {
  padding: 0.4em;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background-color: #e8eaf6;
  color: #3f51b5;
}

.action-btn.delete:hover {
  background-color: #ffebee;
  color: #f44336;
}
</style>
