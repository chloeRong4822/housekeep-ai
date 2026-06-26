<template>
  <div class="dashboard">
    <!-- 数据卡 -->
    <div class="stat-cards">
      <div class="stat-card" v-for="item in stats" :key="item.label">
        <div class="stat-icon" :style="{background: item.bg}">
          <el-icon><component :is="item.icon" /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ item.value }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </div>
      </div>
    </div>

    <!-- 图表区 -->
    <div class="chart-row">
      <div class="chart-card">
        <div class="chart-title">近7日线索趋势</div>
        <v-chart class="chart" :option="trendOption" autoresize />
      </div>
      <div class="chart-card">
        <div class="chart-title">线索意向分布</div>
        <v-chart class="chart" :option="pieOption" autoresize />
      </div>
    </div>

    <!-- 最新线索 -->
    <div class="table-card">
      <div class="table-header">
        <span class="table-title">最新高意向线索</span>
        <el-button type="primary" size="small" @click="$router.push('/leads')">查看全部</el-button>
      </div>
      <el-table :data="recentLeads" style="width: 100%">
        <el-table-column prop="employer_name" label="雇主" width="120" />
        <el-table-column prop="service_type" label="需求类型" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="budget_max" label="预算" width="120">
          <template #default="{row}"><span>{{ row.budget_max ? '¥' + row.budget_max : '-' }}</span></template>
        </el-table-column>
        <el-table-column prop="ai_score" label="AI评分" width="100">
          <template #default="{row}">
            <el-tag :type="row.ai_score >= 80 ? 'success' : row.ai_score >= 50 ? 'warning' : 'info'">
              {{ row.ai_score }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" />
        <el-table-column label="操作" width="120">
          <template #default="{row}">
            <el-button type="primary" size="small" @click="contact(row)">联系</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, LineChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

const stats = ref([
  { label: '今日新线索', value: 35, icon: 'Document', bg: '#667eea' },
  { label: '本周线索', value: 210, icon: 'Calendar', bg: '#764ba2' },
  { label: '累计成交', value: 128, icon: 'CircleCheck', bg: '#11998e' },
  { label: '转化率', value: '12.5%', icon: 'TrendCharts', bg: '#fc4a1a' },
])

const trendOption = ref({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
  yAxis: { type: 'value' },
  series: [{
    data: [28, 35, 42, 38, 45, 52, 35],
    type: 'line',
    smooth: true,
    areaStyle: { color: 'rgba(102,126,234,0.2)' },
    lineStyle: { color: '#667eea', width: 3 },
    itemStyle: { color: '#667eea' },
  }]
})

const pieOption = ref({
  tooltip: { trigger: 'item' },
  legend: { bottom: '0%' },
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],
    data: [
      { value: 45, name: '高意向', itemStyle: { color: '#67c23a' } },
      { value: 35, name: '中意向', itemStyle: { color: '#e6a23c' } },
      { value: 20, name: '低意向', itemStyle: { color: '#909399' } },
    ],
  }]
})

const recentLeads = ref([])

onMounted(() => {
  // 模拟数据
  recentLeads.value = [
    { employer_name: '张女士', service_type: '育儿嫂', city: '成都', district: '高新区', budget_max: 9000, ai_score: 92, created_at: '2024-06-26 10:30' },
    { employer_name: '李先生', service_type: '月嫂', city: '成都', district: '锦江区', budget_max: 12000, ai_score: 88, created_at: '2024-06-26 09:15' },
    { employer_name: '王女士', service_type: '保洁', city: '成都', district: '武侯区', budget_max: 3500, ai_score: 75, created_at: '2024-06-26 08:45' },
    { employer_name: '赵先生', service_type: '育儿嫂', city: '成都', district: '成华区', budget_max: 8000, ai_score: 82, created_at: '2024-06-25 20:10' },
    { employer_name: '陈女士', service_type: '养老护理', city: '成都', district: '金牛区', budget_max: 6000, ai_score: 68, created_at: '2024-06-25 18:30' },
  ]
})

const contact = (row) => {
  // 模拟联系
}
</script>

<style scoped>
.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
}
.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}
.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}
.chart-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.chart-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
}
.chart {
  height: 280px;
}
.table-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.table-title {
  font-size: 16px;
  font-weight: bold;
}
</style>
