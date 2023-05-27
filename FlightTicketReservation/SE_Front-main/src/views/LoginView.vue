<template>
    <div class="login">
        <el-card class="login-content">
            <div class="login-content-title">
                <el-menu :default-active="activeIndex" class="login-menu" mode="horizontal" @select="handleSelect">
                    <el-menu-item class="login-menu-items" index="1">用户</el-menu-item>
                    <el-menu-item class="login-menu-items" index="2">管理员</el-menu-item>
                </el-menu>
            </div>
            <div class="login-form-items">
                <el-form
                class="login-el-form"
                ref="form"
                :model="form"
                :rules="rules"
                label-width="80px">
                    <el-form-item label="手机号" prop="phoneNumber">
                        <el-input placeholder="请输入手机号" v-model="form.phoneNumber" clearable></el-input>
                        <div class="login-link">
                            <router-link class="login-form-link" to="/register">去注册</router-link>
                        </div>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input placeholder="请输入密码" v-model="form.password" show-password clearable></el-input>
                        <div class="login-link">
                            <router-link class="login-form-link" to="/findPassword">找回密码</router-link>
                        </div>
                    </el-form-item>
                    <el-form-item>
                        <el-button id="login-button" type="primary" @click="onSubmit">登录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-card>
    </div>
</template>

<script>
export default {
    data() {
        var checkPhoneNumber = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('手机号不能为空'));
            }
            setTimeout(() => {
                if (value.length != 11) {
                    return callback(new Error('手机号应为11位'));
                }
                var numbers = value.split('');
                for (var i = 0; i < numbers.length; i++) {
                    if (numbers[i] < '0' || numbers[i] > '9') {
                        return callback(new Error('手机号应为数字'));
                    }
                }
                callback();
            }, 500);
        };
        var checkPassword = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('密码不能为空'));
            }
            setTimeout(() => {
                var chars = value.split('');
                for (var i = 0; i < chars.length; i++) {
                    var j = chars[i];
                    if ((j >= 'a' && j <= 'z') || (j >= 'A' && j <= 'Z') || (j >= '0' && j <= '9') || j === '_') {
                        callback();
                    } else {
                        return callback(new Error('密码应由a-z、A-Z、0-9、下划线组成'))
                    }
                }
            }, 500);
        };
        return {
            activeIndex: '1',
            form: {
                phoneNumber: '',
                password: ''
            },
            rules: {
                phoneNumber: [
                    { validator: checkPhoneNumber, trigger: 'blur' }
                ],
                password: [
                    { validator: checkPassword, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        onSubmit() {
            this.$refs['form'].validate(valid => {
                if (valid) {
                    console.log('submit!');
                } else {
                    console.log('error submit!');
                    return false;
                }
            });
            // 登录接口
        },
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
        }
    }
}
</script>

<style>
.login {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.login-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 400px;
    height: 300px;
}

.login-content-title {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 98%;
}

.login-form-items {
    width: 98%;
}

.login-menu-items {
    font-weight: bold;
    font-size: 120%;
}

.login-link {
    position: relative;
    height: 15px;
}

.login-form-link {
    color: #409EFF;
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    vertical-align: middle;
    position: relative;
    text-decoration: none;
    outline: 0;
    padding: 0;
    font-weight: 500;
    position: absolute;
    right: 10px;
    top: 0;
}

.login-form-link:hover {
    color: red;
    text-decoration: underline;
}

#login-button {
    width: 80%;
}
</style>