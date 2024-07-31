import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '../views/HelloWorld.vue';
import Login from '../views/LoginForm.vue';
import UserDashboard from '../views/UserDashboard.vue';
import LibDashboard from '../views/LibDashboard.vue';
import Register from '../views/RegisterForm.vue';
import CreateSection from '../views/CreateSection.vue';
import EditSection from '../views/EditSection.vue';
import AddBook from '../views/AddBook.vue';
import EditBook from '../views/EditBook.vue';
import LibHome from '../views/LibHome.vue';
import UserManagement from '../views/UserManagement.vue'
import UserHome from '../views/UserHome.vue'
import UserProfile from '../views/UserProfile.vue'
import AddSecondarySection from '../views/AddSecondarySection.vue'
import DelSecondarySection from '../views/DelSecondarySection.vue'
import BookContent from '../views/BookContent.vue'
const routes = [
  {
    path: '/',
    name: 'HelloWorld',
    component: HelloWorld
  },
  {path:'/login',
    name: 'login',
    component: Login
  },
  {path:'/user-dashboard',
    name: 'user-dashboard',
    component: UserDashboard,
    children:[
      {
        path:'',
        name:'user-home',
        component:UserHome
      },
      {
        path:'profile',
        name:'profile',
        component:UserProfile
      },
      {
        path: '/book/:id',
        name: 'BookContent',
        component: BookContent,
        props: true
      }
    
    ]

  },
  {
    path:'/lib-dashboard',
    name:'lib-dashboard',
    component:LibDashboard,
  
    children:[
      { 
        path:'',
        name:'lib-home',
        component:LibHome
      }
      ,

      {
          path: 'Create-Section',
          name: 'lib-create-section',
          component: CreateSection
      },
      {
        path: 'Edit-Section/:id',
        name: 'lib-edit-section',
        component: EditSection,
        props: true
      },
      {
        path:'Add-Book/:sectionId',
        name:'lib-add-book',
        component:AddBook,
        props:true
      },
      {
        path:'Edit-Book/:bookId/:sectionId',
        name:'lib-edit-book',
        component:EditBook,
        props:true
      },
      {
        path:'lib-add-secondary-section/:bookId/:sectionId',
        name:'lib-add-secondary-section',
        component:AddSecondarySection,
        props:true
      },
      {
        path:'lib-del-secondary-section/:bookId/:sectionId',
        name:'lib-del-secondary-section',
        component:DelSecondarySection,
        props:true
      },
      {
        path:'User-Management',
        name:'lib-user-management',
        component:UserManagement
      }
      

    ]
  },
{
  path:'/register',
  name:'register',
  component: Register
}
  
  // Add more routes here
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
