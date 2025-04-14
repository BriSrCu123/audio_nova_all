<template>
  <div class="audio-player">
    <audio v-if="src" :src="src" controls></audio>
    <p v-else>Audio not available</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';

export default defineComponent({
  name: 'AudioPlayer',
  props: {
    src: {
      type: String as PropType<string | null>,
      required: false, // 可选
      default: null, // 默认值为 null
    },
  },
});
</script>

<style scoped>
.audio-player {
  margin: 20px 0;
}
</style>
