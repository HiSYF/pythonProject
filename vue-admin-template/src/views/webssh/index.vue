<template>
  <SSH :ip="ip" :height="100" />
</template>

<script>

export default {
  name: 'Xterm',
  components: {
    SSH: () => import('@/components/SSH')
  },
  data() {
    return {
      ip: ''
    }
  },
  mounted() {
    this.ip = this.$route.query.ip //http://localhost:8011/ssh?ip=xxx
  }
}
</script>
