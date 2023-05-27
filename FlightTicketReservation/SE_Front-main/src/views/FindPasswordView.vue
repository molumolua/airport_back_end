<template>
    <div class="findPassword">
        <el-card class="findPassword-content">
            <div class="findPassword-title">
                <div class="findPassword-back">
                    <el-button icon="el-icon-back" @click="toBack">返回</el-button>
                </div>
                <div class="findPassword-content-title">
                    <h2>找回密码</h2>
                </div>
                <div class="findPassword-blank"></div>
            </div>

            <div class="findPassword-form-items">
                <el-form 
                class="findPassword-el-form" 
                ref="findPasswordForm" 
                :model="findPasswordForm" 
                label-width="80px" 
                :rules="rules">
                    <el-form-item label="手机号" prop="phoneNumber">
                        <el-input placeholder="请输入手机号" v-model="findPasswordForm.phoneNumber" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="验证码" prop="verificationCode">
                        <el-input placeholder="请输入验证码" v-model="findPasswordForm.verificationCode" 
                            style="width: 40%;" clearable></el-input>
                        <el-button id="verificationCode-button" type="primary"
                            @click="getVerificationCode">获得验证码</el-button>
                    </el-form-item>
                    <el-form-item label="密码" prop="password1">
                        <el-input placeholder="请输入密码" v-model="findPasswordForm.password1" autocomplete="off"
                            type="password" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="password2">
                        <el-input placeholder="请输入密码" v-model="findPasswordForm.password2" autocomlete="off"
                            type="password" clearable></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button id="findPassword-button" type="primary" @click="submitForm('findPasswordForm')">确定</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-card>
    </div>
</template>

<script>
export default {
    data() {
        var Random = Math.round(Math.random() * 10000) + "";
        while (Random.length < 4) {
            Random = "0" + Random;
        }
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
        var checkPassword1 = (rule, value, callback) => {
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
        var checkPassword2 = (rule, value, callback) => {
            if (!value) {
                callback(new Error('密码不能为空'));
            } else if (value !== this.findPasswordForm.password1) {
                callback(new Error('两次密码输入不一致'));
            } else {
                callback();
            }
        };
        var checkVerficationCode = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('验证码不能为空'));
            }
            setTimeout(() => {
                if (value != Random) {
                    callback(new Error('验证码输入错误'));
                } else {
                    callback();
                }
            }, 500);
        };
        return {
            verificationCodeRandom: Random,
            findPasswordForm: {
                phoneNumber: '',
                password1: '',
                password2: '',
                verificationCode: ''
            },
            rules: {
                phoneNumber: [
                    { validator: checkPhoneNumber, trigger: 'blur' }
                ],
                password1: [
                    { validator: checkPassword1, trigger: 'blur' }
                ],
                password2: [
                    { validator: checkPassword2, trigger: 'blur' }
                ],
                verificationCode: [
                    { validator: checkVerficationCode, trigger: 'blur' }
                ],
            }
        }
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate(valid => {
                if (valid) {
                    console.log('submit!');
                } else {
                    console.log('error submit!');
                    return false;
                }
            });
        },
        getVerificationCode() {
            alert(this.$data.verificationCodeRandom);
        },
        toBack() {
            this.$router.back();
        }
    }
}
</script>

<style>
.findPassword {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.findPassword-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    width: 400px;
    height: 450px;
}

.findPassword-title {
    display: flex;
    justify-content: space-around;
    width: 100%;
}

.findPassword-back {
    height: 30px;
    float: left;
    width: 90px;
}

.findPassword-blank {
    width: 90px;
}

.findPassword-form-items {
    width: 98%;
}

#findPassword-button {
    width: 80%;
}
</style>