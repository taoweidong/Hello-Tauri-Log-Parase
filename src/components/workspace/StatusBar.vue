<script setup lang="ts">
import { computed } from 'vue'
import { useTabManager } from '@/composables/use-tabs'
import { formatSize } from '@/core/format'

const { activeTab, cursorPosition, globalFontSize } = useTabManager()

/** 当前文件摘要信息（行数、编码、插件名） */
const fileInfo = computed(() => {
  if (!activeTab.value?.content) return '无文件打开'
  const c = activeTab.value.content
  const parts: string[] = []
  if (c.lineCount !== undefined) parts.push(`${c.lineCount} 行`)
  if (c.encoding) parts.push(c.encoding)
  if (c.pluginName) parts.push(c.pluginName)
  return parts.join(' | ')
})

/** 当前文件大小（复用 formatSize 工具函数） */
const fileSize = computed(() => {
  const size = activeTab.value?.content?.size
  return size ? formatSize(size) : ''
})

const hasContent = computed(() => !!activeTab.value?.content)
</script>

<template>
  <div class="flex items-center justify-between w-full">
    <div class="flex items-center gap-3">
      <span v-if="hasContent" class="tabular-nums">行 {{ cursorPosition.line }}, 列 {{ cursorPosition.column }}</span>
      <span v-if="hasContent" class="opacity-40">|</span>
      <span>{{ fileInfo }}</span>
      <span v-if="fileSize" class="opacity-60">{{ fileSize }}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="text-[11px] opacity-50">字体缩放</span>
      <input
        type="range"
        min="10"
        max="24"
        v-model.number="globalFontSize"
        class="font-slider"
        title="字体缩放"
      />
      <span class="text-[11px] opacity-50 tabular-nums w-9">{{ globalFontSize }}px</span>
    </div>
  </div>
</template>

<style scoped>
/* 自定义字号滑块：细轨道 + 圆形 thumb，替换原生突兀样式 */
.font-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 80px;
  height: 4px;
  border-radius: 2px;
  background: var(--color-border-strong);
  outline: none;
  cursor: pointer;
}
.font-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 2px solid var(--color-bg-surface);
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--color-primary) 40%, transparent);
  cursor: pointer;
  transition: transform var(--duration-fast) var(--ease-out-quart),
              box-shadow var(--duration-fast) var(--ease-out-quart);
}
.font-slider::-webkit-slider-thumb:hover {
  transform: scale(1.25);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-primary) 25%, transparent);
}
.font-slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 2px solid var(--color-bg-surface);
  cursor: pointer;
  transition: transform var(--duration-fast) var(--ease-out-quart);
}
.font-slider::-moz-range-thumb:hover {
  transform: scale(1.25);
}
</style>
