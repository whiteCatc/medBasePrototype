document.addEventListener('DOMContentLoaded', async () => {
    token = localStorage.getItem('token');
    const currentUrl = window.location.href;
    const validUrls = ['login', 'register'];
    console.log('Current URL:', currentUrl);
    if (!token) {
        console.log('No token found');
        if(validUrls.some(url => currentUrl.includes(url))) return;
        if(!validUrls.some(url => currentUrl.includes(url))) {
            console.log('Redirecting to login');
            location.href = './login.html';
        }
    }

    try {
        const response = await axios({
            method: 'GET',
            url: 'http://localhost:3100/validate-token',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
    } catch (error) {
        if(error.message.includes('403')) {
            alert('Sesion expirada, por favor inicia sesion de nuevo');
            localStorage.removeItem('token');
            location.href = './login.html';
        }
    }
});