<template>
  <div class="optimization-page">
    <h1 class="status-text">已优化</h1>
    <div class="waveform-container">
      <div class="waveform-bar"></div>
      <div class="audio-controls">
        <audio controls class="audio-player">
          <source :src="optimizedAudio || '#'" />
        </audio>
        <span v-if="!optimizedAudio" class="audio-unavailable">Audio not available</span>
      </div>
    </div>
    <button class="download-button" @click="downloadAudio">下载文件</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import AudioPlayer from '../components/AudioPlayer.vue';

export default defineComponent({
  name: 'OptimizationPage',
  components: { AudioPlayer },
  setup() {
    const optimizedAudio = ref<string | null>(null);

    onMounted(() => {
      const audioUrl = localStorage.getItem('optimizedAudio');
      if (audioUrl) {
        optimizedAudio.value = audioUrl;
      }
    });

    const downloadAudio = () => {
      if (optimizedAudio.value) {
        const a = document.createElement('a');
        a.href = optimizedAudio.value;
        a.download = 'optimized_audio.wav';
        a.click();
      }
    };

    return {
      optimizedAudio,
      downloadAudio,
    };
  },
});
</script>

<style scoped>
.optimization-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #5e5e92;
  color: white;
  font-family: 'Arial', sans-serif;
}

.status-text {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.waveform-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #36365c;
  border-radius: 25px;
  padding: 1rem 2rem;
  width: 90%;
  max-width: 800px;
  margin-bottom: 2rem;
}

.waveform-bar {
  width: 100%;
  height: 1.5rem;
  background: linear-gradient(to right, #ff6b6b, #ffd93d, #6bc1ff, #ab47ff);
  border-radius: 10px;
  margin-bottom: 1rem;
}

.audio-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.audio-player {
  width: 100%;
}

.audio-unavailable {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #ffd93d;
}

.download-button {
  background-color: #ffd93d;
  color: #36365c;
  border: none;
  padding: 1rem 2rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.download-button:hover {
  background-color: #ffc107;
}
</style>
