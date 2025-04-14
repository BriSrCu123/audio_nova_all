<template>
  <div class="separation-page">
    <h1 class="title">已分离</h1>
    <div v-for="(audio, index) in separatedAudio" :key="index" class="audio-track">
      <div class="track-header">
        <span>{{ audioLabels[index] }}</span>
        <div class="waveform"></div>
      </div>
      <audio :src="audio" controls class="audio-player"></audio>
      <div class="selectors">
        <label class="selector">
          音色选择：
          <select v-model="selectedTimbres[index]">
            <option value="" disabled>请选择音色</option>
            <option value="音色1">音色1</option>
            <option value="音色2">音色2</option>
            <option value="音色3">音色3</option>
          </select>
        </label>
        <label class="selector">
          音量调节：
          <input type="range" v-model="volumeLevels[index]" min="0" max="1" step="0.01" />
        </label>
      </div>
    </div>

    <!-- 风格选择和开始优化按钮 -->
    <div class="style-and-button">
      <label class="selector">
        风格选择：
        <select v-model="selectedStyle">
          <option value="" disabled>请选择风格</option>
          <option value="pop">流行</option>
          <option value="rock">摇滚</option>
          <option value="jazz">爵士</option>
        </select>
      </label>
      <button :disabled="!isReadyForOptimization" @click="startOptimization" class="start-button">
        开始优化
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
//import AudioPlayer from '../components/AudioPlayer.vue';

export default defineComponent({
  name: 'SeparationPage',
 //components:{AudioPlayer},
  setup() {
    const separatedAudio = ref<string[]>([
      '音轨1.mp3',
      '音轨2.mp3',
      '音轨3.mp3',
      '音轨4.mp3'
    ]);
    const audioLabels = ['人声', '钢琴', '吉他', '鼓声'];
    const selectedTimbres = ref<string[]>(Array(separatedAudio.value.length).fill(''));
    const selectedStyle = ref('');
    const volumeLevels = ref<number[]>(Array(separatedAudio.value.length).fill(1)); // 默认音量为1 (最大)
    const router = useRouter();

    // 检查是否所有音色都已选择，风格是否选择
    const isReadyForOptimization = computed(() =>
      selectedTimbres.value.every(timbre => timbre !== '') &&
      selectedStyle.value !== ''
    );

    const startOptimization = async () => {
      const formData = new FormData();
      // 将音频文件和音色、风格、音量信息添加到 formData
      separatedAudio.value.forEach((audio, index) => {
        formData.append(`audio_${index}`, audio);
        formData.append(`timbre_${index}`, selectedTimbres.value[index]);
        formData.append(`style`, selectedStyle.value); // 使用选中的风格
        formData.append(`volume_${index}`, volumeLevels.value[index].toString()); // 添加音量信息
      });

      try {
        const response = await fetch('http://127.0.0.1:5000/api/optimization', {
          method: 'POST',
          body: formData,
        });

        // 如果请求成功，获取返回的优化音频文件并跳转
        if (response.ok) {
          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          localStorage.setItem('optimizedAudio', url); // 存储优化后的音频URL
          router.push('/optimization'); // 跳转到优化页面并播放音频
        } else {
          alert('优化时发生错误。');
        }
      } catch (error) {
        console.error('请求失败:', error);
        alert('请求失败，请稍后再试。');
      } finally {
        router.push('/optimization');
      }
    };

    return {
      separatedAudio,
      audioLabels,
      selectedTimbres,
      selectedStyle,
      volumeLevels,
      isReadyForOptimization,
      startOptimization,
    };
  },
});
</script>

<style scoped>
.separation-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #5e5e92;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.title {
  font-size: 24px;
  color: #ffffff;
  margin-bottom: 20px;
}

.audio-track {
  width: 90%;
  background: #36365c;
  margin-bottom: 15px;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  color: #ffffff;
  display: flex;
  flex-direction: column;
}

.track-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.track-header span {
  font-size: 18px;
  font-weight: bold;
}

.waveform {
  flex-grow: 1;
  height: 10px;
  background: linear-gradient(to right, #ff6b6b, #ffd93d, #6bc1ff, #ab47ff);
  border-radius: 5px;
}

.audio-player {
  margin: 10px 0;
  width: 100%;
}

.selectors {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.selector {
  font-size: 14px;
  margin-right: 10px;
}

input[type="range"], select {
  margin-top: 5px;
  padding: 5px;
  border-radius: 5px;
  border: none;
  background: #444466;
  color: #ffffff;
  outline: none;
}

select:focus, input[type="range"]:focus {
  border: 1px solid #ffd93d;
}

.style-and-button {
  display: flex;
  justify-content: space-between;
  width: 90%;
  margin-top: 20px;
}

.start-button {
  padding: 10px 20px;
  font-size: 16px;
  background: #ffd93d;
  color: #36365c;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.3s;
}

.start-button:disabled {
  background: #999999;
  cursor: not-allowed;
}

.start-button:hover:not(:disabled) {
  background: #ffc107;
}
</style>
