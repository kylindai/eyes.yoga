// rollup.config.js
import { terser } from '@rollup/plugin-terser'; // 引入 Terser 插件用于压缩代码

export default {
  input: 'dist/greeter.js',       // 指定入口文件
  output: {
    file: 'dist/bundle.min.js',  // 打包后输出的文件路径
    format: 'es',               // 立即执行函数表达式格式，适合浏览器环境
    name: 'Greeter',              // 如果是iife格式，需要指定一个全局变量的名字
    sourcemap: true,              // 生成source map，便于调试
  },
  plugins: [
    terser({ compress: true })    // 使用Terser插件进行压缩
  ],
};