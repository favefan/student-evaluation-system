<template>
  <el-form>
    <el-form-item label="昵称">
      <el-input v-model.trim="user.name" :disabled="true" />
    </el-form-item>
    <el-form-item label="Email">
      <el-input v-model.trim="user.email" />
    </el-form-item>
    <el-form-item label="新密码">
      <el-input placeholder="请输入新密码" show-password />
      <!-- <el-input v-model.trim="user.email" /> -->
    </el-form-item>
    <el-form-item label="当前密码">
      <el-input placeholder="请输入原密码" show-password />
      <!-- <el-input v-model.trim="user.email" /> -->
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit">更新</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '',
          email: ''
        }
      }
    }
  },
  methods: {
    submit() {
      this.$message({
        message: '账户信息更新成功',
        type: 'success',
        duration: 5 * 1000
      })
    }
  }
}
</script>
