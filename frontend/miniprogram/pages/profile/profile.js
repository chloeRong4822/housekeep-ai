Page({
  data: {
    userInfo: null,
    myPosts: [
      { id: 1, service_type: '育儿嫂', status: '已匹配', statusText: '已匹配3家家政公司', ai_score: 87, created_at: '2024-06-26 10:30' },
      { id: 2, service_type: '保洁', status: '已完成', statusText: '已找到合适阿姨', ai_score: 72, created_at: '2024-06-20 14:15' },
    ],
    favorites: [
      { id: 1, name: '和阳家政', tags: ['育儿嫂', '月嫂'] },
    ],
  },

  onLoad() {
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.setData({ userInfo })
    }
  },

  onGetUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        wx.setStorageSync('userInfo', res.userInfo)
        this.setData({ userInfo: res.userInfo })
      }
    })
  },

  onPostTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/post/post?id=${id}` })
  },

  onContactTap(e) {
    const company = e.currentTarget.dataset.company
    wx.makePhoneCall({ phoneNumber: '400-888-8888' })
  },
})
