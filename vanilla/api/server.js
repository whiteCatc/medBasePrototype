
require('dotenv').config();
const cors = require('cors');
const express = require('express');
const app = express();
app.use(cors());
const { admin, firestore, auth } = require('./firebase/firebase.service'); // Import the admin, firestore, and auth objects from the firebase.service.js file

// Middleware to authenticate requests using Firebase Tokens
const authenticate = async (req, res, next) => {
    const token = req.headers.authorization;
    if (!token || !token.startsWith('Bearer ')) {
        return res.status(401).send('Unauthorized access');
    }

    try {
        const decodedToken = await auth.verifyIdToken(token.split('Bearer ')[1]);
        req.user = decodedToken; // Add decoded token to request for use in your route
        next(); // Proceed to the next middleware or route handler
    } catch (error) {
        console.error('Error verifying authentication token', error);
        res.status(403).send('Invalid authentication token');
    }
};

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const port = process.env.PORT || port;

app.get('/validate-token', authenticate, (req, res) => {
    res.send('Token is valid');
});

// this endpoint only returns a message that confirms that the token is valid
app.post('/login', authenticate, async (req, res) => {
    try {
        res.send('User logged in successfully');
    } catch (error) {
        console.error('Error logging in user:', error);
        throw error;
    }
});
// this endpoint will return the user data from the database using the user's uid based on the token
app.get('/user-data', authenticate, async (req, res) => {
    try {
        const userDataCurp = await firestore.collection('users').doc(req.user.uid).get();
        const { curp } = userDataCurp.data();
        const userData = await firestore.collection('users').doc(curp).get();
        res.send(userData.data());
    } catch (error) {
        console.error('Error getting user data:', error);
        throw error;
    }
});
// this endpoint will upload a file to the database using the user's uid based on the token
app.post('/upload-file', authenticate, async (req, res) => {
    try {
        const userDataCurp = await firestore.collection('users').doc(req.user.uid).get();
        const { curp } = userDataCurp.data();
        const userData = await firestore.collection('users').doc(curp).get();
        const { id } = userData.data();
        const { date, type, clinic, doctor, observations, fileName, fileUrl } = req.body;
        await firestore.collection('files').add({
            id: uuidv4(),
            date,
            type,
            clinic,
            doctor,
            observations,
            fileName,
            fileUrl,
            userId: id
        });
        res.send('File uploaded successfully');
    } catch (error) {
        console.error('Error uploading file:', error);
        throw error;
    }
});
app.patch('/update-file', authenticate, async (req, res) => {
    try {
        const { id, date, type, clinic, doctor, observations, fileName, fileUrl } = req.body;
        const fileFound = await firestore.collection('files').where('id', '==', id).get();
        const file = fileFound.docs.pop();
        await file.ref.update({
            date,
            type,
            clinic,
            doctor,
            observations,
            fileName,
            fileUrl
        });
        res.send('File updated successfully');
    } catch (error) {
        console.error('Error updating file:', error);
        throw error;
    }
});
// this endpoint will get the user files from the database using the user's uid based on the token
app.get('/user-files', authenticate, async (req, res) => {
    try {
        const userId = req.user.uid;
        const userFiles = await firestore.collection('files').where('userId', '==', userId).get();
        const files = [];
        userFiles.forEach((file) => {
            files.push(file.data());
        });
        res.send(files);
    } catch (error) {
        console.error('Error getting user files:', error);
        throw error;
    }
});

app.listen(port, () => console.log(`listening on http://localhost:${port}`));
