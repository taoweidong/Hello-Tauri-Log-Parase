<script setup lang="ts">
/**
 * 归档状态指示器
 * 根据压缩包处理状态显示对应标签（已完成/解压中/排队中/失败）及进度条
 * 解压中：状态点呼吸 + 条纹流动进度条，动画即信息
 */
import { NTag } from 'naive-ui'
import type { ArchiveStatus } from '@/types'

defineProps<{
  status: ArchiveStatus
  progress: number
}>()
</script>

<template>
  <div class="flex items-center gap-1.5">
    <!-- 已完成：静态绿点 -->
    <template v-if="status === 'completed'">
      <span class="status-dot status-dot-success"></span>
      <span class="status-label status-label-success">已完成</span>
    </template>

    <!-- 解压中：呼吸蓝点 + 条纹流动进度条 -->
    <template v-else-if="status === 'running'">
      <span class="status-dot status-dot-running"></span>
      <span class="status-label">解压中</span>
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: `${Math.min(100, Math.max(0, progress))}%` }"></div>
      </div>
    </template>

    <!-- 排队中：琥珀点 -->
    <template v-else-if="status === 'pending'">
      <span class="status-dot status-dot-pending"></span>
      <span class="status-label">排队中</span>
    </template>

    <!-- 失败：红点 -->
    <template v-else-if="status === 'failed'">
      <span class="status-dot status-dot-failed"></span>
      <span class="status-label status-label-failed">失败</span>
    </template>
  </div>
</template>

<style scoped>
/* 状态点：统一尺寸与呼吸/静态变体 */
.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}
.status-dot-success {
  background: var(--color-success);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-success) 18%, transparent);
}
.status-dot-running {
  background: var(--color-primary);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-primary) 18%, transparent);
  animation: status-breathe 2.4s ease-in-out infinite;
}
.status-dot-pending {
  background: var(--color-warning);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-warning) 18%, transparent);
}
.status-dot-failed {
  background: var(--color-error);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--color-error) 18%, transparent);
}

/* 状态文字 */
.status-label {
  font-size: 12px;
  color: var(--color-text-secondary);
  white-space: nowrap;
}
.status-label-success {
  color: var(--color-success);
}
.status-label-failed {
  color: var(--color-error);
}

/* 进度条：细轨道 + 条纹流动 */
.progress-track {
  width: 56px;
  height: 4px;
  border-radius: 2px;
  background: color-mix(in srgb, var(--color-primary) 14%, transparent);
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 2px;
  background-image: linear-gradient(
    45deg,
    color-mix(in srgb, var(--color-primary) 75%, transparent) 25%,
    var(--color-primary) 25%,
    var(--color-primary) 50%,
    color-mix(in srgb, var(--color-primary) 75%, transparent) 50%,
    color-mix(in srgb, var(--color-primary) 75%, transparent) 75%,
    var(--color-primary) 75%
  );
  background-size: 12px 12px;
  animation: progress-stripes 0.9s linear infinite;
  transition: width var(--duration-base) var(--ease-out-quart);
}
</style>
