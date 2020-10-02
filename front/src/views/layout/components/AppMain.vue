<template>
  <section class="app-main">
    <transition name="fade-transform" mode="out-in">
      <div>
        <router-view/>
      </div>
    </transition>
  </section>
</template>

<script>

export default {
  name: 'AppMain',
  data () {
    return {
    }
  },
  computed: {
  },
  methods: {
  },
  mounted () {
    console.log('!!!!!', this.$route.name)
  }

}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.app-main {
  min-height: calc(100vh - 50px);
  position: relative;
  overflow: hidden;
}

.el-tabs__nav {
  float: right !important;
}
.main_tab_menu {
  margin: 0;
  /* border-bottom: 1px solid #cdcdcd;*/
  .active {
    border-bottom: 4px solid #409eff;
  }
  li {
    display: inline-block;
    margin: 0 5px;
    padding: 0 10px;
    height: 40px;
    box-sizing: border-box;
    line-height: 40px;
    display: inline-block;
    list-style: none;
    font-size: 16px;
    font-weight: 500;
    color: #303133;
    position: relative;
    cursor: pointer;
  }
}
</style>
