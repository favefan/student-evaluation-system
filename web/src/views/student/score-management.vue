<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.name" placeholder="姓名" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <!-- <el-select v-model="listQuery.role" placeholder="角色" clearable class="filter-item" style="width: 180px">
        <el-option v-for="item in roleList" :key="item.id" :label="item.name+'('+item.id+')'" :value="item.id" />
      </el-select>
      <el-select v-model="listQuery.status" placeholder="状态" clearable class="filter-item" style="width: 180px">
        <el-option v-for="item in statusTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select> -->
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        过滤
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加成绩
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-upload" @click="handleUpload">
        批量导入
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="personnelList"
      
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="成绩名称" width="100px">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="获得人" width="180px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.student_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="成绩类型" width="180px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.score_type | scoreTypeFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="分数" width="230px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.score }}</span>
        </template>
      </el-table-column>
      <el-table-column label="获得日期" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.gain_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <!-- <el-table-column label="评分材料" align="center" width="150">
        <template slot-scope="{row}">
          <span>{{ row.account_username }}</span>
        </template>
      </el-table-column> -->
      <!-- <el-table-column label="审核状态" class-name="status-col" width="80">
        <template slot-scope="{row}">
          <el-tag :type="row.account_status | statusStyleFilter">
            {{ row.account_status | status2ShowFilter }}
          </el-tag>
        </template>
      </el-table-column> -->
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <!-- <el-button v-if="row.account_status!='1'" size="mini" type="success" @click="handleModifyStatus(row, 1)">
            启用
          </el-button>
          <el-button v-if="row.account_status!='0'" size="mini" @click="handleModifyStatus(row, 0)">
            禁用
          </el-button> -->
          <el-popconfirm
            confirm-button-text='好的'
            cancel-button-text='不用了'
            icon="el-icon-info"
            icon-color="red"
            title="确定删除吗？"
            style="margin-left: 10px;"
            @onConfirm="handleDelete(row,$index)"
          >
            <el-button slot="reference" v-if="row.status!='9'" size="mini" type="danger" >
              删除
            </el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="170px" style="width: 400px; margin-left:50px;">
        <el-form-item label="成绩名称">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="获得人(学号)">
          <el-input v-model="temp.personnel_code"/>
        </el-form-item>
        <el-form-item label="分数类型">
          <el-select v-model="temp.score_type" class="filter-item" placeholder="请选择...">
            <el-option v-for="item in scoreTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="分数">
          <el-input v-model="temp.score"/>
        </el-form-item>
        <el-form-item label="获得日期">
          <el-date-picker v-model="temp.gain_time" type="datetime" placeholder="请选择一个日期" value-format="yyyy-MM-dd HH:mm:ss"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogExcelVisible" title="上传Excel以批量导入">
      <upload-excel-component :on-success="handleSuccess" :before-upload="beforeUpload" />
      <el-table :data="tableData" border highlight-current-row style="width: 100%;margin-top:20px;">
        <el-table-column v-for="item of tableHeader" :key="item" :prop="item" :label="item" />
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogExcelVisible = false; tableData = []; tableHeader = [];">
          取消
        </el-button>
        <el-button type="primary" @click="uploadExcel2Import">
          导入
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { fetchScoreList, createScore, updateScore, deleteScore, uploadExcelContent } from '@/api/score'
import { changeAccountStatus } from '@/api/permission'
import { fetchDepartmentList } from '@/api/department'
import { getRoles } from '@/api/role'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import UploadExcelComponent from '@/components/UploadExcel/index.vue'

const roleTypeOptions = [
  { key: 'admin', display_name: '系统管理员' },
  { key: 'class_master', display_name: '班级负责人' }
  // { key: 'student', display_name: '成绩' }
]

const scoreTypeOptions = [
  { key: 'study', display_name: '智育' },
  { key: 'sport', display_name: '体育' },
  { key: 'labour', display_name: '劳育' },
  { key: 'morality', display_name: '德育' },
  { key: 'standard', display_name: '平时' },
]

const statusTypeOptions = [
  { key: '1', display_name: '启用' },
  { key: '0', display_name: '禁用' },
  //{ key: '9', display_name: '已删除' }
]

