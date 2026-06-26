const app = getApp()

Page({
  data: {
    banners: [
      { image: '/images/banner1.jpg', title: 'AI智能匹配' },
      { image: '/images/banner2.jpg', title: '真实评价' },
    ],
    categories: [
      { icon: '👶', name: '育儿嫂', type: '育儿嫂' },
      { icon: '🤱', name: '月嫂', type: '月嫂' },
      { icon: '🧹', name: '保洁', type: '保洁' },
      { icon: '👵', name: '养老护理', type: '养老护理' },
      { icon: '👨‍🍳', name: '做饭阿姨', type: '做饭' },
      { icon: '🏠', name: '住家管家', type: '管家' },
    ],
    companies: [],
    hotTags: ['高新区', '锦江区', '武侯区', '经验3年+', '薪资8000+'],
  },

  onLoad() {
    this.loadCompanies()
  },

  onPullDownRefresh() {
    this.loadCompanies(() => {
      wx.stopPullDownRefresh()
    })
  },

  loadCompanies(cb) {
    // 模拟数据
    const mockCompanies = [
      {
        id: 1, name: '和阳家政', rating: 4.9, orders: 1200,
        tags: ['育儿嫂', '月嫂', '保洁'],
        intro: '8年品牌家政，服务超过10000个家庭',
        image: '/images/company1.jpg',
        distance: '2.3km',
      },
      {
        id: 2, name: '安心家政', rating: 4.8, orders: 850,
        tags: ['育儿嫂', '养老护理'],
        intro: '专注高端家政，全部阿姨持证上岗',
        image: '/images/company2.jpg',
        distance: '3.5km',
      },
      {
        id: 3, name: '金牌月嫂中心', rating: 4.9, orders: 2000,
        tags: ['月嫂', '育儿嫂'],
        intro: '专业月嫂培训，金牌服务品质',
        image: '/images/company3.jpg',
        distance: '5.1km',
      },
    ]
    this.setData({ companies: mockCompanies })
    if (cb) cb()
  },

  onCategoryTap(e) {
    const type = e.currentTarget.dataset.type
    wx.navigateTo({
      url: `/pages/companies/companies?type=${type}`,
    })
  },

  onCompanyTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/company-detail/company-detail?id=${id}`,
    })
  },

  onPostTap() {
    wx.switchTab({ url: '/pages/post/post' })
  },

  onTagTap(e) {
    const tag = e.currentTarget.dataset.tag
    wx.showToast({ title: `筛选：${tag}`, icon: 'none' })
  },

  onSearchTap() {
    wx.navigateTo({ url: '/pages/companies/companies' })
  },
})
