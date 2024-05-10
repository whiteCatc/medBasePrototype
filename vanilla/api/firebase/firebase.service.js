const admin = require('firebase-admin'); // Import Firebase Admin SDK; npm install firebase-admin
const serviceJson = require('./medbase-37455-firebase-adminsdk-ktrsh-b4b7a7bfa8.json'); // Import the serviceAccountKey.json file; This is the file that you download from Firebase Console

// Initialize Firebase Admin SDK
admin.initializeApp({
    credential: admin.credential.cert(serviceJson)
});

const firestore = admin.firestore(); // Initialize Firestore
const auth = admin.auth(); // Initialize Auth

module.exports = { admin, firestore, auth }; // Export the admin, firestore, and auth objects