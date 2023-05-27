<template>
    <div class="flight">
        <p class="title"> 航班查询 </p>
        <el-form :rules="rules" ref="form" :model="form" label-width="80px">
            <el-row :gutter="0">
                <el-col :span="3" :offset="7">
                <el-form-item label="起飞城市" prop="departureCity">
                    <el-cascader
                    v-model="form.departureCity"
                    placeholder="北京"
                    :options="options"
                    filterable></el-cascader>
                </el-form-item>
                </el-col>
                <el-col :span="1" :offset="1">
                    <el-image class="icon"
                    :src="require('../img/icon.png')"
                    fit="fit"></el-image>
                </el-col>
                <el-col :span="3">
                <el-form-item label="到达城市" prop="arrivalCity">
                    <el-cascader
                    v-model="form.arrivalCity"
                    placeholder="上海"
                    :options="options"
                    filterable></el-cascader>
                </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="0">
                <el-col :span="5" :offset="7">
                <el-form-item label="起飞时间" prop="date">
                    <el-date-picker
                    v-model="form.date"
                    :picker-options="pickerOptions"
                    type="date"
                    placeholder="选择日期">
                    </el-date-picker>
                </el-form-item>
                </el-col>
                <el-col :span="6">
                <el-form-item label="预期票价">
                    <el-input-number 
                    v-model="form.price" 
                    controls-position="right" 
                    :step="20"
                    :min="0" :max="10000"></el-input-number>
                </el-form-item>
                </el-col>
            </el-row>
            </el-form>
            <el-row :gutter="0">
            <el-col :span="7" :offset="10"><el-button class="main-button" type="primary" plain @click="submitForm('form')">查询</el-button></el-col>
            <el-col :span="6"><div id="manager" v-if="this.$store.state.identity == 2">
                <el-button v-on:click="toAddFlight" type="info">添加航班</el-button>
                <el-button type="info">导出航班</el-button>
            </div></el-col>
            </el-row>
        <el-divider></el-divider>
        <el-table
            :data="tableData"
            stripe
            class="result-list">
            <el-table-column
            prop="departureAirport"
            label="出发机场"
            width="80">
            </el-table-column>
            <el-table-column
            prop="icon"
            label=""
            width="35">
                <template slot-scope="scope">
                    <i class="el-icon-d-arrow-right"></i>
                </template>
            </el-table-column>
            <el-table-column
            prop="arrivalAirport"
            label="到达机场"
            width="100">
            </el-table-column>
            <el-table-column
            prop="time"
            label="起飞时间"
            width="160">
            </el-table-column>
            <el-table-column
            prop="flight"
            label="航班号"
            width="100">
            </el-table-column>
            <el-table-column
            label="头等舱"
            width="80">
            <template slot-scope="scope">{{scope.row.price1}}￥</template>
            </el-table-column>
            <el-table-column
            prop="ticket1"
            label="余票"
            width="60">
            </el-table-column>
            <el-table-column
            label="商务舱"
            width="80">
            <template slot-scope="scope">{{scope.row.price2}}￥</template>
            </el-table-column>
            <el-table-column
            prop="ticket2"
            label="余票"
            width="60">
            </el-table-column>
            <el-table-column
            label="经济舱"
            width="80">
            <template slot-scope="scope">{{scope.row.price3}}￥</template>
            </el-table-column>
            <el-table-column
            prop="ticket3"
            label="余票"
            width="60">
            </el-table-column>
            <el-table-column
                align="right">
            <template slot-scope="scope">
                <el-button
                size="mini"
                @click="handleMessage(scope.row)">查看</el-button>
            </template>
            </el-table-column>
        </el-table>

    </div>
</template>

<script>
    export default {
        data() {
            const validate1 = (rule, value, callback) => {
                if (value[0] == this.form.departureCity[0]) {
                    callback(new Error('请选择与出发城市不同的城市'))
                } else {
                    callback()
                }
            }
            return {
                form: {
                    date  : '',
                    price : 500,
                    departureCity : '',
                    arrivalCity : '',
                },
                pickerOptions: {
                    disabledDate(time) {
                        return time.getTime() < Date.now() - 24*60*60*1000;
                    },
                },
                tableData: [{
                    arrivalAirport: '北京大兴',
                    departureAirport: '上海浦东',
                    flight: 'M1234',
                    time :'2023-05-21 19:30',
                    price1 : 1500,
                    price2 : 1200,
                    price3 : 800,
                    ticket1 : 2,
                    ticket2 : 3,
                    ticket3 : 15,
                    insurance : {
                        label : '保险方案1',
                        price : 3
                    },
                    canceled : false,
                }],
                options : [{
                    value : 'Beijing',
                    label : '北京',
                },{
                    value : 'Shanghai',
                    label : '上海',
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
                rules: {
                    departureCity: [
                        { required: true, message: '请选择出发城市', trigger: 'change' }
                    ],
                    arrivalCity: [
                        { required: true, message: '请选择到达城市', trigger: 'change' },
                        { validator: validate1, trigger: 'blur'}
                    ],
                    date: [
                        { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
                    ],
                }   
            }
        },
        methods : {
            toAddFlight() {
                this.$router.push({path : "/addFlight"});
            },
            submitForm(formName) {
                console.log(this.$refs[formName])
                this.$refs[formName].validate((valid) => {
                if (valid) {
                    alert('submit!');
                } else {
                    console.log('error submit!!');
                    return false;
                }
                });
            },
            handleMessage (row) {
                this.$store.commit('updateCurrentFlight',row)
                this.$router.push({path: "/flightInfo"});
            },
        },
    }
</script>
 
<style src='../assets/css/flight.css' scoped>
</style>
