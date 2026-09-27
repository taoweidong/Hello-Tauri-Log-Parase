<script setup lang="ts">
/**
 * 应用主布局组件
 * 实现四栏布局：顶部导航栏 + 左侧归档面板 + 中央工作区 + 右侧属性面板
 * 包含面板拖拽调整宽度、键盘快捷键、全局拖放上传、主题色切换等功能
 */
import { ref, computed, h, onMounted, onBeforeUnmount } from 'vue'
import { NButton, NTooltip, NDropdown } from 'naive-ui'
import type { DropdownOption } from 'naive-ui'
import { useMagicKeys, whenever } from '@vueuse/core'
import { useAppStore } from '@/stores/app'
import { useGlobalDrop } from '@/composables/use-global-drop'
import { usePanelLayout } from '@/composables/use-panel-layout'
import { themeColors, type ThemeColorKey } from '@/styles/theme'
import {
  MIN_LEFT_PANEL_WIDTH,
  MAX_LEFT_PANEL_WIDTH,
  MIN_RIGHT_PANEL_WIDTH,
  MAX_RIGHT_PANEL_WIDTH,
  APP_NAME,
  APP_BADGE,
  SITE_LINKS,
} from '@/config'
import PublicBar from '@/components/public-bar/PublicBar.vue'
import ArchivePanel from '@/components/archive-panel/ArchivePanel.vue'
import Workspace from '@/components/workspace/Workspace.vue'
import PropertyPanel from '@/components/property-panel/PropertyPanel.vue'
import GlobalStatusBar from '@/components/workspace/StatusBar.vue'
import AppLogo from '@/components/shared/AppLogo.vue'
import AppIcon, { type AppIconName } from '@/components/shared/AppIcon.vue'
import { themeColorLabels } from '@/styles/theme'

const store = useAppStore()
const { leftCollapsed, rightCollapsed, leftWidth, rightWidth, collapseLeft, expandLeft, collapseRight, expandRight, toggleLeft, toggleRight, setLeftWidth, setRightWidth } = usePanelLayout()

// ── 键盘快捷键（必须在组件 setup 中注册，useMagicKeys 需要事件上下文） ──
const keys = useMagicKeys()
whenever(keys['Ctrl+B'], (v) => {
  if (v) toggleLeft()
})
whenever(keys['Ctrl+Shift+B'], (v) => {
  if (v) toggleRight()
})

// ── 面板拖拽调整宽度 ──
const draggingLeft = ref(false)
const draggingRight = ref(false)

/** 开始拖拽指定侧边栏，设置全局光标样式 */
function startDrag(side: 'left' | 'right', e: MouseEvent) {
  const collapsed = side === 'left' ? leftCollapsed.value : rightCollapsed.value
  if (collapsed) return
  if (side === 'left') draggingLeft.value = true
  else draggingRight.value = true
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'
  e.preventDefault()
}

/** 鼠标移动时实时更新面板宽度 */
function onMouseMove(e: MouseEvent) {
  if (draggingLeft.value) {
    const newWidth = Math.max(MIN_LEFT_PANEL_WIDTH, Math.min(MAX_LEFT_PANEL_WIDTH, e.clientX))
    setLeftWidth(newWidth)
  }
  if (draggingRight.value) {
    const newWidth = Math.max(MIN_RIGHT_PANEL_WIDTH, Math.min(MAX_RIGHT_PANEL_WIDTH, window.innerWidth - e.clientX))
    setRightWidth(newWidth)
  }
}

/** 停止拖拽，恢复光标与选择样式 */
function stopDrag() {
  if (draggingLeft.value || draggingRight.value) {
    draggingLeft.value = false
    draggingRight.value = false
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
  }
}

// 全局拖拽事件
onMounted(() => {
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', stopDrag)
})
onBeforeUnmount(() => {
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', stopDrag)
})

// ── 全局拖放处理 ──
const appShellRef = ref<HTMLElement | null>(null)
const { isDragging, setup: setupDrop, cleanup: cleanupDrop } = useGlobalDrop()

onMounted(() => {
  if (appShellRef.value) setupDrop(appShellRef.value)
})
onBeforeUnmount(() => {
  cleanupDrop()
})

// ── 帮助菜单 ──
const helpOptions: DropdownOption[] = [
  {
    key: 'github',
    label: () =>
      h('a', {
        href: SITE_LINKS.github,
        target: '_blank',
        rel: 'noopener noreferrer',
        class: 'flex items-center gap-2 text-text-primary no-underline hover:text-primary transition-colors'
      }, [
        h(AppIcon, { name: 'github' as AppIconName, size: 16 }),
        h('span', 'GitHub 仓库')
      ])
  },
  {
    key: 'issue',
    label: () =>
      h('a', {
        href: SITE_LINKS.issue,
        target: '_blank',
        rel: 'noopener noreferrer',
        class: 'flex items-center gap-2 text-text-primary no-underline hover:text-primary transition-colors'
      }, [
        h(AppIcon, { name: 'issue' as AppIconName, size: 16 }),
        h('span', '问题反馈')
      ])
  }
]

