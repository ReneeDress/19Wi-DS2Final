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
            <br>
        </el-main>
<!--        <el-row :span="24" class="line-content bg-purple"></el-row>-->
        <el-row :gutter="20" v-show="show">
            <el-col :span="17" :offset="1"><div class="grid-content" style="text-align: left">
                <el-container direction="vertical">
                    <el-tag style="text-align: center; width: 12em;">释义等摘自金山词霸</el-tag>
                    <br>
                    <el-row class="word">{{word}}</el-row>
                    <el-row class="phonetic">
                        <el-col :span="9" v-for="o in phonetic" :key="o" class="text item">{{o}}</el-col>
                    </el-row>
                    <el-row class="meaning">
                        <el-col :span="17" v-for="o in meaning" :key="o" class="meaning item">{{o}}</el-col>
                    </el-row>
                </el-container>
                <el-collapse>
                    <el-collapse-item title="词性转换">
                        <br>
                        <div><el-row class="exchange">
                            <el-col :span="10" v-for="o in exchange" :key="o" class="text item">{{o}}</el-col>
                        </el-row></div>
                    </el-collapse-item>
                    <el-collapse-item title="语料库例句">
                        <br>
                        <div v-for="o in example" :key="o" class="text">
                            <p v-html="o[0]">{{o[0]}}</p>
                            <p v-if="o[1]" class="from item">出自 {{o[1]}}</p>
                        </div>
                    </el-collapse-item>
                    <el-collapse-item title="同义词">
                        <br>
                        <div v-for="o in synonym" :key="o" class="text item">
                            {{o[0]}}<br><span style="color: #3a8ee6; font-weight: 200; font-style: italic">{{o[1] + " "}}</span>
                        </div>
                    </el-collapse-item>
                    <el-collapse-item title="反义词">
                        <br>
                        <div v-for="o in antonym" :key="o" class="text item">
                            {{o[0]}}<br><span style="color: #3a8ee6; font-weight: 200; font-style: italic">{{o[1] + " "}}</span>
                        </div>
                    </el-collapse-item>
                </el-collapse>
            </div></el-col>
            <el-col :span="5"><div class="grid-content bg-purple-light">
                <br><p>上海大学计算机工程与科学学院</p>
                <p>数据结构(2)课程作业</p>
                <br>
                <el-image :src="require('../assets/Sign.png')" style="width: 96%"></el-image>
                <br>
                <p>作者：林艺珺 18120189</p><br>
            </div></el-col>
        </el-row>
        <br><br><br><br><br><br>
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
    import qs from 'qs'
    export default {
        name: "Detail",
        data() {
          return {
              show: false,
              d: {},
              url: 'require("@./assets/head.png")',
              input: '',
              word: '感谢使用',
              phonetic: ['英[没有内容呢]', '美[也没有内容呢]'],
              meaning: ['啊噢~ 没有你要找的单词呢~是不是输错啦~Σ(oﾟдﾟoﾉ)'],
              exchange: ['啊噢~', '没有你要找的单词呢~', '是不是输错啦~', 'Σ(oﾟдﾟoﾉ)'],
              example: [['这是一句语料库里的例句', '这是例句的出处(Info的标题)']],
              synonym: [['啊噢~没有你要找的单词呢~', '是不是输错啦~Σ(oﾟдﾟoﾉ)']],
              antonym: [['啊噢~没有你要找的单词呢~', '是不是输错啦~Σ(oﾟдﾟoﾉ)']],
          }
        },
        created() {
            var word = this.$route.query.input
            var d = this.$route.query.d
            this.word = word
            this.d = d
            this.show = true
            this.$axios.post("/api/dict/", this.word)
                .then(response => {
                    this.phonetic = response.data['phonetic']
                    this.meaning = response.data['meaning']
                    this.exchange = response.data['exchange']
                    if (this.exchange == '') this.exchange = ['暂无词性转换']
                    this.synonym = response.data['synonym']
                    if (this.synonym == '') this.synonym = [['暂无同义词', '']]
                    this.antonym = response.data['antonym']
                    if (this.antonym == '') this.antonym = [['暂无反义词', '']]
                    console.log(this.example)
                    console.log(response.data)
                })
            this.$axios.post("/api/resplit/", qs.stringify({d: this.d[this.word], word: this.word}))
                .then(response => {
                    this.example = response.data['example']
                    if (this.example == '') this.example = [['语料库暂无收录该词例句']]
                    console.log(this.example)
                    console.log(response.data)
                })
        },
        beforeMount() {

        },
        mounted() {
            var word = this.$route.query.input
            var d = this.$route.query.d
            this.word = word
            this.d = d
            this.$axios.post("/api/dict/", this.word)
                .then(response => {
                    this.phonetic = response.data['phonetic']
                    this.meaning = response.data['meaning']
                    this.exchange = response.data['exchange']
                    if (this.exchange == '') this.exchange = ['暂无词性转换']
                    this.synonym = response.data['synonym']
                    if (this.synonym == '') this.synonym = [['暂无同义词', '']]
                    this.antonym = response.data['antonym']
                    if (this.antonym == '') this.antonym = [['暂无反义词', '']]
                    console.log(this.example)
                    console.log(response.data)
                })
            this.$axios.post("/api/resplit/", qs.stringify({d: this.d[this.word], word: this.word}))
                .then(response => {
                    this.example = response.data['example']
                    if (this.example == '') this.example = [['语料库暂无收录该词例句']]
                    console.log(this.example)
                    console.log(response.data)
                })
        },
        methods: {
            onSubmit() {
                this.phonetic = ['英[没有内容呢]', '美[也没有内容呢]']
                this.meaning = ['啊噢~ 没有你要找的单词呢~是不是输错啦~Σ(oﾟдﾟoﾉ)']
                this.exchange = ['啊噢~', '没有你要找的单词呢~', '是不是输错啦~', 'Σ(oﾟдﾟoﾉ)']
                this.example = [['这是一句语料库里的例句', '这是例句的出处(Info的标题)']]
                this.synonym = [['啊噢~没有你要找的单词呢~', '是不是输错啦~Σ(oﾟдﾟoﾉ)']]
                this.antonym = [['啊噢~没有你要找的单词呢~', '是不是输错啦~Σ(oﾟдﾟoﾉ)']]
                this.word = this.input
                this.$router.push({path: '/Detail', query: {input: this.input, d: this.d}})
                this.$axios.post("/api/input/", this.input)
                    .then(response => {
                        console.log(response.data)
                    })
                this.$axios.post("/api/dict/", this.word)
                    .then(response => {
                        this.phonetic = response.data['phonetic']
                        this.meaning = response.data['meaning']
                        this.exchange = response.data['exchange']
                        if (this.exchange == '') this.exchange = ['暂无词性转换']
                        this.synonym = response.data['synonym']
                        if (this.synonym == '') this.synonym = [['暂无同义词', '']]
                        this.antonym = response.data['antonym']
                        if (this.antonym == '') this.antonym = [['暂无反义词', '']]
                        console.log(this.example)
                        console.log(response.data)
                    })
                this.$axios.post("/api/resplit/", qs.stringify({d: this.d[this.word], word: this.word}))
                    .then(response => {
                        this.example = response.data['example']
                        if (this.example == '') this.example = [['语料库暂无收录该词例句']]
                        console.log(this.example)
                        console.log(response.data)
                    })
            },
        }
    }
</script>

<style>
    .el-row {
        margin-bottom: 20px;
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
    .line-content {
        border-radius: 4px;
        min-height: 3px;
    }
    .row-bg {
        padding: 10px 0;
        background-color: #f9fafc;
    }
    .text {
        font-size: 18px;
    }

    .item {
        margin-bottom: 18px;
    }

    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }
    .clearfix:after {
        clear: both
    }

    .box-card {
        margin-bottom: 20px;
    }
    .el-collapse-item__header {
        font-size: 20px;
        padding-left: 4px;
    }
    .word {
        font-size: 50px;
        font-weight: 500;
    }
    .meaning {
        font-size: 18px;
        font-weight: 400;
    }
    .from {
        font-size: 13px;
        font-style: italic;
        font-weight: 100;
        text-align: right;
    }
    .highlight {
        color: #3a8ee6;
        font-weight: 800;
    }
    .link {
        color: #3a8ee6;
        font-weight: 200;
        text-decoration: none;
    }
</style>