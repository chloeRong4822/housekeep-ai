App({
  globalData: {
    apiBaseUrl: 'http://localhost:8000/api/v1/housekeeping',
    userInfo: null,
  },

  onLaunch() {
    console.log('小程序启动')
    // 检查登录状态
    const token = wx.getStorageSync('token')
    if (!token) {
      this.login()
    }
  },

  login() {
    wx.login({
      success: (res) => {
        if (res.code) {
          // 发送code到后端换取token
          console.log('wx.login code:', res.code)
          // wx.request({
          //   url: `${this.globalData.apiBaseUrl}/auth/wx-login`,
          //   method: 'POST',
          //   data: { code: res.code },
          //   success: (r) => {
          //     wx.setStorageSync('token', r.data.token)
          //   }
          // })
        }
      }
    })
  },

  getUserInfo() {
    return new Promise((resolve, reject) => {
      wx.getUserProfile({
        desc: '用于完善用户资料',
        success: (res) => {
          this.globalData.userInfo = res.userInfo
          resolve(res.userInfo)
        },
        fail: reject
      })
    })
  }
})
