<template>
  <div class="auth-page">
    <div class="auth-container">
      <h1>AI辅助就医问诊引擎</h1>
      <h2>登录</h2>
      <form @submit.prevent="login" class="auth-form">
        <div class="input-group">
          <input v-model="username" type="text" placeholder="用户名" required />
        </div>
        <div class="input-group">
          <input v-model="password" type="password" placeholder="密码" required />
        </div>
        <button type="submit" class="primary-btn">登录</button>
      </form>
      <div class="auth-actions">
        <p>
          <span>没有账号？</span>
          <button @click="navigateToRegister" class="secondary-btn">注册</button>
        </p>
      </div>
      <p>
        <button class="back-btn" @click="navigateToHome">返回主页</button>
      </p>
      <p v-if="message" :class="{ success: success, error: !success }">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      message: "",
      success: false,
    };
  },
  methods: {
    async login(event) {
      event.preventDefault();

      try {
        const response = await fetch("http://127.0.0.1:8000/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          redirect: 'manual',  // 禁止自动重定向
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (!response.ok) {
          throw new Error("网络错误");
        }

        const data = await response.json();

        if (data.success) {
          this.message = "登录成功";
          this.success = true;
          this.username = data.username;
          this.$router.push("/"); // 登录后跳转到首页
        } else {
          this.message = data.message;
          this.success = false;
        }
      } catch (error) {
        this.message = "登录失败，请重试";
        this.success = false;
      }
    },
    navigateToRegister() {
      this.$router.push("/register");
    },
    navigateToHome() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* 背景渐变，使用浅蓝色 */
.auth-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #a8c9ff, #6f8eff); /* 浅蓝色渐变 */
  color: white;
  z-index: 999;
}

.auth-container {
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  border-radius: 10px;
  padding: 40px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #3f51b5;
  font-size: 2.5em;
  margin-bottom: 20px;
}

h2 {
  color: #333;
  margin-bottom: 25px;
  font-weight: 400;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.input-group {
  position: relative;
}

.auth-form input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ddd;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.auth-form input:focus {
  border-color: #3f51b5;
  box-shadow: 0 0 8px rgba(63, 81, 181, 0.5);
}

button {
  padding: 12px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s;
  margin-top: 20px;
}

.primary-btn {
  background-color: #4CAF50; /* 绿色 */
  color: white;
}

.primary-btn:hover {
  background-color: #45a049; /* 深绿色 */
}

.secondary-btn {
  background-color: transparent;
  color: #4CAF50; /* 绿色 */
  border: 1px solid #4CAF50;
  padding: 8px 16px;
  font-size: 14px;
  text-decoration: underline;
  margin-top: 10px;
}

.secondary-btn:hover {
  color: #388e3c;
  border-color: #388e3c;
}

.auth-actions {
  margin-top: 20px;
  text-align: center;
}

.auth-actions span {
  color: #3f51b5; /* 蓝色 */
}

.success {
  color: green;
  font-size: 14px;
  margin-top: 15px;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 15px;
}
</style>
