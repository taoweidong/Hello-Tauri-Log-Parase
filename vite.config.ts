import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { resolve } from 'path'

const platform = process.env.VITE_PLATFORM || 'web'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  define: {
    __PLATFORM__: JSON.stringify(platform)
  },
  resolve: {
    alias: {
      '@': resolve(import.meta.dirname, 'src'),
      '@adapter': platform === 'tauri'
        ? resolve(import.meta.dirname, 'src/adapters/tauri-adapter')
        : resolve(import.meta.dirname, 'src/adapters/web-adapter')
    }
  },
  build: {
    outDir: 'build/web',
    emptyOutDir: true,
    // 主 chunk 含 Vue + Naive UI + 应用核心，~650KB 属预期架构体积；
    // 渲染器已拆动态 chunk（见 plugins/parser），超 800KB 才视为异常膨胀
    chunkSizeWarningLimit: 800,
    rolldownOptions: {
      external: platform === 'web' ? [/@tauri-apps\/api/] : []
    }
  }
})
