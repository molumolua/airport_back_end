<template>
    <div class="register">
        <el-card class="register-content">
            <div class="register-title">
                <div class="register-back">
                    <el-button icon="el-icon-back" @click="toBack">返回</el-button>
                </div>
                <div class="register-content-title">
                    <h2>注册</h2>
                </div>
                <div class="register-blank"></div>
            </div>
            
            <div class="register-form-items">
                <el-form 
                class="register-el-form" 
                ref="ruleForm" 
                :model="ruleForm" 
                label-width="80px" 
                :rules="rules" 
                size="mini">
                    <el-form-item label="姓名" prop="name">
                        <el-input placeholder="请输入姓名" v-model="ruleForm.name" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="身份证号" prop="ID">
                        <el-input placeholder="请输入身份证号" v-model="ruleForm.ID" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="手机号" prop="phoneNumber">
                        <el-input placeholder="请输入手机号" v-model="ruleForm.phoneNumber" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password1">
                        <el-input placeholder="请输入密码" v-model="ruleForm.password1" autocomplete="off" 
                            type="password" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="password2">
                        <el-input placeholder="请输入密码" v-model="ruleForm.password2" autocomlete="off" 
                            type="password" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="验证码" prop="verificationCode">
                        <el-input placeholder="请输入验证码" v-model="ruleForm.verificationCode" 
                            style="width: 40%;" clearable></el-input>
                        <el-button id="verificationCode-button" type="primary" @click="getVerificationCode">获得验证码</el-button>
                    </el-form-item>
                    <el-form-item size="medium">
                        <el-button id="register-button" type="primary" @click="submitForm('ruleForm')">注册</el-button>
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
            while(Random.length < 4) {
                Random = "0" + Random;
            }
        var checkName = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('名字不能为空'));
            }
            setTimeout(() => {
                var flag = true;
                for(var i = 0;i < value.length; i++) {
                    if(value.charCodeAt(i) <= 255) {
                        flag = false;
                        break;
                    }
                }
                if(!flag) {
                    callback(new Error('名字必须是中文'));
                } else {
                    callback();
                }
            }, 500);
        };
        var checkID = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('身份证不能为空'));
            }
            setTimeout(() => {
                var year = parseInt(value.substring(6, 10));
                var month = parseInt(value.substring(10, 12));
                var day = parseInt(value.substring(12, 14));
                var numbers = value.substring(0, 17).split('');
                var last = value.substring(17);
                var big = [1, 3, 5, 7, 8, 10, 12]
                var small = [4, 6, 9, 11]
                if (value.length != 18) {
                    return callback(new Error('身份证号输入错误'));
                }
                if(year == 0) {
                    return callback(new Error('身份证号输入错误'));
                }
                if(month < 1 || month > 12) {
                    return callback(new Error('身份证号输入错误'));
                }
                if(big.indexOf(month) != -1) {
                    if(day < 1 || day > 31) {
                        return callback(new Error('身份证号输入错误'));
                    }
                    callback();
                } else if(small.indexOf(month) != -1) {
                    if(day < 1 || day > 30) {
                        return callback(new Error('身份证号输入错误'));
                    }
                    callback();
                } else {
                    if((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
                        if(day < 1 || day > 29) {
                            return callback(new Error('身份证号输入错误'));
                        }
                        callback();
                    } else {
                        if(day < 1 || day > 28) {
                            return callback(new Error('身份证号输入错误'));
                        }
                        callback();
                    }
                }
                for(var i = 0; i < numbers.length; i++) {
                    if(numbers[i] < '0' || numbers[i] > '9') {
                        return callback(new Error('身份证号输入错误'));
                    }
                }
                if((last >= '0' && last <= '9') || last == 'x' || last == 'X') {
                    callback();
                } else {
                    return callback(new Error('身份证号输入错误'));
                }
            }, 500);
        };
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
                for(var i = 0; i < chars.length; i++) {
                    var j = chars[i];
                    if((j >= 'a' && j <= 'z') || (j >= 'A' && j <= 'Z') || (j >= '0' && j <= '9') || j === '_') {
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
            } else if(value !== this.ruleForm.password1) {
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
                if(value != Random) {
                    callback(new Error('验证码输入错误'));
                } else {
                    callback();
                }
            }, 500);
        };
        return {
            verificationCodeRandom: Random,
            ruleForm: {
                name: '',
                ID: '',
                phoneNumber: '',
                password1: '',
                password2: '',
                verificationCode: ''
            },
            rules: {
                name: [
                    { validator: checkName, trigger: 'blur'}
                ],
                ID: [
                    {validator: checkID, trigger: 'blur'}
                ],
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
                if(valid) {
                    alert('submit!');
                    console.log('submit!');
                } else {
                    alert("error!");
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
.register {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.register-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    width: 400px;
    height: 450px;
}

.register-title {
    display: flex;
    justify-content: space-around;
    width: 100%;
}

.register-back {
    height: 30px;
    float: left;
    width: 90px;
}

.register-blank {
    width: 90px;
}

.register-form-items {
    width: 98%;
}

#register-button {
    width: 80%;
}

#verificationCode-button {
    margin-left: 20px;
}
</style>