Page({
  data: {
    companies: [],
    nannies: [],
    activeTab: 'company',
    filterType: '',
    filterArea: '',
    loading: false,
  },

  onLoad(options) {
    if (options.type) {
      this.setData({ filterType: options.type })
    }
    this.loadData()
  },

  loadData() {
    this.setData({ loading: true })
    setTimeout(() => {
      this.setData({
        companies: [
          { id: 1, name: '和阳家政', rating: 4.9, orders: 1200, tags: ['育儿嫂', '月嫂'], intro: '8年品牌家政', image: '', distance: '2.3km' },
          { id: 2, name: '安心家政', rating: 4.8, orders: 850, tags: ['育儿嫂', '养老护理'], intro: '专注高端家政', image: '', distance: '3.5km' },
        ],
        nannies: [
          { id: 1, name: '李阿姨', age: 45, origin: '四川绵阳', work_years: 8, skills: ['育儿嫂', '辅食'], salary_expect: 8000, image: '', rating: 4.9 },
          { id: 2, name: '王阿姨', age: 42, origin: '四川南充', work_years: 6, skills: ['月嫂', '催乳'], salary_expect: 12000, image: '', rating: 4.8 },
        ],
        loading: false,
      })
    }, 500)
  },

  onTabChange(e) {
    this.setData({ activeTab: e.currentTarget.dataset.tab })
  },

  onCompanyTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/company-detail/company-detail?id=${id}` })
  },
})
