<template>
  <div class="dialog-overlay" v-if="show" @click.self="cancel">
    <div class="dialog-content">
      <h2>患者基本信息</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>姓名：</label>
          <input v-model="patientInfo.name" required placeholder="请输入姓名" />
        </div>
        <div class="form-group">
          <label>年龄：</label>
          <input
            v-model="patientInfo.age"
            type="number"
            required
            placeholder="请输入年龄"
          />
        </div>
        <div class="form-group">
          <label>性别：</label>
          <select v-model="patientInfo.gender" required>
            <option value="">请选择性别</option>
            <option value="male">男</option>
            <option value="female">女</option>
          </select>
        </div>
        <div class="form-group">
          <label>身高(cm)：</label>
          <input
            v-model="patientInfo.height"
            type="number"
            required
            placeholder="请输入身高"
          />
        </div>
        <div class="form-group">
          <label>体重(kg)：</label>
          <input
            v-model="patientInfo.weight"
            type="number"
            required
            placeholder="请输入体重"
          />
        </div>
        <div class="form-group">
          <label>既往病史：</label>
          <textarea
            v-model="patientInfo.medicalHistory"
            placeholder="请输入既往病史（如有）"
          ></textarea>
        </div>
        <div class="form-group">
          <label>过敏史：</label>
          <textarea
            v-model="patientInfo.allergies"
            placeholder="请输入过敏史（如有）"
          ></textarea>
        </div>
        <div class="button-group">
          <button type="submit" class="submit-btn">确认</button>
          <button type="button" class="cancel-btn" @click="cancel">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "PatientInfoDialog",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      patientInfo: {
        name: "",
        age: "",
        gender: "",
        height: "",
        weight: "",
        medicalHistory: "",
        allergies: "",
      },
    };
  },
  methods: {
    submitForm() {
      this.$emit("submit", { ...this.patientInfo });
      this.resetForm();
    },
    cancel() {
      this.$emit("cancel");
      this.resetForm();
    },
    resetForm() {
      this.patientInfo = {
        name: "",
        age: "",
        gender: "",
        height: "",
        weight: "",
        medicalHistory: "",
        allergies: "",
      };
    },
  },
};
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background-color: white;
  padding: 2em;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

h2 {
  margin-top: 0;
  color: #2c3e50;
  text-align: center;
  margin-bottom: 1.5em;
}

.form-group {
  margin-bottom: 1em;
}

label {
  display: block;
  margin-bottom: 0.5em;
  color: #2c3e50;
  font-weight: 500;
}

input,
select,
textarea {
  width: 100%;
  padding: 0.5em;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}

textarea {
  height: 80px;
  resize: vertical;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 1em;
  margin-top: 2em;
}

button {
  padding: 0.5em 1.5em;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s;
}

.submit-btn {
  background-color: #3f51b5;
  color: white;
}

.submit-btn:hover {
  background-color: #303f9f;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}
</style> 