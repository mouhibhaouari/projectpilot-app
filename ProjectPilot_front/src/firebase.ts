import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth"
import { getFirestore } from "firebase/firestore"

const firebaseConfig = {
  apiKey: "AIzaSyC3iv_mQMzIfwr3IxVRWjdptjyIjlcH_LU",
  authDomain: "aiprojectpilot.firebaseapp.com",
  projectId: "aiprojectpilot",
  storageBucket: "aiprojectpilot.firebasestorage.app",
  messagingSenderId: "410918673107",
  appId: "1:410918673107:web:3ca5276b3d1c0204139226",
  measurementId: "G-8EV5EXJFFF"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app)
export const db = getFirestore(app)
export default app