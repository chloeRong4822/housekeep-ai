<template>
  <div class="content-page">
    <!-- 生成配置 -->
    <div class="config-card">
      <div class="card-title"><el-icon><MagicStick /></el-icon> AI内容生成</div>
      <el-form :model="form" label-width="100px" class="config-form">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="平台">
              <el-select v-model="form.platform" placeholder="选择平台">
                <el-option label="小红书" value="xiaohongshu" />
                <el-option label="抖音" value="douyin" />
                <el-option label="朋友圈" value="wechat" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="内容类型">
              <el-select v-model="form.content_type" placeholder="选择类型">
                <el-option label="阿姨展示" value="nanny_show" />
                <el-option label="避坑指南" value="guide" />
                <el-option label="真实案例" value="case" />
                <el-option label="促销活动" value="promo" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="城市">
              <el-input v-model="form.city" placeholder="如：成都" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="服务类型">
              <el-select v-model="form.service_type" placeholder="选择服务">
                <el-option label="育儿嫂" value="育儿嫂" />
                <el-option label="月嫂" value="月嫂" />
                <el-option label="保洁" value="保洁" />
                <el-option label="养老护理" value="养老护理" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="风格">
              <el-select v-model="form.style" placeholder="选择风格">
                <el-option label="亲切友好" value="friendly" />
                <el-option label="专业权威" value="professional" />
                <el-option label="活泼有趣" value="lively" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="生成数量">
              <el-slider v-model="form.count" :min="1" :max="5" show-stops />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="核心卖点">
          <el-input v-model="form.selling_point" type="textarea" :rows="2" placeholder="描述你想突出的卖点，如：8年经验、0投诉、擅长辅食" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" :loading="generating" @click="generate">
            <el-icon><MagicStick /></el-icon> AI一键生成
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 生成结果 -->
    <div v-if="contents.length > 0" class="results">
      <div class="content-card" v-for="(item, idx) in contents" :key="idx">
        <div class="content-header">
          <div class="content-version">版本 {{ idx + 1 }}</div>
          <div class="content-actions">
            <el-button type="primary" size="small" @click="copy(item)"><el-icon><DocumentCopy /></el-icon> 复制</el-button>
            <el-button size="small" @click="publish(item)"><el-icon><Upload /></el-icon> 发布</el-button>
          </div>
        </div>
        <div class="content-body">
          <div class="content-section">
            <div class="section-label">标题</div>
            <div class="section-value title">{{ item.title }}</div>
          </div>
          <div class="content-section">
            <div class="section-label">正文</div>
            <div class="section-value body">{{ item.body }}</div>
          </div>
          <div class="content-section">
            <div class="section-label">配图建议</div>
            <div class="section-value">{{ item.image_desc }}</div>
          </div>
          <div class="content-section">
            <div class="section-label">话题标签</div>
            <el-tag v-for="tag in item.hashtags" :key="tag" class="tag">{{ tag }}</el-tag>
          </div>
          <div class="content-section">
            <div class="section-label">建议发布时间</div>
            <div class="section-value"><el-icon><Clock /></el-icon> {{ item.suggested_time }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 历史记录 -->
    <div class="history-card">
      <div class="card-title">历史生成记录</div>
      <el-table :data="history" style="width: 100%">
        <el-table-column prop="title" label="标题" show-overflow-tooltip />
        <el-table-column prop="platform" label="平台" width="100">
          <template #default="{row}">{{ platformName(row.platform) }}</template>
        </el-table-column>
        <el-table-column prop="likes" label="点赞" width="80" />
        <el-table-column prop="leads" label="转化" width="80" />
        <el-table-column prop="created_at" label="时间" width="160" />
        <el-table-column label="操作" width="120">
          <template #default="{row}">
            <el-button size="small" @click="copy(row)">复制</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  platform: 'xiaohongshu',
  content_type: 'nanny_show',
  city: '成都',
  service_type: '育儿嫂',
  style: 'friendly',
  count: 3,
  selling_point: '',
})

const generating = ref(false)
const contents = ref([])

