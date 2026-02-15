import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyCFzIzEA-TWZR2Cn5uP5V-QBm51EpyRA8A",
  authDomain: "career-assistant-e706b.firebaseapp.com",
  projectId: "career-assistant-e706b"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export default app;
