var token = localStorage.getItem('token');

function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function replaceTextWithVariable(text, variable, value) {
    console.log('Replacing text with variable:', variable, value);
    const regex = new RegExp(`{{${variable}}}`, 'g');
    return text.replace(regex, value);
}

async function getUserData() {
    try {
        const response = await axios({
            method: 'GET',
            url: 'http://localhost:3100/user-data',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        console.log('User data:', response.data);
        return response.data;
    } catch (error) {
        throw error;
    }
}