const history = ref([
  { title: '成都宝妈注意！这个月嫂有8年经验...', platform: 'xiaohongshu', likes: 128, leads: 15, created_at: '2024-06-25 20:00' },
  { title: '面试育儿嫂必问的10个问题，第3个最关键', platform: 'xiaohongshu', likes: 256, leads: 32, created_at: '2024-06-24 18:30' },
  { title: '换了3个阿姨，终于遇到神仙育儿嫂！', platform: 'douyin', likes: 89, leads: 8, created_at: '2024-06-23 12:00' },
])

const generate = async () => {
  generating.value = true
  // 模拟AI生成
  setTimeout(() => {
    contents.value = [
      {
        title: '成都宝妈注意！这个月嫂有8年经验，带过30多个宝宝，0投诉！',
        body: '张女士生完二胎后，换了3个月嫂都不满意。后来通过平台找到了李阿姨...\n\n李阿姨有8年育儿经验，带过30多个宝宝，0投诉记录。她擅长辅食添加、睡眠训练、早教启蒙。\n\n雇主评价："李阿姨太专业了！宝宝原来夜醒3-4次，她来了1周就调整到睡整觉。每天还主动写喂养记录，让我上班也能知道宝宝情况。"',
        image_desc: '阿姨微笑照 + 宝宝互动照 + 辅食成品照',
        hashtags: ['#成都月嫂', '#月嫂推荐', '#新手妈妈', '#育儿嫂'],
        suggested_time: '20:00',
      },
      {
        title: '8年月嫂告诉你：面试时这3个问题一定要问！',
        body: '做了8年月嫂，我见过太多宝妈因为没问对问题，最后换了好几轮阿姨。\n\n今天分享面试时必问的3个问题：\n\n1. "您带过最小的宝宝是多大？" — 测试真实经验\n2. "宝宝哭闹不止时，您会怎么处理？" — 测试应变能力\n3. "您能接受我们每天沟通宝宝情况吗？" — 测试沟通意愿\n\n点赞收藏，需要的时候翻出来看！',
        image_desc: '阿姨面试场景 + 问题清单卡片',
        hashtags: ['#月嫂面试', '#育儿知识', '#新手妈妈避坑'],
        suggested_time: '12:00',
      },
      {
        title: '救命！成都这位育儿嫂治好了我的产后焦虑',
        body: '说实话，找阿姨之前我每天都很焦虑。怕宝宝照顾不好，怕阿姨不靠谱...\n\n直到遇到王阿姨。她不仅把宝宝照顾得很好，还每天陪我聊天，教我育儿知识。\n\n她说："宝妈心情好，宝宝才能好。"这句话让我特别感动。\n\n现在我已经离不开她了，打算续约到宝宝上幼儿园！',
        image_desc: '阿姨和宝妈聊天场景 + 宝宝笑脸照',
        hashtags: ['#成都育儿嫂', '#产后焦虑', '#神仙阿姨'],
        suggested_time: '21:00',
      },
    ]
    generating.value = false
    ElMessage.success('AI内容生成完成！')
  }, 2000)
}

const copy = (item) => {
  const text = `${item.title}\n\n${item.body}\n\n${item.hashtags?.join(' ') || ''}`
  navigator.clipboard.writeText(text)
  ElMessage.success('已复制到剪贴板')
}

const publish = (item) => {
  ElMessage.success('已添加到发布队列')
}

const platformName = (p) => {
  const map = { xiaohongshu: '小红书', douyin: '抖音', wechat: '朋友圈', zhihu: '知乎' }
  return map[p] || p
}
</script>

<style scoped>
.content-page { padding: 0; }
.config-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
}
.card-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-title .el-icon { color: #667eea; }
.config-form { max-width: 100%; }
.results {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}
.content-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.content-header {
  padding: 16px 20px;
  background: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.content-version {
  font-weight: bold;
  color: #667eea;
}
.content-body { padding: 20px; }
.content-section { margin-bottom: 16px; }
.section-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 6px;
}
.section-value.title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  line-height: 1.5;
}
.section-value.body {
  font-size: 14px;
  color: #555;
  line-height: 1.8;
  white-space: pre-line;
}
.tag { margin-right: 6px; margin-bottom: 6px; }
.history-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
}
@media (max-width: 1200px) {
  .results { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .results { grid-template-columns: 1fr; }
}
</style>
