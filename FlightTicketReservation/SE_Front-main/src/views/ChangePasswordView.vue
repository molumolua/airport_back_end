<template>
    <div class="changePassword">
        <el-card class="changePassword-content">
            <div class="changePassword-title">
                <div class="changePassword-back">
                    <el-button icon="el-icon-back" @click="toBack">返回</el-button>
                </div>
                <div class="changePassword-content-title">
                    <h2>修改密码</h2>
                </div>
                <div class="changePassword-blank"></div>
            </div>

            <div class="changePassword-form-items">
                <el-form 
                class="changePassword-el-form"
                ref="changePasswordForm"
                :model="changePasswordForm"
                label-width="80px"
                :rules="rules">
                    <el-form-item label="旧密码" prop="oldPassword">
                        <el-input placeholder="请输入旧密码" v-model="changePasswordForm.oldPassword" autocomplete="off"
                            type="password" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="新密码" prop="password1">
                        <el-input placeholder="请输入新密码" v-model="changePasswordForm.password1" autocomplete="off"
                            type="password" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="password2">
                        <el-input placeholder="请输入新密码" v-model="changePasswordForm.password2" autocomlete="off"
                            type="password" clearable></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button id="changePassword-button" type="primary"
                            @click="submitForm('changePasswordForm')">确定</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-card>
    </div>
</template>

<script>
export default {
    data() {
        var checkOldPassword = (rule, value, callback) => {
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
            } else if (value !== this.changePasswordForm.password1) {
                callback(new Error('两次密码输入不一致'));
            } else {
                callback();
            }
        };
        return {
            changePasswordForm: {
                oldPassword: '',
                password1: '',
                password2: '',
            },
            rules: {
                oldPassword: [
                    { validator: checkOldPassword, trigger: 'blur' }
                ],
                password1: [
                    { validator: checkPassword1, trigger: 'blur' }
                ],
                password2: [
                    { validator: checkPassword2, trigger: 'blur' }
                ]
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
        toBack() {
            this.$router.back();
        }
    }
}
</script>

<style>
.changePassword {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.changePassword-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 10px;
    width: 400px;
    height: 450px;
}

.changePassword-title {
    display: flex;
    justify-content: space-around;
    width: 100%;
}

.changePassword-back {
    height: 30px;
    float: left;
    width: 90px;
}

.changePassword-blank {
    width: 90px;
}

.changePassword-form-items {
    width: 98%;
}

#changePassword-button {
    width: 40%;
}
</style>