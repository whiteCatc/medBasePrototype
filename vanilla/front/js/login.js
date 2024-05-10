// Login button event listener
const loginButton = document.getElementById('login-button')
if(loginButton) {
    loginButton.addEventListener('click', async (event) => {
        event.preventDefault();
    
        const curp = document.getElementById('curp')?.value ?? '';
        const password = document.getElementById('password')?.value ?? '';
        try {
            await login(curp, password);
        } catch (error) {
            console.error('Error logging in:', error);
            alert('Credenciales invalidas');
        }
    });
}

async function login(curp, password) {
    console.log('logging in user');
    try {
        const user = await app.firestore().collection('users').doc(curp.toLowerCase()).get();
        if (!user.exists) {
            console.error('User not found');
            throw new Error('Invalid credentials');
        }

        const userData = user.data(); // Get user data from Firestore
        const auth = await app.auth().signInWithEmailAndPassword(userData.email, password);
        console.log('User logged in successfully', auth.user);
        const userToken = await auth.user.getIdToken();
        const response = await axios({
            method: 'POST',
            url: 'http://localhost:3100/login',
            data: {},
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            }
        });
        localStorage.setItem('token', userToken);
        location.href = './index.html';
    } catch (error) {
        console.error('Error logging in fireauth:', error);
        throw new Error('Invalid credentials');
    }
}