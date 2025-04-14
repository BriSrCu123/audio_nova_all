<template>
  <div class="upload-page">
    <h1 class="title">声音分离器</h1>
    <p class="description">对上传的音频进行识别并分离，为您分离出纯净的干声。</p>
    <div class="waveform-preview">
      <div class="wave music"></div>
      <div class="wave vocal"></div>
    </div>
    <div class="actions">
      <input
        type="file"
        id="file-input"
        class="file-input"
        @change="onFileChange"
        multiple
        accept=".wav"
      />
      <label for="file-input" class="custom-button">选择文件</label>
      <button class="custom-button" :disabled="!files.length" @click="startSeparation">
        开始分离
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'UploadPage',
  setup() {
    const files = ref<File[]>([]);
    const router = useRouter();

    const onFileChange = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files) {
        files.value = Array.from(input.files);
      }
    };

    const startSeparation = async () => {
      const formData = new FormData();
      files.value.forEach((file) => formData.append('audio', file));

      try {
        const response = await fetch('http://127.0.0.1:5000/api/separation', {
          method: 'POST',
          body: formData,
        });
        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('separatedAudio', JSON.stringify(data.audioPaths));
          router.push('/separation');
        } else {
          alert('Error during separation.');
        }
      } catch (error) {
        console.error('Error:', error);
      } finally {
        router.push('/separation');
      }
    };

    return {
      files,
      onFileChange,
      startSeparation,
    };
  },
});
</script>

<style>
.upload-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #6b5b95;
  color: #ffffff;
  padding: 40px;
  font-family: 'Arial', sans-serif;
  height: 100vh;
  box-sizing: border-box;
}

.title {
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 20px;
}

.description {
  font-size: 1.2em;
  margin-bottom: 30px;
  text-align: center;
  max-width: 500px;
}

.waveform-preview {
  display: flex;
  flex-direction: column;
  width: 80%;
  max-width: 600px;
  margin-bottom: 30px;
}

.wave {
  height: 50px;
  background-color: rgba(255, 255, 255, 0.3);
  margin: 5px 0;
  border-radius: 5px;
  position: relative;
}

.music::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 60%;
  height: 100%;
  background-color: #ffcccb;
  border-radius: 5px;
}

.vocal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 80%;
  height: 100%;
  background-color: #90ee90;
  border-radius: 5px;
}

.actions {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.file-input {
  display: none;
}

.custom-button {
  background-color: #ffffff;
  color: #6b5b95;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  font-weight: bold;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.custom-button:hover {
  background-color: #d1c4e9;
}

.custom-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
