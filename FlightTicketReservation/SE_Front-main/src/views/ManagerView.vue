<template>
    <div class="manager" v-if="this.$store.state.identity == 2">
        <el-row :gutter="0">
            <el-col :span="2" :offset="7">
                <el-button 
                type="primary" 
                icon="el-icon-arrow-left"
                @click="toBack">返回</el-button>
            </el-col>
            <el-col :span="2" :offset="2">
            <p class="title"> 航班信息</p>
            </el-col>
        </el-row>
        <el-row>
            <el-card>
                <el-row>
                    <el-col :span="20">
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
                            prop="flight"
                            label="航班号"
                            width="100">
                            </el-table-column>
                            <el-table-column
                            label="起飞时间"
                            width="250">
                                <template slot-scope="scope">
                                    <div v-if="!changing">{{scope.row.time}}</div>
                                    <div v-else>
                                    <el-date-picker
                                    v-model="scope.row.time"
                                    value-format="yyyy-MM-dd hh:mm"
                                    type="datetime"
                                    placeholder="选择日期时间">
                                    </el-date-picker>
                                    </div>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-col>
                    <el-col :span="4">
                    <el-row>
                        <el-button
                            v-if="!changing"
                            :disabled="tableData[0].canceled"
                            @click="change">修改</el-button>
                        <el-button
                            v-else
                            type="primary"
                            :disabled="tableData[0].canceled"
                            @click="change">保存修改</el-button>
                    </el-row>
                    <el-row>
                        <el-popconfirm 
                            title="确定取消航班吗？"
                            @confirm="cancel()">
                                <el-button
                                slot="reference"
                                type="danger"
                                plain
                                :disabled="tableData[0].canceled">
                                    <div v-if="tableData[0].canceled">已取消</div>
                                    <div v-else>取消航班</div>
                                </el-button>
                        </el-popconfirm>
                    </el-row>
                    </el-col>
                </el-row>
            </el-card>
            <el-table 
                class="passenger-list"
                :data="passengerList"
                stripe>
                    <el-table-column
                    prop="name"
                    label="乘客姓名"
                    width="120">
                    </el-table-column>
                    <el-table-column
                    prop="id"
                    label="身份证号"
                    width="200">
                    </el-table-column>
                    <el-table-column
                    prop="seat"
                    label="座位号"
                    width="120">
                    </el-table-column>
                    <el-table-column
                    label="餐食预定"
                    width="120">
                        <template slot-scope="scope">
                            {{scope.row.food ? '是':'否'}}
                        </template>
                    </el-table-column>
                    <el-table-column
                        align="right"
                        label="状态">
                        <template slot-scope="scope">
                            <div v-if="scope.row.application">
                                <el-button
                                v-if="!scope.row.pass"
                                size="medium"
                                :disabled="tableData[0].canceled"
                                @click="pass(scope.row)">审核值机</el-button>
                                <el-button
                                v-else
                                size="medium"
                                type="primary"
                                :disabled="tableData[0].canceled">已值机</el-button>
                            </div>
                            <div v-else>
                                <el-button
                                size="medium"
                                v-if="!scope.row.pass"
                                type="warning"
                                :disabled="tableData[0].canceled">未申请值机</el-button>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column
                        align="right">
                        <template slot-scope="scope">
                            <el-popconfirm 
                            title="确定退票吗？"
                            @confirm="remove(scope.$index)">
                                <el-button
                                slot="reference"
                                size="medium"
                                type="danger"
                                plain
                                :disabled="tableData[0].canceled">
                                    <div v-if="scope.row.canceled">已退票</div>
                                    <div v-else>退票</div>
                                </el-button>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
            </el-table>
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
                tableData : [],
                passengerList : [{
                        name : '张三',
                        id : '100020003000400050',
                        seat : '12C',
                        food : false,
                        application : false,
                        pass : false,
                    },{
                        name : '李四',
                        id : '100020003000400051',
                        seat : '12A',
                        food : false,
                        application : true,
                        pass : false,
                    }],
                changing : false,
            }
        },
        mounted() { 
            this.tableData.push(this.$store.state.currentFlight);
        },
        methods : {
            toBack() {
                this.$router.back();
            },
            change() {
                this.changing = !this.changing;
            },
            cancel() {
                this.tableData[0].canceled = true;
            },
            pass(passenger) {
                if(!passenger.application) return;
                passenger.pass = true;
            },
            remove (index) {
                this.passengerList.splice(index, 1);
            }
        }
    }
</script>


<style src='../assets/css/manage.css' scoped>
</style>