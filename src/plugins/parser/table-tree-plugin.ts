import type { IFileParserPlugin, ParseOptions } from '../types'
import { decodeAndParseCsv } from '../helpers'
import { defineAsyncComponent } from 'vue'

/** 表格+树形联动渲染器（动态导入，按需加载，减小主 chunk） */
const TableTreeRenderer = defineAsyncComponent(() => import('@/views/renderers/TableTreeRenderer.vue'))

/** 表格+树形联动解析插件，用于 *_table_tree.csv 类型文件 */
export const tableTreePlugin: IFileParserPlugin = {
  name: 'table-tree',
  supportedExtensions: [],
  canParse(file) {
    // 通过文件名中的 _table_tree.csv 后缀修饰符识别
    return /_table_tree\.csv$/i.test(file.name)
  },
  async parse(data: Uint8Array, options?: ParseOptions) {
    return decodeAndParseCsv(data, options)
  },
  getComponent() {
    return TableTreeRenderer
  },
}
