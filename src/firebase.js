// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from 'firebase/auth';

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBTqd4oEyw9y-2FSsvaI1ryatmGJg4SFRo",
  authDomain: "final-project-b03d6.firebaseapp.com",
  projectId: "final-project-b03d6",
  storageBucket: "final-project-b03d6.appspot.com",
  messagingSenderId: "321009636869",
  appId: "1:321009636869:web:cf5630518155dfad03ae6c",
  measurementId: "G-YE9HMNWV0L"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged };