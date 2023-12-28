<template>
  <div style="padding: 30px;">
    <el-alert :closable="false" title="menu 1-1" type="success" class="full-height-alert">
      <el-row :gutter="20" :justify="justify" type="flex" class="row-flex">
        <el-card class="box-card" v-for="(item, index) in displayBoxes" :key="index" :span="getSpanValue(displayBoxes.length)">
          <el-card>{{ index + 1 }}</el-card>
        </el-card>
      </el-row>
      <el-button v-if="displayBoxes.length < 3" @click="addDisplayBox">Add Display Box</el-button>
    </el-alert>
  </div>
</template>

<script>
export default {
  data() {
    return {
      displayBoxes: [],
      justify: 'end'
    };
  },
  methods: {
    addDisplayBox() {
      if (this.displayBoxes.length < 3) {
        this.displayBoxes.push({});
        if (this.displayBoxes.length === 2) {
          this.justify = 'center';
        } else if (this.displayBoxes.length === 3) {
          this.justify = 'start';
        }
      }
    },
    getSpanValue(length) {
      if (length === 1) {
        return 24; // 占据整行
      } else {
        return 24 / length; // 平分行宽
      }
    }
  }
};
</script>

<style>
.el-card {
  height: 100px;
  text-align: center;
  line-height: 100px;
  flex: 1;
}

.full-height-alert {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.row-flex {
  width: 100%;


  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
