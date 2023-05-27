<template>
    <div class="userInfo">
        <div class="userInfo-content">
            <div class="userInfo-title">
                <div class="userInfo-content-title">
                    <h2>个人中心</h2>
                </div>
                <div class="userInfo-content-message">
                    <el-row class="userInfo-line">
                        <el-col :span="3" class="userInfo-key"><span >姓名</span></el-col>
                        <el-col :span="1" style="text-align: center;"><span>:</span></el-col>
                        <el-col :span="6" class="userInfo-value">
                            <span v-if="!isChange">{{ user.username }}</span>
                            <span v-else><el-input v-model="user.username"></el-input></span>
                        </el-col>
                        <el-col :span="3" class="userInfo-key"><span class="userInfo-key">信用分</span></el-col>
                        <el-col :span="1" style="text-align: center;"><span>:</span></el-col>
                        <el-col :span="6" class="userInfo-value">
                            <span>{{ user.credit }}</span>
                        </el-col>
                        
                    </el-row>
                    <el-row class="userInfo-line">
                        <el-col :span="3" class="userInfo-key"><span >身份证号</span></el-col>
                        <el-col :span="1" style="text-align: center;"><span>:</span></el-col>
                        <el-col :span="6" class="userInfo-value">
                            <span v-if="!isChange">{{ user.ID }}</span>
                            <span v-else><el-input v-model="user.ID"></el-input></span>
                        </el-col>
                        <el-col :span="3" class="userInfo-key"><span class="userInfo-key">信用等级</span></el-col>
                        <el-col :span="1" style="text-align: center;"><span>:</span></el-col>
                        <el-col :span="6" class="userInfo-value">
                            <span>{{ user.creditRating }}</span>
                        </el-col>
                    </el-row>
                    <el-row class="userInfo-line">
                        <el-col :span="3" class="userInfo-key"><span >邮箱</span></el-col>
                        <el-col :span="1" style="text-align: center;"><span>:</span></el-col>
                        <el-col :span="6" class="userInfo-value">
                            <span v-if="!isChange">{{ user.email }}</span>
                            <span v-else><el-input v-model="user.email"></el-input></span>
                        </el-col>
                        <el-col :span="3" class="userInfo-key"><span class="userInfo-key">出行次数</span></el-col>
                        <el-col :span="1" style="text-align: center;"><span>:</span></el-col>
                        <el-col :span="6" class="userInfo-value">
                            <span>{{ user.travalNumber }}</span>
                        </el-col>
                    </el-row>
                    <el-row class="userInfo-button-line">
                        <el-button class="userInfo-button" plain @click="change">
                            <span v-if="!isChange">修改个人信息</span>
                            <span v-else>确定修改</span>
                        </el-button>   
                    </el-row>
                    <el-row class="userInfo-button-line">
                        <router-link to="/changePassword">
                            <el-button class="userInfo-button" plain>修改密码</el-button>
                        </router-link>
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isChange: false,
            user: {
                username: '小明',
                credit: 20,
                ID: '123456200201031234',
                creditRating: 2,
                email: '123456@qq.com',
                travalNumber: 3
            }
        }
    },
    methods: {
        change() {
            if(this.isChange == false) {
                this.isChange = true;
            } else {
                alert('submint');
                this.isChange = false;
            }
        }
    }
}
</script>

<style>
.userInfo {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.userInfo-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    width: 70%;
    height: 450px;
}

.userInfo-title {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.userInfo-content-message {
    width: 100%;
}

.userInfo-line {
    width: 100%;
    display: flex;
    height: 40px;
    font-size: 120%;
}

.userInfo-key {
    width: 25%;
    text-align: right;
    padding-right: 5px;
}

.userInfo-value {
    padding-left: 5px;
}

.userInfo-button-line {
    margin-top: 8px;
    margin-left: 15px;
}
</style>