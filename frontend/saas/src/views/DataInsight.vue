<template>
  <div class="insight-page">
    <!-- 我的数据 -->
    <div class="section">
      <div class="section-title">我的数据</div>
      <div class="chart-row">
        <div class="chart-card">
          <div class="chart-title">线索量趋势</div>
          <v-chart class="chart" :option="leadTrendOption" autoresize />
        </div>
        <div class="chart-card">
          <div class="chart-title">转化率趋势</div>
          <v-chart class="chart" :option="conversionOption" autoresize />
        </div>
      </div>
    </div>

    <!-- 城市数据 -->
    <div class="section">
      <div class="section-title">城市数据</div>
      <div class="chart-row">
        <div class="chart-card">
          <div class="chart-title">各服务类型供需比</div>
          <v-chart class="chart" :option="supplyDemandOption" autoresize />
        </div>
        <div class="chart-card">
          <div class="chart-title">平均薪资趋势</div>
          <v-chart class="chart" :option="salaryOption" autoresize />
        </div>
      </div>
    </div>

    <!-- AI建议 -->
    <div class="section">
      <div class="section-title">AI智能建议</div>
      <div class="advice-list">
        <div class="advice-card" v-for="(advice, idx) in advices" :key="idx">
          <div class="advice-icon" :style="{background: advice.bg}">
            <el-icon><component :is="advice.icon" /></el-icon>
          </div>
          <div class="advice-content">
            <div class="advice-title">{{ advice.title }}</div>
            <div class="advice-desc">{{ advice.desc }}</div>
          </div>
          <el-button type="primary" size="small" plain @click="applyAdvice(advice)">立即行动</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, LineChart, BarChart, GridComponent, TooltipComponent, LegendComponent])

const leadTrendOption = ref({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
  yAxis: { type: 'value' },
  series: [{
    data: [120, 180, 250, 320, 400, 520],
    type: 'line',
    smooth: true,
    areaStyle: { color: 'rgba(102,126,234,0.2)' },
    lineStyle: { color: '#667eea', width: 3 },
  }]
})

const conversionOption = ref({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
  yAxis: { type: 'value', max: 30, axisLabel: { formatter: '{value}%' } },
  series: [{
    data: [8, 10, 12, 11, 14, 15.5],
    type: 'line',
    smooth: true,
    lineStyle: { color: '#11998e', width: 3 },
    itemStyle: { color: '#11998e' },
  }]
})

const supplyDemandOption = ref({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: ['育儿嫂', '月嫂', '保洁', '养老护理', '管家'] },
  yAxis: { type: 'value' },
  series: [
    { name: '需求', data: [85, 72, 60, 45, 30], type: 'bar', itemStyle: { color: '#667eea' } },
    { name: '供给', data: [70, 65, 80, 40, 25], type: 'bar', itemStyle: { color: '#67c23a' } },
  ]
})

const salaryOption = ref({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
  yAxis: { type: 'value' },
  series: [{
    name: '平均薪资',
    data: [7500, 7800, 8200, 8000, 8500, 8800],
    type: 'line',
    smooth: true,
    lineStyle: { color: '#fc4a1a', width: 3 },
    itemStyle: { color: '#fc4a1a' },
  }]
})

const advices = ref([
  {
    icon: 'TrendCharts',
    bg: '#667eea',
    title: '本月育儿嫂需求上涨30%',
    desc: '建议重点招募育儿嫂，目前高新区和锦江区缺口最大，可针对性投放招聘内容。',
  },
  {
    icon: 'Message',
    bg: '#11998e',
    title: '您的线索转化率低于同行',
    desc: '当前转化率12.5%，同行平均15%。建议优化跟进话术，AI已为您生成3套跟进模板。',
  },
  {
    icon: 'MapLocation',
    bg: '#fc4a1a',
    title: 'XX小区新生儿数量增加',
    desc: '数据显示XX小区本季度新生儿增加40%，建议在该区域投放育儿嫂内容。',
  },
  {
    icon: 'Star',
    bg: '#764ba2',
    title: '王阿姨被收藏次数最多',
    desc: '王阿姨本周被雇主收藏15次，建议将其置顶推荐，并为其拍摄更专业的展示视频。',
  },
])

const applyAdvice = (advice) => {
  // 模拟行动
}
</script>

<style scoped>
.section { margin-bottom: 24px; }
.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 16px;
}
.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.chart-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 12px;
}
.chart { height: 260px; }
.advice-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.advice-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.advice-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  flex-shrink: 0;
}
.advice-content { flex: 1; }
.advice-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
}
.advice-desc {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}
@media (max-width: 768px) {
  .chart-row { grid-template-columns: 1fr; }
  .advice-list { grid-template-columns: 1fr; }
}
</style>
