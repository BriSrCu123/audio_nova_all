import { createRouter, createWebHistory } from 'vue-router';
import UploadPage from '../pages/UploadPage.vue';
import SeparationPage from '../pages/SeparationPage.vue';
import OptimizationPage from '../pages/OptimizationPage.vue';

const routes = [
  { path: '/', component: UploadPage },
  { path: '/separation', component: SeparationPage },
  { path: '/optimization', component: OptimizationPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

console.log('Router config:', routes);




