<script setup lang="ts">
/**
 * 归档卡片组件
 * 展示单个压缩包的状态、错误信息与文件树，支持展开/折叠、删除与重试
 */
import { ref } from 'vue'
import { NCard, NButton, NCollapseTransition } from 'naive-ui'
import type { ArchiveItem } from '@/types'
import StatusIndicator from './StatusIndicator.vue'
import FileTree from './FileTree.vue'
import AppIcon from '@/components/shared/AppIcon.vue'

const props = defineProps<{
  archive: ArchiveItem
}>()

const emit = defineEmits<{
  remove: [id: string]
  retry: [id: string]
}>()

const collapsed = ref(false)

/** 切换归档卡片的展开/折叠状态 */
function toggleCollapse() {
  collapsed.value = !collapsed.value
}
</script>

<template>
  <NCard size="small" closable class="mb-2" @close="emit('remove', archive.id)">
    <template #header>
      <div class="flex items-center gap-2 cursor-pointer select-none w-full" @click="toggleCollapse">
        <svg
          viewBox="0 0 24 24"
          width="16"
          height="16"
          fill="currentColor"
          class="transition-transform duration-200 flex-shrink-0"
          :class="{ '-rotate-90': collapsed }"
        >
          <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z" />
        </svg>
        <span class="flex-1 truncate text-sm">{{ archive.name }}</span>
      </div>
    </template>
    <template #header-extra>
      <StatusIndicator :status="archive.status" :progress="archive.progress" />
    </template>

    <NCollapseTransition :show="!collapsed">
      <!-- 失败：图标 + 错误信息 + 重试按钮 -->
      <div v-if="archive.status === 'failed'" class="archive-error mb-2">
        <span class="archive-error-icon"><AppIcon name="warning" :size="14" /></span>
        <span class="flex-1 min-w-0 text-[12px] break-all">{{ archive.error }}</span>
        <NButton size="tiny" @click="emit('retry', archive.id)">重试</NButton>
      </div>

      <div v-else-if="archive.status === 'pending'" class="text-muted mb-2">
        <NButton size="tiny" @click="emit('retry', archive.id)">重新加载</NButton>
      </div>

      <!-- B1：业务清单外的未知文件提示 -->
      <div
        v-if="archive.unsupportedFiles && archive.unsupportedFiles.length > 0"
        class="archive-warn mb-2"
      >
        <span class="archive-error-icon"><AppIcon name="warning" :size="14" /></span>
        <span>{{ archive.unsupportedFiles.length }} 个文件不支持解压展示</span>
      </div>

      <FileTree
        v-if="archive.files.length > 0"
        :data="archive.files"
        :archive-id="archive.id"
      />
    </NCollapseTransition>
  </NCard>
</template>

<style scoped>
/* 失败信息行：轻红底 + 图标 + 可换行文本 */
.archive-error {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  padding: 6px 8px;
  border-radius: 4px;
  color: var(--color-error);
  background: color-mix(in srgb, var(--color-error) 8%, transparent);
}
.archive-warn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: var(--color-warning);
  background: color-mix(in srgb, var(--color-warning) 8%, transparent);
}
.archive-error-icon {
  display: inline-flex;
  flex-shrink: 0;
  margin-top: 1px;
}
</style>
