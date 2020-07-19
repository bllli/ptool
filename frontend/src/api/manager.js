export function getAppStatus() {
    return window.axios({
        url: `manager/app/status`,
        method: 'get',
    })
}

export function getAppVersion() {
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

export function updateFileInfo() {
    return window.axios({
        url: `manager/update/check`,
        method: 'get',
    })
}

export function updateConfirm() {
    return window.axios({
        url: `manager/update/confirm`,
        method: 'get',
    })
}

