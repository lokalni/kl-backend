import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import store from '@/store';

Vue.use(VueRouter);


export const ROUTE_NAMES = {
  MAIN: 'main',
  TEACHER_GROUPS: 'teacher:groups',
  TEACHER_GROUP_DETAIL: 'teacher:group-details',
  LIMBO: 'student:limbo',
  ADMIN_MODERATORS: 'admin:moderators',
};

const routes = [
  // Teacher namespace
  {
    path: '/',
    name: ROUTE_NAMES.MAIN,
    component: Home
  },
  {
    path: '/groups',
    name: ROUTE_NAMES.TEACHER_GROUPS,
    component: () => import('../views/teacher/TeacherGroups.vue'),
  },
  // TODO - consider nested routes
  {
    path: '/groups/:id',
    name: ROUTE_NAMES.TEACHER_GROUP_DETAIL,
    component: () => import('../views/teacher/TeacherGroupDetail.vue'),
  },

  // Student namespace
  {
    path: '/limbo',
    name: ROUTE_NAMES.LIMBO,
    component: () => import('../views/student/Limbo.vue'),
  },

  // Admin namespace
  {
    path: '/moderators',
    name: ROUTE_NAMES.ADMIN_MODERATORS,
    component: () => import('../views/admin/ManageModerators.vue'),
  },
];

const router = new VueRouter({
  routes
});

router.beforeEach(async (to, from, next) => {
  if (to.name === ROUTE_NAMES.MAIN) {
    return next();
  }
  window.console.log("Updating session");
  try {
    await store.dispatch('updateSession');
  } catch (e) {
    window.console.log("Updating session failed.");
    return next({name: ROUTE_NAMES.MAIN});
  }
  next();
});

export default router
