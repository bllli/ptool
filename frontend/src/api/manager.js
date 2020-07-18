export function getAppStatus() {
    console.log(111)
    return window.axios({
        url: `manager/app/status`,
        method: 'get',
    })
}

export function getAppVersion() {
    console.log(111)
    return window.axios({
        url: `manager/app/version`,
        method: 'get',
    })
}

export function restartApp(appName) {
    let url = 'manager/app/restart'
    if (appName) {
        url = `manager/app/restart?process=${appName}`
    }
    return window.axios({
        url: url,
        method: 'get',
    })
}
