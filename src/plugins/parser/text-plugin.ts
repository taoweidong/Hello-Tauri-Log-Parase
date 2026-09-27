import type { IFileParserPlugin, ParseOptions } from '../types'
import { createExtensionMatcher } from '../helpers'
import { parseText } from '@/plugins/parsers/text-parser'
import { defineAsyncComponent } from 'vue'

const EXTENSIONS = ['.txt', '.md', '.cfg', '.ini', '.env', '.yaml', '.yml', '.toml']

/** 文本渲染器（动态导入，按需加载，减小主 chunk） */
const TextRenderer = defineAsyncComponent(() => import('@/views/renderers/TextRenderer.vue'))

/** 纯文本解析插件，支持 txt、md、cfg、ini、env、yaml、toml 等格式 */
export const textPlugin: IFileParserPlugin = {
  name: 'text',
  supportedExtensions: EXTENSIONS,
  canParse: createExtensionMatcher(EXTENSIONS),
  async parse(data: Uint8Array, options?: ParseOptions) {
    return parseText(data, options?.encoding)
  },
  getComponent() {
    return TextRenderer
  },
}
