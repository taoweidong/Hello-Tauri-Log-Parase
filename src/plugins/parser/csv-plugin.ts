import type { IFileParserPlugin, ConfigSchema, ParseOptions } from '../types'
import { createExtensionMatcher, decodeAndParseCsv } from '../helpers'
import { defineAsyncComponent } from 'vue'

const EXTENSIONS = ['.csv', '.tsv']

/** CSV 渲染器（动态导入，按需加载，减小主 chunk） */
const CsvRenderer = defineAsyncComponent(() => import('@/views/renderers/CsvRenderer.vue'))

/** CSV/TSV 解析插件，支持自定义分隔符与固定表头 */
export const csvPlugin: IFileParserPlugin = {
  name: 'csv',
  supportedExtensions: EXTENSIONS,
  canParse: createExtensionMatcher(EXTENSIONS),
  async parse(data: Uint8Array, options?: ParseOptions) {
    return decodeAndParseCsv(data, options)
  },
  getComponent() {
    return CsvRenderer
  },
  getConfigSchema(): ConfigSchema {
    return {
      fields: [
        { key: 'delimiter', label: '分隔符', type: 'input', default: ',' },
        { key: 'fixedHeader', label: '固定表头', type: 'switch', default: true },
      ]
    }
  },
}
