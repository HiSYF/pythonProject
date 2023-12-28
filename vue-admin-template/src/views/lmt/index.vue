<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index +1 }}
        </template>
      </el-table-column>
      <el-table-column label="账号" width=auth>
        <template slot-scope="scope">
          {{ scope.row.username }}
        </template>
      </el-table-column>
      <el-table-column label="密码" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.password }}</span>
        </template>
      </el-table-column>
      <el-table-column label="web端口" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.webport }}</span>
        </template>
      </el-table-column>
      <el-table-column label="appID" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.appID }}</span>
        </template>
      </el-table-column>
      <el-table-column label="appSecret" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.appSecret }}</span>
        </template>
      </el-table-column>
      <el-table-column label="摄像头总数" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.sxtZS }}</span>
        </template>
      </el-table-column>
      <el-table-column label="摄像头启用数" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.sxtQYS }}</span>
        </template>
      </el-table-column>
      <el-table-column label="摄像头在线数" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.sxtZXS }}</span>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
      fixed="right"
      label="操作"
      width="100">
      <template slot-scope="scope">
        <el-button @click="handleEdit(scope.$index, scope.row)" type="text" size="small">编辑</el-button>
        <el-button @click="handleDelete(scope.$index, scope.row)" type="text" size="small">删除</el-button>
      </template>
    </el-table-column>
    </el-table>
    <el-dialog
      title="编辑"
      :visible.sync="dialogFormVisible"
      :before-close="handleDialogClose"
    >
      <el-form :model="editForm" ref="editForm" label-width="80px">
        <el-form-item label="账号">
          <el-input v-model="editForm.username"></el-input>
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="editForm.password"></el-input>
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="editForm.webport"></el-input>
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="editForm.appID"></el-input>
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="editForm.appSecret"></el-input>
        </el-form-item>
        <!-- 其他表单项 -->
        <!-- ... （根据需要添加其他表单项） ...  -->
        <el-form-item>
          <el-button type="primary" @click="updateData">提交</el-button>
          <el-button @click="closeDialog">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-pagination
      :page-size="10"
      :pager-count="5"
      layout="prev, pager, next"
      :total=total_articles
      @current-change="fetchData"
    >>
    </el-pagination>
  </div>

</template>

<script>
import {getLmt,putLmt,delLmt} from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'ok',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      total_articles: null, //定义数据总条数
      listLoading: true,
      dialogFormVisible: false, // 控制Dialog显示/隐藏
      editForm: {}, // 存储编辑的数据
      editIndex: -1 // 用于记录编辑的行索引
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData(page) {
      this.listLoading = true
      // 在这里调用后端API获取特定页数的数据
      getLmt({page:page}).then(response => {
        this.list = response.data.data //数据
        this.total_articles = response.data.total_articles //总数据条数
        this.listLoading = false
      })
    },

    handleEdit(index, row) {
        // 点击编辑按钮时，显示Dialog，并将对应行的数据填充到表单中
      this.editForm = Object.assign({}, row) // 浅拷贝数据，避免直接修改原始数据
      this.editIndex = index // 记录编辑的行索引
      this.dialogFormVisible = true
      },
    updateData() {
      // 在这里调用后端API提交编辑后的数据
              console.log(this.editForm.id)
        console.log(this.editForm)
      putLmt(this.editForm.id, this.editForm).then(response => {
        // 处理编辑成功的逻辑

        this.fetchData() // 编辑成功后重新获取数据
        this.dialogFormVisible = false // 关闭Dialog
      })
    },
    closeDialog() {
      // 取消编辑时，关闭Dialog
      this.dialogFormVisible = false
    },
    handleDialogClose(done) {
      // 在这里执行一些关闭前的逻辑
      if (this.editForm.username === '') {
        this.$message.error('账号不能为空');
        // 如果账号为空，阻止关闭对话框
      } else {
        // 如果账号不为空，允许关闭对话框
        done();  // 调用 done() 来关闭 Dialog
      }
    },
    handleDelete(index, row) {
      console.log(index, row);
    }
  }
}
</script>
