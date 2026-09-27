<script setup lang="ts">
/**
 * 统一 SVG 图标组件
 * 24×24 viewBox，内联 path 分发，继承 currentColor，尺寸随字号缩放
 * 目标：全应用零 Unicode 字符图标、零 CDN、零图标库依赖
 */
import { computed } from 'vue'

/** 图标名称（受控联合类型，拼写错误在编译期暴露） */
export type AppIconName =
  | 'upload'
  | 'search'
  | 'file'
  | 'clock'
  | 'folder'
  | 'chevron-left'
  | 'chevron-right'
  | 'chevron-down'
  | 'close'
  | 'sun'
  | 'moon'
  | 'help'
  | 'github'
  | 'issue'
  | 'pin'
  | 'arrow-up'
  | 'trash'
  | 'retry'
  | 'warning'
  | 'check'
  | 'batch'

const props = withDefaults(defineProps<{
  /** 图标名称 */
  name: AppIconName
  /** 尺寸（px，默认 16） */
  size?: number
  /** 描边宽度（默认 2，填充型图标忽略） */
  strokeWidth?: number
}>(), {
  size: 16,
  strokeWidth: 2,
})

/** 填充型图标（fill="currentColor"，无描边） */
const FILLED_ICONS: ReadonlySet<AppIconName> = new Set(['pin', 'github'])

const isFilled = computed(() => FILLED_ICONS.has(props.name))

/**
 * 图标 path 数据表
 * stroke 型图标遵循 Feather 风格：24×24 网格、圆角端点
 */
const PATHS: Record<AppIconName, string> = {
  upload: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4|M17 8 12 3 7 8|M12 3v12',
  search: 'M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z|M21 21l-4.35-4.35',
  file: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z|M14 2v6h6',
  clock: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z|M12 6v6l4 2',
  folder: 'M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z',
  'chevron-left': 'M15 18l-6-6 6-6',
  'chevron-right': 'M9 18l6-6-6-6',
  'chevron-down': 'M6 9l6 6 6-6',
  close: 'M18 6 6 18|M6 6l12 12',
  sun: 'M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10z|M12 1v2|M12 21v2|M4.22 4.22l1.42 1.42|M18.36 18.36l1.42 1.42|M1 12h2|M21 12h2|M4.22 19.78l1.42-1.42|M18.36 5.64l1.42-1.42',
  moon: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z',
  help: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z|M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3|M12 17h.01',
  github: 'M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z',
  issue: 'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z|M12 8v4|M12 16h.01',
  pin: 'M16 9V4h1c.55 0 1-.45 1-1s-.45-1-1-1H7c-.55 0-1 .45-1 1s.45 1 1 1h1v5c0 1.66-1.34 3-3 3v2h5.97v7l1 1 1-1v-7H19v-2c-1.66 0-3-1.34-3-3z',
  'arrow-up': 'M12 19V5|M5 12l7-7 7 7',
  trash: 'M3 6h18|M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6|M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2',
  retry: 'M23 4v6h-6|M20.49 15a9 9 0 1 1-2.12-9.36L23 10',
  warning: 'M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z|M12 9v4|M12 17h.01',
  check: 'M20 6 9 17l-5-5',
  batch: 'M8 6h13|M8 12h13|M8 18h13|M3 6h.01|M3 12h.01|M3 18h.01',
}

/** 拆分多段 path（| 分隔） */
const pathSegments = computed(() => PATHS[props.name].split('|'))
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    :stroke="isFilled ? 'none' : 'currentColor'"
    :stroke-width="isFilled ? 0 : strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    :fill-rule="isFilled ? 'evenodd' : undefined"
    aria-hidden="true"
    focusable="false"
  >
    <!-- 填充型图标：单 path 用 fill -->
    <path v-if="isFilled" :d="pathSegments[0]" fill="currentColor" />
    <!-- 描边型图标：多段 path -->
    <path v-else v-for="(d, i) in pathSegments" :key="i" :d="d" />
  </svg>
</template>
