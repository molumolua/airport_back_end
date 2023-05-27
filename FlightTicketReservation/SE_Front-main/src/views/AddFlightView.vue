<template>
    <div class="addFlight" v-if="this.$store.state.identity == 2">
        <el-row :gutter="0">
            <el-col :span="2" :offset="7">
                <el-button 
                type="primary" 
                icon="el-icon-arrow-left"
                @click="toBack">返回</el-button>
            </el-col>
            <el-col :span="2" :offset="2">
            <p class="title"> 添加航班</p>
            </el-col>
        </el-row>
        <el-form ref="form" :model="form" label-width="80px">
            <el-row :gutter="0">
                <el-col :span="4" :offset="7">
                <el-form-item label="出发机场">
                    <el-cascader
                    v-model="form.departureCity"
                    placeholder="北京"
                    :show-all-levels="false"
                    :options="options"
                    filterable></el-cascader>
                </el-form-item>
                </el-col>
                <el-col :span="1" :offset="1">
                    <el-image class="icon"
                    :src="require('../img/icon.png')"
                    fit="fit"></el-image>
                </el-col>
                <el-col :span="4">
                <el-form-item label="到达机场">
                    <el-cascader
                    v-model="form.arrivalCity"
                    placeholder="上海"
                    :show-all-levels="false"
                    :options="options"
                    filterable></el-cascader>
                </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="0">
                <el-col :span="5" :offset="7">
                <el-form-item label="时间">
                    <el-date-picker
                        v-model="form.span"
                        type="datetimerange"
                        range-separator="至"
                        start-placeholder="起飞时间"
                        end-placeholder="降落时间">
                    </el-date-picker>
                </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="0">
                <el-col :span="3" :offset="8">头等舱</el-col>
                <el-col :span="3">商务舱</el-col>
                <el-col :span="3">经济舱</el-col>
            </el-row>
            <el-row :gutter="0">
                <el-col :span="1" :offset="7">票价</el-col>
                <el-col :span="3">
                <el-input-number 
                    v-model="form.price1" 
                    controls-position="right" 
                    :step="20"
                    :min="0" :max="10000"></el-input-number>
                </el-col>
                <el-col :span="3">
                <el-input-number 
                    v-model="form.price2" 
                    controls-position="right" 
                    :step="20"
                    :min="0" :max="10000"></el-input-number>
                </el-col>
                <el-col :span="3">
                <el-input-number 
                    v-model="form.price3" 
                    controls-position="right" 
                    :step="10"
                    :min="0" :max="10000"></el-input-number>
                </el-col>
            </el-row>
            <el-row :gutter="0">
                <el-col :span="1" :offset="7">票量</el-col>
                <el-col :span="3">
                <el-input-number 
                    v-model="form.ticket1" 
                    controls-position="right" 
                    :step="1"
                    :min="0" :max="1000"></el-input-number>
                </el-col>
                <el-col :span="3">
                <el-input-number 
                    v-model="form.ticket2" 
                    controls-position="right" 
                    :step="1"
                    :min="0" :max="1000"></el-input-number>
                </el-col>
                <el-col :span="3">
                <el-input-number 
                    v-model="form.ticket3" 
                    controls-position="right" 
                    :step="1"
                    :min="0" :max="1000"></el-input-number>
                </el-col>
            </el-row>
            <el-row :gutter="0">
            <el-col :span="5" :offset="7">
            <el-form-item label="保险方案">
            <el-select v-model="form.insurance" placeholder="请选择">
                <el-option
                v-for="item in optionsInsurance"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                </el-option>
            </el-select></el-form-item></el-col>
            <el-col :span="7" :offset="3">
                <el-upload
                    class="upload-demo"
                    :on-preview="handlePreview"
                    :on-remove="handleRemove"
                    :before-remove="beforeRemove"
                    :limit="1"
                    :on-exceed="handleExceed"
                    :file-list="fileList">
                    <el-button size="small" type="primary">从文件中导入...</el-button>
                </el-upload>
            </el-col>
            </el-row>
            </el-form>
            <el-row :gutter="0">
            <el-col :span="5" :offset="10"><el-button class="main-button" type="primary" plain>提交</el-button></el-col>
            </el-row>
    </div>
    <div v-else>
        <el-result icon="error" title="permission denied" subTitle="您没有权限访问此页面">
        </el-result>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                form: {
                span  : '',
                price1 : 0,
                price2 : 0,
                price3 : 0,
                ticket1 : 0,
                ticket2 : 0,
                ticket3 : 0,
                insurance : 'insurance0',
                departureAirport : '',
                arrivalAirport : '',
                },
                options : [{
                    value : 'Beijing',
                    label : '北京',
                    children : [{
                        value : 'PEK',
                        label : '北京首都国际机场',
                    },{
                        value : 'PKX',
                        label : '北京大兴国际机场',
                    }]
                },{
                    value : 'Shanghai',
                    label : '上海',
                    children : [{
                        value : 'PVG',
                        label : '上海浦东国际机场',
                    },{
                        value : 'SHA',
                        label : '上海虹桥国际机场',
                    }]
                },{
                value : 'Guangdong',
                    label : '广东',
                    children : [{
                        value : 'Guangzhou',
                        label : '广州',
                    },{
                        value : 'Shenzhen',
                        label : '深圳',
                    }]
                }],
                optionsInsurance : [{
                    value: 'insurance0',
                    label: '无'
                    }, {
                    value: 'insurance1',
                    label: '保险1(3￥)'
                    }, {
                    value: 'insurance2',
                    label: '保险2(10￥)'
                    }, {
                    value: 'insurance3',
                    label: '保险3(30￥)'
                }],
            }
        },
        methods : {
            toBack() {
                this.$router.back();
            },
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePreview(file) {
                console.log(file);
            },
            handleExceed(files, fileList) {
                this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
            },
            beforeRemove(file, fileList) {
                return this.$confirm(`确定移除 ${ file.name }？`);
            }
        }
    }
</script>

<style src="../assets/css/addFlight.css" scoped>
</style>