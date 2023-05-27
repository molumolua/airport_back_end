<template>
  <div id="app" style="position: relative; height: 100%;">
    <div v-if="this.$store.state.identity == 1">
      <el-menu 
      router
      :default-active="this.$router.path"
      class="el-menu-2" 
      mode="horizontal" 
      @select="handleSelect"
      >
        <el-menu-item> <i class="el-icon-position"></i></el-menu-item>
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/flight">航班信息</el-menu-item>
        <el-menu-item index="/ticketInfo">我的订单</el-menu-item>
        <el-menu-item index="/userInfo">个人信息</el-menu-item>
        <el-menu-item index="/about">关于我们</el-menu-item>
      </el-menu>
    </div>
    <div v-else>
      <el-menu 
      router
      :default-active="this.$router.path"
      class="el-menu-1" 
      mode="horizontal" 
      @select="handleSelect"
      >
      <el-menu-item> <i class="el-icon-position"></i></el-menu-item>
      <el-menu-item index="/">首页</el-menu-item>
      <el-menu-item index="/flight">航班信息</el-menu-item>
      <el-menu-item index="/about">关于我们</el-menu-item>
      </el-menu>
    </div>
    
    <div v-if="this.$store.state.identity == 0">
      <el-menu 
      style="position: absolute; right: 10px; top: 0;"
      :router="true"
      :default-active="this.$router.path"
      class="el-menu-1" 
      mode="horizontal" 
      @select="handleSelect" 
      >
        <el-menu-item index="/login" style="border-bottom-color: white !important;">登录</el-menu-item>
        <el-menu-item index="/register" style="border-bottom-color: white !important;">注册</el-menu-item>
      </el-menu>
    </div>
    <div v-else-if="this.$store.state.identity == 1">
      <el-menu 
      style="position: absolute; right: 10px; top: 0;"
      router
      :default-active="this.$router.path"
      class="el-menu-2" 
      mode="horizontal" 
      @select="handleSelect" 
      >
        <el-menu-item index="/userInfo" style="border-bottom-color: white !important;">用户名字</el-menu-item>
        <el-menu-item @click="del" style="border-bottom-color: white !important;">注销</el-menu-item>
      </el-menu>
    </div>
    <div v-else>
      <el-menu 
        style="position: absolute; right: 10px; top: 0;"
        router
        :default-active="this.$router.path"
        class="el-menu-3" 
        mode="horizontal" 
        @select="handleSelect" 
        >
          <el-menu-item index="/" style="border-bottom-color: white !important;">管理员名字</el-menu-item>
          <el-menu-item @click="del" style="border-bottom-color: white !important;">注销</el-menu-item>
        </el-menu>
    </div>
    <router-view/>
  </div>
</template>

<script>
  export default {
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      del() {
        this.$store.state.identity = 0;
        console.log(this.$store.state.identity);
        this.$router.push({path:'/'});
      }
    }
  }
</script>