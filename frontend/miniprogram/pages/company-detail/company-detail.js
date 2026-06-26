Page({
  data: {
    company: {},
    nannies: [],
    reviews: [],
    activeTab: 'nannies',
  },

  onLoad(options) {
    const id = options.id
    this.loadCompanyDetail(id)
  },

  loadCompanyDetail(id) {
    // 模拟数据
    this.setData({
      company: {
        id: id,
        name: '和阳家政',
        rating: 4.9,
        orders: 1200,
        tags: ['育儿嫂', '月嫂', '保洁'],
        intro: '8年品牌家政，服务超过10000个家庭。所有阿姨持证上岗，提供背景调查、健康体检、技能认证三重保障。',
        service_areas: ['高新区', '锦江区', '武侯区', '成华区'],
        phone: '400-888-8888',
      },
      nannies: [
        { id: 1, name: '李阿姨', age: 45, work_years: 8, skills: ['育儿嫂', '辅食', '早教'], salary_expect: 8000, rating: 4.9, service_count: 32 },
        { id: 2, name: '王阿姨', age: 42, work_years: 6, skills: ['月嫂', '催乳'], salary_expect: 12000, rating: 4.8, service_count: 28 },
        { id: 3, name: '张阿姨', age: 38, work_years: 4, skills: ['保洁', '收纳'], salary_expect: 4500, rating: 4.7, service_count: 45 },
      ],
      reviews: [
        { user: '张女士', rating: 5, content: '李阿姨太专业了！宝宝照顾得很好，每天还主动写喂养记录。', date: '2024-06-20' },
        { user: '李先生', rating: 5, content: '服务很到位，阿姨准时到，做事认真。', date: '2024-06-18' },
      ],
    })
  },

  onTabChange(e) {
    this.setData({ activeTab: e.currentTarget.dataset.tab })
  },

  onPhoneTap() {
    wx.makePhoneCall({ phoneNumber: this.data.company.phone })
  },
})
