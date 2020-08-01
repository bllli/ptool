<template>
    <div id="app">
        <h1>发种🐔管理工具</h1>
        <h3>看明白再操作啊</h3>
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>版本信息 Version</span>
                <el-button style="float: right; padding: 3px 0" type="text" v-on:click="updateAppVersion">刷新</el-button>
            </div>
            <div style="white-space: pre-wrap">
                {{ version }}
            </div>
        </el-card>
        <el-divider></el-divider>
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>服务状态 Status</span>
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
                        <template slot="header" slot-scope="{}">
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
        <el-divider></el-divider>
        <el-card class="box-card">
            <div slot="header" class="clearfix">
                <span>版本更新 Update</span>
                <el-button style="float: right; padding: 3px 0" type="text" v-on:click="updateAppVersion">刷新</el-button>
            </div>
            <div>
                <div v-if="upload_pack_md5">
                    服务器上发现了安装包 <br/>
                    md5值： {{upload_pack_md5}} <br/>
                    请确认完全信赖安装包来源，并确认md5值匹配 <br/>
                    <el-button
                            size="huge"
                            type="danger"
                            v-bind:loading="updating"
                            @click="updateConfirm()">确认安装更新
                    </el-button>
                    <el-divider></el-divider>
                    当然也可以重新上传安装包
                </div>
                <div v-else>
                    服务器上没有安装包，请先上传
                </div>
                <el-upload
                        class="upload-demo"
                        drag
                        action="manager/update/upload"
                        :show-file-list=false
                        accept="application/zip"
                        :on-success="reloadUpdateFileInfo"
                >
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将安装包拖到此处，或<em>点击上传</em><br/>请务必上传从官方渠道获取的安装包</div>
                    <div class="el-upload__tip" slot="tip">多次上传时，以最后一个文件为准</div>
                </el-upload>

            </div>
        </el-card>

        <el-row>
            <div class="text-wrapper">
            </div>
        </el-row>
    </div>
</template>

<script>
    import {getAppStatus, getAppVersion, restartApp, updateFileInfo, updateConfirm} from '@/api/manager'

    export default {
        name: "Manager",
        data() {
            return {
                version: "123",
                app_status: [],
                all_app_restarting: false,
                updating: false,
                upload_pack_md5: ""
            }
        },
        mounted() {
            this.updateAppVersion()
            this.updateAppStatus()
            this.reloadUpdateFileInfo()
        },
        methods: {
            updateConfirm: function () {
                this.updating = true
                updateConfirm().then(resp => {
                    this.updating = false
                })
            },
            reloadUpdateFileInfo: function () {
                updateFileInfo().then(resp => {
                    if (resp.data.msg === 'ok') {
                        this.upload_pack_md5 = resp.data.info.md5
                    }
                })
            },
            restartAppFFFF: function (row_index, app_name) {
                let message = `全部服务重启完成`
                if (row_index !== undefined) {
                    this.app_status[row_index].restarting = true
                    message = `${app_name}服务重启完成`
                } else {
                    this.all_app_restarting = true
                }
                restartApp(app_name).then(() => {
                    this.$notify({
                        title: '提示',
                        message: message,
                        duration: 0
                    });
                    if (row_index !== undefined) {
                        this.app_status[row_index].restarting = false
                    } else {
                        this.all_app_restarting = false
                    }
                    this.updateAppStatus()
                })
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