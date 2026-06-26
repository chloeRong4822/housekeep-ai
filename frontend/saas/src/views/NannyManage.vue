<template>
  <div class="nanny-page">
    <div class="page-header">
      <el-button type="primary" @click="dialogVisible = true">
        <el-icon><Plus /></el-icon> 添加阿姨
      </el-button>
    </div>

    <div class="nanny-grid">
      <div class="nanny-card" v-for="nanny in nannies" :key="nanny.id">
        <div class="nanny-avatar">
          <img :src="nanny.avatar || '/default-avatar.png'" alt="avatar" />
          <div class="status-badge" :class="'status-' + nanny.status">
            {{ statusText(nanny.status) }}
          </div>
        </div>
        <div class="nanny-info">
          <div class="nanny-name">{{ nanny.name }}</div>
          <div class="nanny-meta">{{ nanny.age }}岁 · {{ nanny.origin }} · {{ nanny.work_years }}年经验</div>
          <div class="nanny-tags">
            <el-tag v-for="skill in nanny.skills" :key="skill" size="small" type="info">{{ skill }}</el-tag>
          </div>
          <div class="nanny-salary">期望薪资：¥{{ nanny.salary_expect }}/月</div>
          <div class="nanny-scores">
            <div class="score-item">
              <div class="score-label">技能</div>
              <div class="score-value">{{ nanny.skill_score }}</div>
            </div>
            <div class="score-item">
              <div class="score-label">稳定</div>
              <div class="score-value">{{ nanny.stability_score }}</div>
            </div>
            <div class="score-item">
              <div class="score-label">服务</div>
              <div class="score-value">{{ nanny.service_score }}</div>
            </div>
          </div>
          <div class="nanny-actions">
            <el-button type="primary" size="small" @click="optimizeResume(nanny)">AI简历优化</el-button>
            <el-button size="small" @click="editNanny(nanny)">编辑</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- AI简历优化弹窗 -->
    <el-dialog v-model="optimizeDialog" title="AI简历优化" width="600px">
      <div v-if="optimized">
        <div class="optimize-original">
          <div class="optimize-label">原始简历</div>
          <div class="optimize-text">{{ selectedNanny?.original_resume }}</div>
        </div>
        <div class="optimize-arrow"><el-icon><ArrowDown /></el-icon></div>
        <div class="optimize-result">
          <div class="optimize-label">AI优化版</div>
          <div class="optimize-text optimized">{{ optimizedText }}</div>
        </div>
        <div class="optimize-versions">
          <el-radio-group v-model="selectedVersion">
            <el-radio-button label="v1">版本1</el-radio-button>
            <el-radio-button label="v2">版本2</el-radio-button>
            <el-radio-button label="v3">版本3</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div v-else class="optimize-loading">
        <el-icon class="loading-icon"><Loading /></el-icon>
        <p>AI正在优化简历...请稍候</p>
      </div>
      <template #footer>
        <el-button @click="optimizeDialog = false">关闭</el-button>
        <el-button type="primary" @click="useOptimized">采用此版本</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const dialogVisible = ref(false)
const optimizeDialog = ref(false)
const optimizing = ref(false)
const optimized = ref(false)
const selectedVersion = ref('v1')
const selectedNanny = ref(null)
const optimizedText = ref('')

const nannies = ref([
  {
    id: 1, name: '李阿姨', age: 45, origin: '四川绵阳', work_years: 8,
    skills: ['育儿嫂', '辅食', '早教'], salary_expect: 8000,
    status: 0, skill_score: 92, stability_score: 88, service_score: 90,
    original_resume: '做了5年育儿嫂，带过几个宝宝，经验丰富。',
  },
  {
    id: 2, name: '王阿姨', age: 42, origin: '四川南充', work_years: 6,
    skills: ['月嫂', '催乳', '月子餐'], salary_expect: 12000,
    status: 1, skill_score: 95, stability_score: 90, service_score: 93,
    original_resume: '6年月嫂经验，带过20多个宝宝。',
  },
  {
    id: 3, name: '张阿姨', age: 38, origin: '四川成都', work_years: 4,
    skills: ['保洁', '收纳', '做饭'], salary_expect: 4500,
    status: 0, skill_score: 85, stability_score: 82, service_score: 88,
    original_resume: '4年保洁经验，做事认真。',
  },
  {
    id: 4, name: '陈阿姨', age: 50, origin: '四川泸州', work_years: 10,
    skills: ['养老护理', '康复', '陪护'], salary_expect: 6000,
    status: 0, skill_score: 90, stability_score: 92, service_score: 89,
    original_resume: '10年养老护理经验，照顾过多位老人。',
  },
])

const statusText = (s) => {
  const map = { 0: '待岗', 1: '上户', 2: '休假' }
  return map[s] || '未知'
}

const optimizeResume = (nanny) => {
  selectedNanny.value = nanny
  optimizeDialog.value = true
  optimized.value = false
  setTimeout(() => {
    optimized.value = true
    optimizedText.value = `【成都金牌${nanny.skills[0]}】${nanny.work_years}年专注${nanny.skills[0]}服务，带过${nanny.work_years * 4}+个家庭，0投诉记录\n\n✅ ${nanny.skills.join('、')}全掌握\n✅ 持国家认证证书上岗\n✅ 前雇主好评率100%\n✅ 服务稳定，平均服务时长18个月\n\n雇主评价："${nanny.name}太专业了！不仅把宝宝/老人照顾得很好，还特别细心，我们全家都很满意。"\n\n👉 想找${nanny.skills[0]}的雇主，强烈推荐！`
  }, 1500)
}

const useOptimized = () => {
  ElMessage.success('已采用AI优化版简历')
  optimizeDialog.value = false
}

const editNanny = (nanny) => {
  ElMessage.info(`编辑 ${nanny.name} 的信息`)
}
</script>

<style scoped>
.page-header { margin-bottom: 20px; }
.nanny-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.nanny-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.nanny-avatar {
  position: relative;
  height: 200px;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
}
.nanny-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  color: #fff;
}
.status-0 { background: #67c23a; }
.status-1 { background: #e6a23c; }
.status-2 { background: #909399; }
.nanny-info { padding: 16px; }
.nanny-name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 4px;
}
.nanny-meta {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}
.nanny-tags { margin-bottom: 8px; }
.nanny-tags .el-tag { margin-right: 4px; margin-bottom: 4px; }
.nanny-salary {
  font-size: 14px;
  color: #f56c6c;
  font-weight: bold;
  margin-bottom: 12px;
}
.nanny-scores {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}
.score-item { text-align: center; }
.score-label { font-size: 12px; color: #999; }
.score-value { font-size: 18px; font-weight: bold; color: #667eea; }
.nanny-actions {
  display: flex;
  gap: 8px;
}
.optimize-original, .optimize-result {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 12px;
}
.optimize-text {
  font-size: 14px;
  color: #555;
  line-height: 1.8;
  white-space: pre-line;
}
.optimize-text.optimized {
  color: #333;
  font-weight: 500;
}
.optimize-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}
.optimize-arrow {
  text-align: center;
  color: #667eea;
  font-size: 24px;
  margin: 12px 0;
}
.optimize-loading {
  text-align: center;
  padding: 40px;
}
.loading-icon {
  font-size: 48px;
  color: #667eea;
  animation: rotate 1s linear infinite;
}
@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.optimize-versions { margin-top: 16px; text-align: center; }
@media (max-width: 1200px) { .nanny-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .nanny-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
