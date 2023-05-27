<template>
    <div class="ticketInfo">
        <el-row>
            <el-col :span="2" :offset="11">
            <p class="title">历史订单</p>
            </el-col>
        </el-row>
        <el-collapse class="result-list" v-model="activeNames">
            <el-collapse-item v-for="order in orderList" :name="order.id" :key="order.id">
                <template slot="title">
                    <el-row>
                        <el-col :span="4">
                            订单号：{{order.id}}
                        </el-col>
                        <el-col :span="6">
                            购买时间：{{order.purchaseTime}}
                        </el-col>
                        <el-col :span="6">
                            {{order.departureAirport}} -> {{order.arrivalAirport}}
                        </el-col>
                        <el-col :span="6">
                            <el-button 
                            type="info" 
                            size="small"
                            plain 
                            @click.stop.prevent=openCollapse()>开具发票</el-button>
                        </el-col>
                    </el-row>
                </template>
                <el-table
                    :data="order.ticketList"
                    stripe>
                    <el-table-column
                    prop="departureAirport"
                    label="出发机场"
                    width="80">
                        <template slot-scope="scope">
                            {{order.departureAirport}}
                        </template>
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
                        <template slot-scope="scope">
                            {{order.arrivalAirport}}
                        </template>
                    </el-table-column>
                    <el-table-column
                    prop="flight"
                    label="航班号"
                    width="100">
                        <template slot-scope="scope">
                            {{order.flight}}
                        </template>
                    </el-table-column>
                    <el-table-column
                    prop="time"
                    label="起飞时间"
                    width="160">
                        <template slot-scope="scope">
                            {{order.flightTime}}
                        </template>
                    </el-table-column>
                    <el-table-column
                    prop="name"
                    label="乘客姓名"
                    width="100">
                    </el-table-column>
                    <el-table-column
                    prop="seat"
                    label="座位号"
                    width="100">
                    </el-table-column>
                    <el-table-column
                        align="right">
                        <template slot-scope="scope">
                        <el-button 
                            v-if="!scope.row.canceled"
                            size="mini"
                            @click="temp">申请值机</el-button>
                        </template>
                    </el-table-column>
                    <el-table-column
                        align="right">
                        <template slot-scope="scope">
                            <el-button
                            v-if="!scope.row.food"
                            size="mini"
                            :disabled="scope.row.canceled"
                            @click="changeFood(scope.row)">预定餐食</el-button>
                            <el-button
                            v-else
                            size="mini"
                            type="primary"
                            :disabled="scope.row.canceled"
                            @click="changeFood(scope.row)">取消预定</el-button>
                        </template>
                    </el-table-column>
                    <el-table-column
                        align="right">
                        <template slot-scope="scope">
                            <el-popconfirm 
                            title="确定退票吗？"
                            @confirm="cancel(scope.row)">
                                <el-button
                                slot="reference"
                                size="mini"
                                type="danger"
                                plain
                                :disabled="scope.row.canceled">
                                    <div v-if="scope.row.canceled">已退票</div>
                                    <div v-else>退票</div>
                                </el-button>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                </el-table>
            </el-collapse-item>
        </el-collapse>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                activeNames: [],
                orderList : [{
                    id : 'X00001',
                    purchaseTime : '2023-05-21',
                    departureAirport : '北京大兴',
                    arrivalAirport : '上海浦东',
                    flight : 'M1234',
                    flightTime : '2023-05-23 19:30',
                    ticketList : [{
                        name : '张三',
                        seat : '12C',
                        food : false,
                        canceled : false,
                    },{
                        name : '李四',
                        seat : '12A',
                        food : false,
                        canceled : false,
                    }]
                },{
                    id : 'X00002',
                    purchaseTime : '2023-05-21',
                    departureAirport : '北京大兴',
                    arrivalAirport : '上海浦东',
                    flight : 'M1234',
                    flightTime : '2023-05-23 19:30',
                    ticketList : [{
                        name : '王五',
                        seat : '12B',
                        food : false,
                        canceled : false,
                    }]
                }]
            }
        },
        methods : {
            cancel(row) {
                row.canceled = true;
            },
            changeFood(row) {
                row.food = !row.food; 
            },
            temp() {
                alert(':D');
            }
        }
    }
</script>


<style src='../assets/css/ticketInfo.css' scoped>
</style>
