<template>
  <div>
  <el-row>
    <el-col :span="20">
      <el-input v-model="filepath" @keydown.enter="send_file_msg"></el-input>
    </el-col>
    <el-col :span="4">
      <el-button @click="send_file_msg">查看日志</el-button>
    </el-col>
  </el-row>

  <div
    id="terminal"
    style="margin: 10px; text-align: left; height: 700px"
    :class="{ 'is-loading': loading }"
    ref="terminal"
  ></div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import { debounce } from "lodash";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import "xterm/css/xterm.css";

export default {
  data() {
    return {
      filepath: "",
      terminal: null,
      first: true,
      loading: true,
      terminalSocket: null,
      term: null,
    };
  },
  methods: {
    send_file_msg() {
      if (this.isWsOpen()) {
        this.terminalSocket.send(
          JSON.stringify({
            filepath: this.filepath,
          })
        );
      }
    },
    runRealTerminal() {
      this.loading = false;
    },
    onWSReceive(message) {
      // 首次接收消息,发送给后端，进行同步适配
      if (this.first === true) {
        this.first = false;
        this.resizeRemoteTerminal();
      }
      const data = JSON.parse(message.data);
      this.term.element && this.term.focus();
      this.term.write(data.message);
    },
    errorRealTerminal(ex) {
      let message = ex.message;
      if (!message) message = "disconnected";
      this.term.write(`\x1b[31m${message}\x1b[m\r\n`);
      console.log("err");
    },
    closeRealTerminal() {
      console.log("close");
    },
    createWS() {
      const url = "ws://127.0.0.1:8000/ws/message/hihi/hihi";
      this.terminalSocket = new WebSocket(url);
      this.terminalSocket.onopen = this.runRealTerminal;
      this.terminalSocket.onmessage = this.onWSReceive;
      this.terminalSocket.onclose = this.closeRealTerminal;
      this.terminalSocket.onerror = this.errorRealTerminal;
    },
    initWS() {
      if (!this.terminalSocket) {
        this.createWS();
      }
      if (this.terminalSocket && this.terminalSocket.readyState > 1) {
        this.terminalSocket.close();
        this.createWS();
      }
    },
    resizeRemoteTerminal() {
      const { cols, rows } = this.term;
      if (this.isWsOpen()) {
        this.terminalSocket.send(
          JSON.stringify({
            Op: "resize",
            Cols: cols,
            Rows: rows,
          })
        );
      }
    },
    initTerm() {
      this.term = new Terminal({
        lineHeight: 1.2,
        fontSize: 12,
        fontFamily: "Monaco, Menlo, Consolas, 'Courier New', monospace",
        theme: {
          background: "#181d28",
        },
        // 光标闪烁
        cursorBlink: true,
        cursorStyle: "underline",
        scrollback: 1000,
        tabStopWidth: 4,
      });
      this.term.open(this.$refs.terminal);
      this.term.loadAddon(new FitAddon());
      // 不能初始化的时候fit,需要等terminal准备就绪,可以设置延时操作
      setTimeout(() => {
        this.fitTerm();
      }, 5);
    },
    isWsOpen() {
      const readyState = this.terminalSocket && this.terminalSocket.readyState;
      return readyState === 1;
    },
    fitTerm() {
      this.term.fit();
    },
    onResize: debounce(function () {
      this.fitTerm();
    }, 800),
    termData() {
      this.term.onData((data) => {
        if (this.isWsOpen()) {
          this.terminalSocket.send(
            JSON.stringify({
              Op: "stdin",
              Data: data,
            })
          );
        }
      });
    },
    onTerminalResize() {
      window.addEventListener("resize", this.onResize);
    },
    removeResizeListener() {
      window.removeEventListener("resize", this.onResize);
    },
  },
  watch: {
    type() {
      this.first = true;
      this.loading = true;
      this.terminalSocket = null;
      this.initWS();
      // 重置
      this.term.reset();
    },
  },
  mounted() {
    this.initWS();
    this.initTerm();
    this.termData();
    this.onTerminalResize();
  },
  beforeUnmount() {
    this.removeResizeListener();
    this.terminalSocket && this.terminalSocket.close();
  },
};
</script>

<style lang="scss" scoped>
#terminal {
  width: 100%;
  height: 100%;
  &.is-loading {
    // 添加样式以显示加载状态
  }
}
</style>
