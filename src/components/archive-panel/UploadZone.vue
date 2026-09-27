<script setup lang="ts">
/**
 * 上传区域组件
 * 支持点击选择与拖放上传压缩包，内部执行过滤→验证→添加流程
 */
import { ref } from 'vue'
import { NText, useMessage } from 'naive-ui'
import { useArchiveManager } from '@/composables/use-archives'
import { processArchiveUpload } from '@/core/archive-utils'

const { addFiles } = useArchiveManager()
const message = useMessage()
const fileInput = ref<HTMLInputElement>()
const isDragging = ref(false)
let dragDepth = 0

/** 处理拖放或输入的文件：过滤 → 验证 → 添加 */
async function processFiles(rawFiles: File[]) {
  const validFiles = await processArchiveUpload(rawFiles, (name, msg) => {
    message.error(`${name}：${msg}`)
  })
  if (validFiles.length) addFiles(validFiles)
}

/** 处理文件拖放事件 */
async function handleDrop(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false
  dragDepth = 0
  const items = e.dataTransfer?.files
  if (!items?.length) return
  await processFiles(Array.from(items))
}


/** 处理拖拽进入事件 */
function handleDragEnter(e: DragEvent) {
  e.preventDefault()
  dragDepth++
  isDragging.value = true
}

/** 处理拖拽离开事件 */
function handleDragLeave() {
  dragDepth--
  if (dragDepth <= 0) {
    dragDepth = 0
    isDragging.value = false
  }
}

/** 处理拖拽悬停事件 */
function handleDragOver(e: DragEvent) {
  e.preventDefault()
}

/** 点击上传区域时触发文件选择 */
function handleClick() {
  fileInput.value?.click()
}

/** 处理文件输入框 change 事件 */
async function handleInputChange(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files?.length) return
  await processFiles(Array.from(input.files))
  input.value = ''
}
</script>

<template>
  <div
    class="upload-zone"
    :class="{ 'upload-zone-active': isDragging }"
    @drop="handleDrop"
    @dragenter="handleDragEnter"
    @dragleave="handleDragLeave"
    @dragover="handleDragOver"
    @click="handleClick"
  >
    <div class="p-4 text-center pointer-events-none">
      <span class="upload-icon" :class="{ 'upload-icon-float': isDragging }">
        <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
      </span>
      <NText depth="3">拖拽压缩包到此处，或点击上传</NText>
    </div>
    <input
      ref="fileInput"
      type="file"
      multiple
      accept=".zip,.gz,.gzip,.tgz,.7z,.rar,.tar"
      class="hidden"
      @change="handleInputChange"
    />
  </div>
</template>

<style scoped>
/* 上传区域：虚线边框 + 拖入时高亮/上浮/图标浮动 */
.upload-zone {
  cursor: pointer;
  border: 1px dashed var(--color-border-strong);
  border-radius: 6px;
  margin-right: 4px;
  transition: border-color var(--duration-base) var(--ease-out-quart),
              background-color var(--duration-base) var(--ease-out-quart),
              transform var(--duration-base) var(--ease-out-quart),
              box-shadow var(--duration-base) var(--ease-out-quart);
}
.upload-zone:hover {
  border-color: var(--color-primary);
  background: color-mix(in srgb, var(--color-primary) 7%, transparent);
}
.upload-zone-active {
  border-color: var(--color-primary);
  background: color-mix(in srgb, var(--color-primary) 10%, transparent);
  transform: scale(1.01);
  box-shadow: 0 0 0 4px color-mix(in srgb, var(--color-primary) 15%, transparent);
}

/* 上传图标：拖入时轻浮动，暗示「可放置」 */
.upload-icon {
  display: inline-block;
  margin-bottom: 8px;
  color: var(--color-text-secondary);
  transition: color var(--duration-base) var(--ease-out-quart);
}
.upload-zone:hover .upload-icon,
.upload-zone-active .upload-icon {
  color: var(--color-primary);
}
.upload-icon-float {
  animation: gentle-float 1.6s ease-in-out infinite;
}
</style>
