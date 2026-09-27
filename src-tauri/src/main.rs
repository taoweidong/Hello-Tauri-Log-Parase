// 发布构建（打包 exe）走 Windows GUI 子系统，双击启动不弹出黑色控制台窗口；
// 调试构建保留控制台，方便开发期查看日志与 panic 信息。
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    hello_tauri_log_parase::run()
}
