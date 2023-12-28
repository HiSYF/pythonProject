<template>
  <div ref="xterm" className="terminal" :style="styleVar"/>
</template>

<script>
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import 'xterm/css/xterm.css'
export default {
  name: 'Xterm',
  props: {
    ip: { type: String }, // 通过父组件传递登录ip
    height: {
      type: Number, // xterm显示屏幕，高度
      default: 100
    }
  },
  data() {
    return {
      term: null,
      socket: null
    }
  },
  computed: { // 动态设置xterm显示屏幕高度
    styleVar() {
      return {
        '--terminal-height': this.height + 'vh'
      }
    }
  },
  mounted() { // 初始化链接
    this.init()
    this.initSocket()
  },
  beforeDestroy() { // 退出销毁链接
    this.socket.close()
    this.term.dispose()
  },
  methods: {
    init() { // 初始化Terminal
      this.term = new Terminal({
        fontSize: 18,
        convertEol: true, // 启用时，光标将设置为下一行的开头
        rendererType: 'canvas', // 渲染类型
        cursorBlink: true, // 光标闪烁
        cursorStyle: 'bar', // 光标样式 underline
        theme: {
          background: '#060101', // 背景色
          cursor: 'help' // 设置光标
        }
      })
    },
    initSocket() { // 初始化Websocket
      const fitPlugin = new FitAddon()
      this.term.loadAddon(fitPlugin)

      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      // this.socket = new WebSocket(`${protocol}//${window.location.host}/ws/ssh/${this.ip}`)
      this.socket = new WebSocket(`${protocol}//${window.location.host}/ws/ssh/1/`)

      this.socket.onmessage = e => {
        const reader = new window.FileReader()
        reader.onload = () => this.term.write(reader.result)
        reader.readAsText(e.data, 'utf-8')
      }

      this.socket.onopen = () => {
        this.term.open(this.$refs.xterm)
        this.term.focus()
        fitPlugin.fit()
      }

      this.socket.onclose = e => {
        if (e.code === 1234) { // 结束标记
          window.location.href = 'about:blank'
          window.close()
        } else {
          setTimeout(() => this.term.write('\r\nConnection is closed.\r\n'), 200)
        }
      }

      this.term.onData(data => this.socket.send(JSON.stringify({ data })))
      this.term.onResize(({ cols, rows }) => {
        this.socket.send(JSON.stringify({ resize: [cols, rows] }))
      })

      window.onresize = () => fitPlugin.fit()
    }
  }
}
</script>
<style lang="scss" scoped>
.terminal {
  display: flex;
  width: 100%;
  min-height: var(--terminal-height);
  flex: 1;
  background-color: #000;
}

.terminal > div {
  flex: 1;
}
</style>