// ── 主题色切换 ──
const currentThemeColor = ref<ThemeColorKey>('blue')
/** 主题色下拉项：色点 + 名称 */
const themeColorOptions: DropdownOption[] = (Object.keys(themeColors) as ThemeColorKey[]).map(key => ({
  key,
  label: () =>
    h('span', { class: 'flex items-center gap-2' }, [
      h('span', {
        class: 'inline-block w-3 h-3 rounded-full shrink-0 border border-black/10',
        style: { background: themeColors[key], boxShadow: `0 0 0 3px color-mix(in srgb, ${themeColors[key]} 20%, transparent)` }
      }),
      h('span', themeColorLabels[key])
    ])
}))
/** 批量设置 CSS 自定义属性 */
function setCssVars(vars: Record<string, string>) {
  const style = document.documentElement.style
  for (const [prop, value] of Object.entries(vars)) {
    style.setProperty(prop, value)
  }
}

/** 处理主题色选择，更新 CSS 自定义属性 */
function handleThemeColorSelect(key: string) {
  currentThemeColor.value = key as ThemeColorKey
  const color = themeColors[key as ThemeColorKey]
  setCssVars({
    '--color-primary': color,
    '--color-primary-soft': `color-mix(in srgb, ${color} 14%, transparent)`,
    '--color-primary-hover': color,
  })
}
</script>

