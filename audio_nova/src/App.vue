<!-- eslint-disable vue/no-export-in-script-setup -->
<!-- src/App.vue -->
<template>
  <div id="app">
    <router-view /> <!-- 渲染路由组件 -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});


</script>