export default {
  name: 'ComplexTable',
  components: { Pagination, UploadExcelComponent },
  directives: { waves },
  filters: {
    statusStyleFilter(status) {
      const statusMap = {
        1: 'success',
        0: 'info',
        9: 'danger'
      }
      return statusMap[status]
    },
    scoreTypeFilter(status) {
      const statusMap = {
        study: '智育',
        sport: '体育',
        labour: '劳育',
        morality: '德育',
        standard: '平时'
      }
      return statusMap[status]
    },
    status2ShowFilter(status) {
      const status2ShowMap = {
        1: '启用',
        0: '禁用',
        //9: '已删除'
      }
      return status2ShowMap[status]
    },
    role2ShowFilter(role) {
      const role2ShowMap = {
        admin: '系统管理员',
        class_master: '班级负责人',
        student: '成绩'
      }
      return role2ShowMap[role]
    }
    // typeFilter(type) {
    //   return calendarTypeKeyValue[type]
    // }
  },
  data() {
    return {
      tableData: [],
      tableHeader: [],
      tableKey: 0,
      personnelList: null,
      departmentList: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        name: undefined,
        // role: undefined,
        // status: undefined,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      // calendarTypeOptions,
      roleTypeOptions,
      statusTypeOptions,
      scoreTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: [{
          status: '启用',
          key: 1
        },
        {
          status: '禁用',
          key: 0
        },
        // {
        //   status: 'deleted',
        //   key: 9
        // }
      ],
      rolesOptions: [],
      // showReviewer: false,
      temp: {
        id: 0,
        name: '',
        personnel_code: '',
        score_type: '',
        score: '',
        gain_time: new Date()
      },
      dialogFormVisible: false,
      dialogExcelVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改成绩',
        create: '新建成绩'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: { // rules of DataForm in dialog
        name: [{ required: true, message: '成绩的名称必须的', trigger: 'blur' }],
        code: [{ required: true, message: '学号是必须的', trigger: 'blur' }],
        type: [{ required: true, message: '分数类型是必须的', trigger: 'blur' }],
        account_status: [{ required: true, message: '状态是必须的', trigger: 'blur' }],
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    this.getDepartmentsList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchScoreList(this.listQuery).then(response => {
        this.personnelList = response.data.items
        for (var i = 0; i < this.personnelList.length; i ++) {  //遍历数组
            if (this.personnelList[i].status != 1)  //如果为数字，则返回该元素的值
                delete this.personnelList[i]
        }
        this.total = response.data.total
        this.listLoading = false
      })
    },
    getDepartmentsList() {
      fetchDepartmentList({page: 1, limit: 100, sort: '+id'}).then(response => {
        this.departmentList = response.data.items
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      console.log(this.listQuery)
      for (let key in this.listQuery) {
        if (this.listQuery[key] == "") {
          this.listQuery[key] = undefined
        }
      }
      this.getList()
    },
    handleModifyStatus(row, status) {
      changeAccountStatus({ id: row.account_id, status: status }).then(() => { 
        this.$message({
          message: '成绩状态切换成功',
          type: 'success'
        })
        // row.status = status
        this.getList()
      })
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: 0,
        name: '',
        personnel_code: '',
        score_type: '',
        score: '',
        gain_time: new Date()
      }
    },
    handleCreate() {
      this.getDepartmentsList()
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          createScore(this.temp).then(() => {
            // this.personnelList.unshift(this.temp)
            this.getList()
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.getDepartmentsList()
      this.temp = Object.assign({}, row) // copy obj
      this.temp.id = row.id
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateScore(tempData).then(() => {
           this.getList()
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row, index) {
      deleteScore(row.id).then(() => {
        this.$notify({
        title: 'Success',
        message: '成绩删除成功',
        type: 'success',
        duration: 2000
      })
        // this.list.splice(index, 1)
        this.getList()
      })
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    handleUpload() {
      this.dialogExcelVisible = true
      // this.downloadLoading = true
      // import('@/vendor/Export2Excel').then(excel => {
      //   const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
      //   const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
      //   const data = this.formatJson(filterVal)
      //   excel.export_json_to_excel({
      //     header: tHeader,
      //     data,
      //     filename: 'table-list'
      //   })
      //   this.downloadLoading = false
      },
      beforeUpload(file) {
      const isLt1M = file.size / 1024 / 1024 < 1

      if (isLt1M) {
        return true
      }

      this.$message({
        message: 'Please do not upload files larger than 1m in size.',
        type: 'warning'
      })
      return false
    },
    handleSuccess({ results, header }) {
      console.log(results)
      this.tableData = results
      this.tableHeader = header
      console.log(this.tableData)
    },
    uploadExcel2Import() {
      uploadExcelContent(this.tableData).then(() => {
        this.$notify({
          title: 'Success',
          message: '成绩批量创建成功',
          type: 'success',
          duration: 2000
        })
        this.dialogExcelVisible = false
        this.getList()
      })
    }
  }
}
</script>
