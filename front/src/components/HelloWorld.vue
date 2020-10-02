<template>
  <div class="hello">
    <v-chart id="logo" :options="echartsOptions" autoresize theme="ovilia-green"/>
  </div>
</template>

<script>
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/line'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/title'
import 'echarts/lib/component/visualMap'
import 'echarts/lib/component/dataset'

import { mapState, mapActions } from 'vuex'
// import { polar } from './data.js'

export default {
  name: 'HelloWorld',
  components: {
    'v-chart': ECharts
  },
  props: {
    msg: String
  },
  data () {
    return {
      loading: false,
      echartsOptions: {
        tooltip: {
          // trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: []
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: []
      }
    }
  },
  computed: {
    ...mapState('speciality', ['speciality_data'])
  },
  mounted () {
    this.loading = false
    this.loadSpecialityData({ year: 2020, month: 8 }).then((data) => {
      console.log('data', data)
      this.echartsOptions.xAxis.data = data.labels
      this.echartsOptions.legend.data = data.specialties
      this.echartsOptions.series = data.series
      this.loading = false
    })
  },
  methods: {
    ...mapActions('speciality', ['loadSpecialityData'])
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  #logo {
    display: inline-block;
    width: 100%;
    height: 600px;
  }

</style>
