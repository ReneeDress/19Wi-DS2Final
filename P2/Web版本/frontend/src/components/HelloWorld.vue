<template>
  <transition name="el-zoom-in-top">
  <el-container>
    <el-header height="100%" style="margin-bottom: 40px" v-show="show">
      <el-image :src="require('../assets/head.png')" style="width: 96%; align-content: center; opacity: 80%;"/>
    </el-header>
    <el-main v-show="show">
      <el-row :gutter="20">
        <el-col :span="10" :offset="6"><el-input v-model="input" placeholder="请输入要查找的单词"></el-input></el-col>
        <el-col :span="2" :offset="0"><el-button type="primary" @click="onSubmit" @keyup.enter="onSubmit">搜索例句</el-button></el-col>
      </el-row>
      <br><br>
    </el-main>
<!--&lt;!&ndash;    {% verbatim %}&ndash;&gt;-->
<!--    <el-row>-->
<!--      <el-button>{{ hello['hello'] }}</el-button>-->
<!--      <el-button type="primary">{{ hello['world'] }}</el-button>-->
<!--      <el-button type="success">成功按钮</el-button>-->
<!--      <el-button type="info">信息按钮</el-button>-->
<!--      <el-button type="warning">警告按钮</el-button>-->
<!--      <el-button type="danger">危险按钮</el-button>-->
<!--    </el-row>-->
<!--&lt;!&ndash;    {% endverbatim %}&ndash;&gt;-->
    <el-row :gutter="20">
      <el-col :span="7" :offset="1"><div class="grid-content bg-purple" style="height: 200px"></div></el-col>
      <el-col :span="8"><div class="grid-content bg-purple" style="height: 200px"></div></el-col>
      <el-col :span="7"><div class="grid-content bg-purple" style="height: 200px"></div></el-col>
    </el-row>
    <br><br><br>
    <el-footer style="line-height: 20px; font-size: 14px">
      Copyright © 2020 <a class="link" href="http://yijunstudio.xyz">YijunLin.</a> All Rights Reserved.<br>
      上海大学计算机工程与科学学院2019-2020学年冬季学期《数据结构(2)》课程作业<br>
      部分数据来源: <a class="link" href="http://www.iciba.com/">金山词霸在线词典</a><br>
      <a class="link" href="http://www.beian.gov.cn/portal/index.do/">沪ICP备20015145号-1</a><br>
    </el-footer>
    <br><br><br><br><br><br>
  </el-container>
  </transition>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data() {
      return {
        show: false,
        d: {},
        url: 'require("@./assets/head.png")',
        hello: 'Welcome to Your Vue.js App',
        options: [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }, {
          value: '选项4',
          label: '龙须面'
        }, {
          value: '选项5',
          label: '北京烤鸭'
        }],
        value: '',
        input: '',
      }
    },
    methods: {
      onSubmit() {
        this.$router.push({path: '/Detail', query: {input: this.input, d: this.d}});
        this.$axios.post("/api/input/", this.input)
                .then(response => {
                  console.log(response.data)
                })
      },
    },
    created() {
      this.show = true
      this.$axios.get("/api/test/")
        .then(response => {
          this.hello = response.data
          console.log(response.data)
        })
      this.$axios.get("/api/init/")
              .then(response => {
                this.d = response.data
                console.log(response.data)
              })
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-row {
    margin-bottom: 10px;
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .head {
    background-image: url("https://uploader.shimo.im/f/xGuJmIsir3Pd36xC.png");
  }
  .link {
    color: #3a8ee6;
    font-weight: 200;
    text-decoration: none;
  }
</style>