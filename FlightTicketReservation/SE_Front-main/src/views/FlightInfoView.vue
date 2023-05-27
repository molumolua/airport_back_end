<template>
    <div class="flight-info">
        <el-row :gutter="0">
            <el-col :span="2" :offset="2">
                <el-button 
                type="primary" 
                icon="el-icon-arrow-left"
                @click="toBack">返回</el-button>
            </el-col>
            <el-col :span="2" :offset="7">
            <p class="title"> 航班信息 </p>
            </el-col>
        </el-row>
        <el-card class="box-card">
            <el-row :gutter="0">
                航班号：{{this.form.flight}}<span v-if="this.form.canceled" class="canceled">[已取消]</span>
            </el-row>
            <el-row :gutter="0">
                出发机场： {{this.form.departureAirport}}
            </el-row>
            <el-row :gutter="0">
                到达机场： {{this.form.arrivalAirport}}
            </el-row>
            <el-row :gutter="0">
                起飞时间： {{this.form.time}}
            </el-row>
            <el-divider></el-divider>
            <el-table
                :data="tableData"
                stripe>    
                <el-table-column
                prop="title"
                label="">
                </el-table-column>
                <el-table-column
                prop="first"
                label="头等舱"
                width="120">
                </el-table-column>
                <el-table-column
                prop="second"
                label="商务舱"
                width="120">
                </el-table-column>
                <el-table-column
                prop="third"
                label="经济舱"
                width="120">
                </el-table-column>
            </el-table>
        </el-card>
        <el-button v-if="this.$store.state.identity == 1" class="main-button" type="primary" @click="toOrder">去订票</el-button>
        <el-button v-if="this.$store.state.identity == 2" class="main-button" type="info" @click="toManager">管理航班</el-button>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                form : {},
                tableData:[{
                    title:'',
                    first:'',
                    second:'',
                    third:'',
                },{
                    title:'',
                    first:'',
                    second:'',
                    third:'',
                }]
            }
        },
        mounted() { 
            this.form = this.$store.state.currentFlight;
            this.tableData[0].title="票价￥";
            this.tableData[0].first=this.form.price1;
            this.tableData[0].second=this.form.price2;
            this.tableData[0].third=this.form.price3;
            this.tableData[1].title="余票--";
            this.tableData[1].first=this.form.ticket1;
            this.tableData[1].second=this.form.ticket2;
            this.tableData[1].third=this.form.ticket3;
        },
        methods :{
            toBack() {
                this.$router.back();
            },
            toOrder() {
                this.$router.push({path : "/order"});
            },
            toManager() {
                this.$router.push({path : "/manager"});
            }
        }
    }
</script>

<style src="../assets/css/flightInfo.css" scoped>
</style>