<template>
  <div ref="appShellRef" class="absolute inset-0 grid grid-rows-[var(--spacing-header)_1fr_var(--spacing-statusbar)] bg-bg-base text-text-primary overflow-hidden" :data-theme="store.isDarkTheme ? 'dark' : 'light'">
    
    <!-- ═══════════ 顶部导航栏 48px ═══════════ -->
    <header class="flex items-center gap-4 px-4 h-header bg-bg-surface/85 backdrop-blur-md border-b border-border z-10 select-none">
      <!-- 左侧：Logo + 名称 + 徽章 -->
      <div class="flex items-center gap-2.5 shrink-0">
        <div class="w-[26px] h-[26px] flex items-center justify-center text-primary" style="filter: drop-shadow(0 0 6px color-mix(in srgb, var(--color-primary) 40%, transparent))"><AppLogo /></div>
        <span class="text-[15px] font-bold tracking-[0.3px] bg-gradient-to-r from-primary to-[color-mix(in_srgb,var(--color-primary)_60%,#94a3b8)] bg-clip-text text-transparent">{{ APP_NAME }}</span>
        <span class="text-[11px] px-2 py-0.5 rounded-[10px] bg-primary-soft text-primary font-medium tracking-[0.2px]">{{ APP_BADGE }}</span>
      </div>

      <!-- 中央：PublicBar -->
      <div class="flex-1 min-w-0 h-full flex items-center">
        <PublicBar />
      </div>

      <!-- 右侧：帮助 + 主题色 + 主题切换 -->
      <div class="flex items-center gap-3 shrink-0">

        <!-- 帮助下拉菜单 -->
        <NDropdown trigger="hover" :options="helpOptions" placement="bottom-end">
          <NButton quaternary circle class="!w-8 !h-8" aria-label="帮助">
            <AppIcon name="help" :size="18" />
          </NButton>
        </NDropdown>

        <!-- 主题色选择器 -->
        <NDropdown trigger="click" :options="themeColorOptions" placement="bottom-end" @select="handleThemeColorSelect">
          <NButton quaternary circle class="!w-8 !h-8" aria-label="主题色">
            <span class="inline-block w-3.5 h-3.5 rounded-full" :style="{ background: themeColors[currentThemeColor] }"></span>
          </NButton>
        </NDropdown>

        <!-- 主题切换按钮 -->
        <NTooltip trigger="hover">
          <template #trigger>
            <NButton quaternary circle class="!w-8 !h-8" @click="store.toggleTheme">
              <Transition name="icon-spin" mode="out-in">
                <span v-if="store.isDarkTheme" key="moon" class="inline-flex">
                  <AppIcon name="moon" :size="16" />
                </span>
                <span v-else key="sun" class="inline-flex">
                  <AppIcon name="sun" :size="16" />
                </span>
              </Transition>
            </NButton>
          </template>
          {{ store.isDarkTheme ? '切换浅色模式' : '切换深色模式' }}
        </NTooltip>
      </div>
    </header>

    <!-- ═══════════ 主体区域：flex 三栏 + 折叠按钮 ═══════════ -->
    <div class="flex w-full box-border overflow-hidden relative">
      <!-- 左侧面板 -->
      <aside class="relative shrink-0 bg-bg-surface overflow-hidden border-r border-border transition-[width,border-color] duration-320 ease-[cubic-bezier(0.4,0,0.2,1)] box-border" :style="{ width: leftCollapsed ? '0px' : `${leftWidth}px` }">
        <div class="h-full w-full overflow-y-auto overflow-x-hidden py-2.5 px-3" :style="{ width: leftCollapsed ? '0px' : '100%' }">
          <ArchivePanel />
        </div>
      </aside>

      <!-- 左侧拖拽手柄 -->
      <div
        v-if="!leftCollapsed"
        class="shrink-0 w-[4px] h-full cursor-col-resize bg-border-strong/40 hover:bg-primary/50 transition-colors duration-200 relative z-[4]"
        @mousedown="(e) => startDrag('left', e)"
      >
      </div>

      <!-- 左侧折叠按钮 -->
      <button
        class="shrink-0 w-[18px] h-[52px] flex items-center justify-center bg-bg-surface border border-border-strong cursor-pointer p-0 outline-none text-text-secondary self-center opacity-60 hover:opacity-100 hover:text-primary hover:bg-primary-soft transition-all duration-200 rounded-r-md border-l-0 z-[5]"
        @click="leftCollapsed ? expandLeft() : collapseLeft()"
        :title="leftCollapsed ? '展开面板 (Ctrl+B)' : '收起面板 (Ctrl+B)'"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-3 h-3 shrink-0">
          <polyline v-if="!leftCollapsed" points="15 18 9 12 15 6"/>
          <polyline v-else points="9 18 15 12 9 6"/>
        </svg>
      </button>

      <!-- 中央工作区 -->
      <main class="flex-1 min-w-0 w-full overflow-hidden flex flex-col">
        <Workspace />
      </main>

      <!-- 右侧拖拽手柄 -->
      <div
        v-if="!rightCollapsed"
        class="shrink-0 w-[4px] h-full cursor-col-resize bg-border-strong/40 hover:bg-primary/50 transition-colors duration-200 relative z-[4]"
        @mousedown="(e) => startDrag('right', e)"
      >
      </div>

      <!-- 右侧折叠按钮 -->
      <button
        class="shrink-0 w-[18px] h-[52px] flex items-center justify-center bg-bg-surface border border-border-strong cursor-pointer p-0 outline-none text-text-secondary self-center opacity-60 hover:opacity-100 hover:text-primary hover:bg-primary-soft transition-all duration-200 rounded-l-md border-r-0 z-[5]"
        @click="rightCollapsed ? expandRight() : collapseRight()"
        :title="rightCollapsed ? '展开面板 (Ctrl+Shift+B)' : '收起面板 (Ctrl+Shift+B)'"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-3 h-3 shrink-0">
          <polyline v-if="!rightCollapsed" points="9 18 15 12 9 6"/>
          <polyline v-else points="15 18 9 12 15 6"/>
        </svg>
      </button>

      <!-- 右侧面板 -->
      <aside class="relative shrink-0 bg-bg-surface overflow-hidden border-l border-border transition-[width,border-color] duration-320 ease-[cubic-bezier(0.4,0,0.2,1)] box-border" :style="{ width: rightCollapsed ? '0px' : `${rightWidth}px` }">
        <div class="h-full w-full overflow-y-auto overflow-x-hidden py-2.5 px-3" :style="{ width: rightCollapsed ? '0px' : '100%' }">
          <PropertyPanel />
        </div>
      </aside>
    </div>

    <!-- ═══════════ 全局状态栏 26px ═══════════ -->
    <footer class="flex items-center justify-between px-2 h-statusbar bg-bg-surface border-t border-border select-none text-[11px] text-text-secondary tracking-[0.2px]">
      <GlobalStatusBar />
    </footer>

    <!-- ═══════════ 全局拖拽上传遮罩 ═══════════ -->
    <Transition name="drop-overlay">
      <div v-if="isDragging" class="absolute inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm pointer-events-none">
        <div class="flex flex-col items-center gap-4 px-14 py-10 border-2 border-dashed border-primary rounded-2xl bg-primary-soft text-primary">
          <span class="animate-gentle-float">
            <AppIcon name="upload" :size="44" :stroke-width="1.5" />
          </span>
          <span class="text-base font-semibold tracking-[0.5px]">释放以上传压缩包</span>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
/* ═══════════ 保留样式 ═══════════ */

/* 主题图标切换动画 */
.icon-spin-enter-active,
.icon-spin-leave-active {
  transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.28s ease;
}
.icon-spin-enter-from {
  transform: rotate(-90deg) scale(0.4);
  opacity: 0;
}
.icon-spin-leave-to {
  transform: rotate(90deg) scale(0.4);
  opacity: 0;
}

/* 遮罩淡入淡出 */
.drop-overlay-enter-active,
.drop-overlay-leave-active {
  transition: opacity 0.2s ease;
}
.drop-overlay-enter-from,
.drop-overlay-leave-to {
  opacity: 0;
}

/* 面板内滚动条统一使用全局 6px 样式（见 main.css） */
</style>
