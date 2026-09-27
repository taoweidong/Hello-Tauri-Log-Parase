import type { IFileParserPlugin, ParseOptions } from '../types'
import { createExtensionMatcher, decodeText } from '../helpers'
import { parseJson } from '@/plugins/parsers/json-parser'
import { defineAsyncComponent } from 'vue'

const EXTENSIONS = ['.json', '.jsonl']

/** JSON 渲染器（动态导入，按需加载，减小主 chunk） */
const JsonRenderer = defineAsyncComponent(() => import('@/views/renderers/JsonRenderer.vue'))

/** JSON/JSONL 解析插件，支持标准 JSON 与按行分隔的 JSONL 格式 */
export const jsonPlugin: IFileParserPlugin = {
  name: 'json',
  supportedExtensions: EXTENSIONS,
  canParse: createExtensionMatcher(EXTENSIONS),
  async parse(data: Uint8Array, options?: ParseOptions) {
    const text = decodeText(data, options?.encoding ?? 'utf-8')
    return parseJson(text)
  },
  getComponent() {
    return JsonRenderer
  },
}
