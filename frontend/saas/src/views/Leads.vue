<template>
  <div class="leads-page">
    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-select v-model="filter.level" placeholder="AI评分" clearable style="width: 120px">
        <el-option label="高意向" value="high" />
        <el-option label="中意向" value="medium" />
        <el-option label="低意向" value="low" />
      </el-select>
      <el-select v-model="filter.service_type" placeholder="服务类型" clearable style="width: 120px">
        <el-option label="育儿嫂" value="育儿嫂" />
        <el-option label="月嫂" value="月嫂" />
        <el-option label="保洁" value="保洁" />
        <el-option label="养老护理" value="养老护理" />
      </el-select>
      <el-input v-model="filter.city" placeholder="城市" clearable style="width: 150px" />
      <el-button type="primary" @click="fetchLeads"><el-icon><Search /></el-icon> 筛选</el-button>
      <el-button @click="resetFilter">重置</el-button>
    </div>

    <!-- 线索列表 -->
    <div class="table-card">
      <el-table :data="leads" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="employer_name" label="雇主" width="100" />
        <el-table-column prop="employer_phone" label="电话" width="140">
          <template #default="{row}">{{ maskPhone(row.employer_phone) }}</template>
        </el-table-column>
        <el-table-column prop="service_type" label="服务类型" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="district" label="区域" width="120" />
        <el-table-column prop="budget_max" label="预算" width="120">
          <template #default="{row}"><span v-if="row.budget_max">¥{{ row.budget_max }}</span><span v-else>-</span></template>
        </el-table-column>
        <el-table-column prop="ai_score" label="AI评分" width="100">
          <template #default="{row}">
            <el-tag :type="scoreTagType(row.ai_score)" size="small">
              {{ row.ai_score }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ai_reason" label="评分理由" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{row}">
            <el-tag :type="statusType(row.status)">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{row}">
            <el-button type="primary" size="small" @click="contact(row)">联系</el-button>
            <el-button size="small" @click="viewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchLeads"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const leads = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(100)

const filter = reactive({
  level: '',
  service_type: '',
  city: '',
})

const mockLeads = [
  { id: 1001, employer_name: '张女士', employer_phone: '138****8000', service_type: '育儿嫂', city: '成都', district: '高新区', budget_max: 9000, ai_score: 92, ai_reason: '评分92分（高意向）。主要依据：+15:有预算；+20:预算充足；+10:有详细地址；+15:紧急需求；+10:有微信号', status: 1, created_at: '2024-06-26 10:30' },
  { id: 1002, employer_name: '李先生', employer_phone: '139****6000', service_type: '月嫂', city: '成都', district: '锦江区', budget_max: 12000, ai_score: 88, ai_reason: '评分88分（高意向）。主要依据：+15:有预算；+20:预算充足；+15:有期望时间；+10:有微信号', status: 1, created_at: '2024-06-26 09:15' },
  { id: 1003, employer_name: '王女士', employer_phone: '136****2000', service_type: '保洁', city: '成都', district: '武侯区', budget_max: 3500, ai_score: 75, ai_reason: '评分75分（中意向）。主要依据：+15:有预算；+10:有详细地址；+5:有姓名；+10:有家庭信息', status: 0, created_at: '2024-06-26 08:45' },
  { id: 1004, employer_name: '赵先生', employer_phone: '137****9000', service_type: '育儿嫂', city: '成都', district: '成华区', budget_max: 8000, ai_score: 82, ai_reason: '评分82分（高意向）。主要依据：+15:有预算；+20:预算充足；+10:有区域；+15:有期望时间', status: 0, created_at: '2024-06-25 20:10' },
  { id: 1005, employer_name: '陈女士', employer_phone: '135****5000', service_type: '养老护理', city: '成都', district: '金牛区', budget_max: 6000, ai_score: 68, ai_reason: '评分68分（中意向）。主要依据：+15:有预算；+10:有区域；+10:有偏好', status: 0, created_at: '2024-06-25 18:30' },
  { id: 1006, employer_name: '周先生', employer_phone: '133****7000', service_type: '育儿嫂', city: '成都', district: '高新区', budget_max: 8500, ai_score: 90, ai_reason: '评分90分（高意向）。主要依据：+15:有预算；+20:预算充足；+10:有详细地址；+15:紧急需求；+10:有微信号；+10:有偏好', status: 1, created_at: '2024-06-25 16:20' },
]

const fetchLeads = () => {
  loading.value = true
  setTimeout(() => {
    leads.value = mockLeads
    loading.value = false
  }, 500)
}

const resetFilter = () => {
  filter.level = ''
  filter.service_type = ''
  filter.city = ''
  fetchLeads()
}

const scoreTagType = (score) => {
  if (score >= 80) return 'success'
  if (score >= 50) return 'warning'
  return 'info'
}

const statusType = (status) => {
  const map = { 0: 'info', 1: 'primary', 2: 'success', 3: 'danger' }
  return map[status] || 'info'
}

const statusText = (status) => {
  const map = { 0: '待分发', 1: '已分发', 2: '已成交', 3: '已失效' }
  return map[status] || '未知'
}

const maskPhone = (phone) => {
  if (!phone || phone.length < 11) return phone
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

const contact = (row) => {
  ElMessage.success(`正在联系 ${row.employer_name}，扣除线索费 ¥80`)
}

const viewDetail = (row) => {
  ElMessage.info(`查看线索 #${row.id} 详情`)
}

onMounted(fetchLeads)
</script>

<style scoped>
.leads-page { padding: 0; }
.filter-bar {
  background: #fff;
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
  align-items: center;
}
.table-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
