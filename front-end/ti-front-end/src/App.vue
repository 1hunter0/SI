<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import Login from './views/login'

export default {
  name: 'App',
  components: { Login}
}
</script>
