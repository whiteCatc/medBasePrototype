const registerButton = document.getElementById('register-button')
if(!!registerButton) {
    registerButton.addEventListener('click', async (event) => {
        console.log('registering user');
        event.preventDefault();
    
        const curp = document.getElementById('curp')?.value ?? '';
        const name = document.getElementById('name')?.value ?? '';
        const email = document.getElementById('email')?.value ?? '';
        const password = document.getElementById('password')?.value ?? '';
    
        try {
            const user = await app.auth().createUserWithEmailAndPassword(email, password);
            await app.firestore().collection('users').doc(curp.toLowerCase()).set({
                id: user.user.uid,
                name,
                email,
                curp: curp.toLowerCase(),
                createdAt: new Date().toISOString(),
                role: 'user'
            });
            console.log('User registered successfully', user);
            await app.firestore().collection('users').doc(user.user.uid).set({
                curp: curp.toLowerCase()
            });
            console.log('User registered successfully', user);
            alert('Usuario registrado exitosamente');
            await login(curp, password);
        } catch (error) {
            console.error('Error registering user:', error);
            throw new Error('Error registering user');
        }
    });
}