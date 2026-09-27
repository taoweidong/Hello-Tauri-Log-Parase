<script setup lang="ts">
/**
 * 欢迎页组件
 * 无标签页打开时展示应用引导信息、操作提示、最近文件与快捷键说明
 */
import { computed } from 'vue'
import { usePanelLayout } from '@/composables/use-panel-layout'
import { useTabManager } from '@/composables/use-tabs'
import { APP_NAME, APP_DESCRIPTION } from '@/config'
import AppLogo from '@/components/shared/AppLogo.vue'
import AppIcon, { type AppIconName } from '@/components/shared/AppIcon.vue'

const { leftCollapsed, expandLeft } = usePanelLayout()
const { recentFiles } = useTabManager()

/** 欢迎页最近文件显示条数（C3：命名常量替代魔数字） */
const MAX_DISPLAY_RECENT = 5

/** 截取前 N 条最近文件，只显示文件名 */
const displayRecentFiles = computed(() => {
  return recentFiles.value.slice(0, MAX_DISPLAY_RECENT).map(path => {
    const parts = path.split(/[\\/]/)
    return parts[parts.length - 1] || path
  })
})

/** 引导卡片结构 */
interface GuideCard {
  icon: AppIconName
  title: string
  desc: string
  interactive: boolean
}

/** 操作提示卡片定义：图标 + 标题 + 描述 */
const guideCards = computed<GuideCard[]>(() => {
  const cards: GuideCard[] = [
    { icon: 'upload', title: '拖放文件', desc: '将压缩包拖放到窗口任意位置', interactive: false },
    { icon: 'folder', title: '上传文件', desc: '点击左侧面板上传区域选择文件', interactive: true },
    { icon: 'search', title: '搜索内容', desc: '使用顶部搜索栏或快捷键 Ctrl+K', interactive: false },
  ]
  if (displayRecentFiles.value.length > 0) {
    cards.push({ icon: 'clock', title: '最近文件', desc: '', interactive: false })
  }
  return cards
})
</script>

<template>
  <div class="flex-1 flex items-center justify-center bg-bg-base">
    <div class="flex flex-col items-center gap-6 px-8 py-12">

      <!-- 图标：入场第一拍 -->
      <div class="logo-shell animate-fade-in-up">
        <AppLogo class="w-10 h-10" />
      </div>

      <!-- 标题：第二拍 -->
      <div class="text-center animate-fade-in-up" style="animation-delay: 60ms;">
        <h2 class="text-[15px] font-bold text-text-primary mb-1">{{ APP_NAME }}</h2>
        <p class="text-[13px] text-text-secondary">{{ APP_DESCRIPTION }}</p>
      </div>

      <!-- 操作提示卡片：后续交错入场 -->
      <div class="flex flex-col gap-3 w-72">
        <template v-for="(card, idx) in guideCards" :key="card.title">
          <!-- 最近文件卡片（含文件列表） -->
          <div
            v-if="card.title === '最近文件'"
            class="guide-card animate-fade-in-up"
            :style="{ animationDelay: `${140 + idx * 70}ms` }"
          >
            <div class="guide-icon">
              <AppIcon :name="card.icon" :size="16" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-[13px] font-medium text-text-primary mb-1">最近文件</p>
              <div class="flex flex-col gap-0.5">
                <span v-for="(file, fIdx) in displayRecentFiles" :key="fIdx" class="text-[12px] text-text-secondary truncate">
                  {{ file }}
                </span>
              </div>
            </div>
          </div>

          <!-- 普通操作卡片 -->
          <div
            v-else
            class="guide-card animate-fade-in-up"
            :class="{ 'cursor-pointer': card.interactive }"
            :style="{ animationDelay: `${140 + idx * 70}ms` }"
            @click="card.interactive && leftCollapsed ? expandLeft() : undefined"
          >
            <div class="guide-icon">
              <AppIcon :name="card.icon" :size="16" />
            </div>
            <div>
              <p class="text-[13px] font-medium text-text-primary">{{ card.title }}</p>
              <p class="text-[12px] text-text-secondary">{{ card.desc }}</p>
            </div>
          </div>
        </template>
      </div>

      <!-- 快捷键提示：最后一拍 -->
      <div class="flex flex-wrap justify-center gap-2 text-[11px] text-text-disabled animate-fade-in-up" style="animation-delay: 420ms;">
        <kbd>Ctrl+B</kbd>
        <span>切换左侧面板</span>
        <kbd>Ctrl+Shift+B</kbd>
        <span>切换右侧面板</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Logo 容器：柔和品牌色底 */
.logo-shell {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  background: var(--color-primary-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
}

/* 引导卡片：交错入场 + hover 微上浮 */
.guide-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  transition: border-color var(--duration-base) var(--ease-out-quart),
              transform var(--duration-base) var(--ease-out-quart),
              box-shadow var(--duration-base) var(--ease-out-quart);
}
.guide-card:hover {
  border-color: color-mix(in srgb, var(--color-primary) 30%, transparent);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px -6px color-mix(in srgb, var(--color-text-primary) 12%, transparent);
}

/* 卡片内图标槽 */
.guide-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--color-primary-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  flex-shrink: 0;
}
</style>
