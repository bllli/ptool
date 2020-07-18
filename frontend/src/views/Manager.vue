<template>
    <div id="app">
        <h1>做种🐔管理工具</h1>
        <h3>看明白再操作啊</h3>
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>版本信息 Version</span>
                <el-button style="float: right; padding: 3px 0" type="text" v-on:click="updateAppVersion">刷新</el-button>
            </div>
            <div>
                {{ version }}
            </div>
        </el-card>

        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>服务状态</span>
                <el-button style="float: right; padding: 3px 0" type="text" v-on:click="updateAppStatus">刷新</el-button>
            </div>
            <div>
                <el-table
                        :data="app_status"
                        border
                        style="width: 100%">
                    <el-table-column
                            prop="name"
                            label="服务名"
                            width="180">
                    </el-table-column>
                    <el-table-column
                            prop="description"
                            label="状态描述"
                            width="250">
                    </el-table-column>
                    <el-table-column
                            prop="statename"
                            label="状态">
                    </el-table-column>
                    <el-table-column label="操作">
                        <template slot="header" slot-scope="">
                            <el-button
                                    size="mini"
                                    type="danger"
                                    v-bind:loading="all_app_restarting"
                                    @click="restartAppFFFF()">全部重启
                            </el-button>
                        </template>
                        <template slot-scope="scope">
                            <el-button
                                    size="mini"
                                    type="danger"
                                    v-bind:loading="scope.row.restarting"
                                    @click="restartAppFFFF(scope.$index, scope.row.name)">重启
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
        </el-card>
        <el-row>
            <div class="text-wrapper">
            </div>
        </el-row>
    </div>
</template>

<script>
    import {getAppStatus, getAppVersion, restartApp} from '@/api/manager'

    export default {
        name: "Manager",
        data() {
            return {
                version: "123",
                app_status: [],
                all_app_restarting: false,
            }
        },
        mounted() {
            this.updateAppVersion()
            this.updateAppStatus()
        },
        methods: {
            restartAppFFFF: function (row_index, app_name) {
                let message = `全部服务重启完成`
                if (row_index !== undefined) {
                    this.app_status[row_index].restarting = true
                    message = `${app_name}服务重启完成`
                } else {
                    console.log(this.all_app_restarting)
                    this.all_app_restarting = true
                    console.log(this.all_app_restarting)
                }
                // restartApp(app_name).then(() => {
                //     this.$notify({
                //         title: '提示',
                //         message: message,
                //         duration: 0
                //     });
                //     if (row_index !== undefined) {
                //         this.app_status[row_index].restarting = false
                //     } else {
                //         this.all_app_restarting = false
                //     }
                //     this.updateAppStatus()
                // })
            },
            updateAppVersion: function () {
                getAppVersion().then(resp => {
                    console.log(resp.data.data)
                    this.version = resp.data.data
                })
            },
            updateAppStatus: function () {
                getAppStatus().then(resp => {
                    let status_info = resp.data.info
                    let status = []
                    for (let app_name in status_info) {
                        let app_info = status_info[app_name]
                        app_info.restarting = false
                        status.push(app_info)
                    }
                    this.app_status = status
                })
            }
        }
    }
</script>

<style scoped>
    .text-wrapper {
        white-space: pre-wrap;
    }
</style>