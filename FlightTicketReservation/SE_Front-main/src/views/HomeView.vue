<template>
  <div class="home">
    <el-container class="home-container">
      <el-aside class="home-aside" width="80%">
        <h1 class="home-title">欢迎使用机票预订系统</h1>
        <div class="home-else">
          <p>您可以：</p>
        </div>
        <div class="home-buttons">
          <router-link class="home-link" to="/flight">
            <el-button class="home-button" plain size="mini">查询航班信息</el-button>
          </router-link>
          <router-link class="home-link" to="/login">
            <el-button class="home-button" plain size="mini">去登录</el-button>
          </router-link>
        </div>
      </el-aside>
      <el-main class="home-main">
          <el-card class="home-card">
            通知栏
          </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>

</script>

<style>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 95%;
  height: 88%;
}

.home-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 95%;
  height: 100%;
}

.home-title {
  text-align: center;
  font-size: 300%;
  margin-bottom: 200px;
}

.home-else {
  font-size: 300%;
  margin-left: 250px;
}

.home-buttons {
  margin-left: 200px;
  margin-bottom: 200px;
}

.home-link {
  margin-left: 150px;
}

.home-button {
  width: 200px;
  height: 60px;
  font-size: large;
}

.home-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}
</style>