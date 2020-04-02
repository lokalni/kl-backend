import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter);


export const ROUTE_NAMES = {
  MAIN: 'main',
  TEACHER_GROUPS: 'teacher-groups',
  TEACHER_GROUP_DETAIL: 'teacher-group-details',
  LIMBO: 'student-limbo',
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
  }
];

const router = new VueRouter({
  routes
});

export default router
