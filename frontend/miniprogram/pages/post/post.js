Page({
  data: {
    step: 1,
    form: {
      service_type: '',
      service_form: '住家',
      city: '成都',
      district: '',
      budget_min: '',
      budget_max: '',
      family_size: '',
      baby_age: '',
      has_pet: false,
      urgency: 0,
      employer_name: '',
      employer_phone: '',
    },
    serviceTypes: ['育儿嫂', '月嫂', '保洁', '养老护理', '做饭', '管家'],
    serviceForms: ['住家', '白班', '钟点'],
    districts: ['高新区', '锦江区', '武侯区', '成华区', '金牛区', '青羊区'],
    questions: [
      { field: 'service_type', text: '您需要什么服务？', type: 'select', options: 'serviceTypes' },
      { field: 'service_form', text: '服务形式？', type: 'select', options: 'serviceForms' },
      { field: 'district', text: '您在哪个区域？', type: 'select', options: 'districts' },
      { field: 'budget_max', text: '您的预算是多少？', type: 'input', placeholder: '如：8000', unit: '元/月' },
      { field: 'family_size', text: '家里几口人？', type: 'input', placeholder: '如：3' },
      { field: 'baby_age', text: '宝宝多大了？（没有填0）', type: 'input', placeholder: '如：6' },
      { field: 'has_pet', text: '家里有宠物吗？', type: 'switch' },
      { field: 'urgency', text: '有多急？', type: 'radio', options: [{label:'不急',value:0},{label:'一般',value:1},{label:'很急',value:2}] },
      { field: 'employer_name', text: '怎么称呼您？', type: 'input', placeholder: '如：张女士' },
      { field: 'employer_phone', text: '您的手机号？', type: 'input', placeholder: '13800138000' },
    ],
    currentQuestion: {},
    totalSteps: 10,
  },

  onLoad() {
    this.showQuestion(0)
  },

  showQuestion(index) {
    const question = this.data.questions[index]
    this.setData({
      step: index + 1,
      currentQuestion: question,
    })
  },

  onSelect(e) {
    const { field } = this.data.currentQuestion
    const value = e.currentTarget.dataset.value
    this.setData({ [`form.${field}`]: value })
    this.nextStep()
  },

  onInput(e) {
    const { field } = this.data.currentQuestion
    const value = e.detail.value
    this.setData({ [`form.${field}`]: value })
  },

  onSwitchChange(e) {
    const { field } = this.data.currentQuestion
    this.setData({ [`form.${field}`]: e.detail.value })
  },

  onRadioChange(e) {
    const { field } = this.data.currentQuestion
    this.setData({ [`form.${field}`]: parseInt(e.detail.value) })
  },

  nextStep() {
    const nextIndex = this.data.step
    if (nextIndex < this.data.totalSteps) {
      this.showQuestion(nextIndex)
    } else {
      this.submit()
    }
  },

  submit() {
    const { form } = this.data
    wx.showLoading({ title: 'AI匹配中...' })

    // 模拟提交
    setTimeout(() => {
      wx.hideLoading()
      wx.showModal({
        title: '发布成功',
        content: `AI已为您分析需求，匹配度评分87分（高意向）。\n\n预计3家家政公司将在10分钟内联系您。`,
        showCancel: false,
        success: () => {
          wx.switchTab({ url: '/pages/profile/profile' })
        }
      })
    }, 2000)
  },

  goBack() {
    if (this.data.step > 1) {
      this.showQuestion(this.data.step - 2)
    }
  },
})
