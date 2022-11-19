<template>
  <div>
    <router-link :to="{
      name: 'Ip',
      query: {
        ip: '107.52.172.11'
      }
    }">
    107.52.172.11
    </router-link>
  </div>
</template>

<script>
export default {
  name: "DNS",

}
</script>

<style>

</style>
