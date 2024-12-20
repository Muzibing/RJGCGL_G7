<template>
  <div class="health-info">
    <h2>用户健康信息</h2>
    <form @submit.prevent="saveHealthInfo">
      <textarea
        v-model="healthInfo"
        placeholder="请输入您的健康信息..."
        rows="4"
      ></textarea>
      <button type="submit">保存</button>
    </form>
    <p v-if="message" class="success">{{ message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      healthInfo: "",
      message: "",
    };
  },
  methods: {
    saveHealthInfo() {
      fetch("http://127.0.0.1:8000/api/health-info/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: this.$parent.username, // 从父组件获取用户名
          healthInfo: this.healthInfo,
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            this.message = "健康信息保存成功";
          } else {
            this.message = "保存失败，请重试";
          }
        })
        .catch(() => {
          this.message = "保存失败，请检查网络";
        });
    },
  },
};
</script>

<style>
.health-info {
  border: 1px solid #ddd;
  padding: 1em;
  border-radius: 8px;
  background-color: #f9f9f9;
  width: 400px;
  margin: 20px auto;
}

.health-info h2 {
  margin-top: 0;
}

.health-info textarea {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1em;
}

.health-info button {
  padding: 10px;
  font-size: 16px;
  border: none;
  background-color: #3f51b5;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}

.success {
  color: green;
  margin-top: 10px;
}
</style>
