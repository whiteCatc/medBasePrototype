document.addEventListener('DOMContentLoaded', async () => {
    try {
        getUserFiles();
        const userData = await getUserData();
        let element = document.getElementById('welcome');
        if(element) element.innerHTML = replaceTextWithVariable(element.innerHTML, 'name', userData.name);
        element = document.getElementById('curp');
        if(element) element.innerHTML = replaceTextWithVariable(element.innerHTML, 'curp', userData.curp);
    } catch (error) {
        console.log('Error getting user data:', error);
        if(error.message.includes('403')) {
            alert('Sesion expirada, por favor inicia sesion de nuevo');
            localStorage.removeItem('token');
            location.href = './login.html';
        }
    }
});

// Add file button event listener
const addFileButton = document.getElementById('add-file-button');
if(addFileButton) {
    addFileButton.addEventListener('click', async (event) => {
        event.preventDefault();
        localStorage.setItem('file', null);
        location.href = './file-form.html';
    });
}

async function getUserFiles() {
    try {
        const response = await axios({
            method: 'GET',
            url: 'http://localhost:3100/user-files',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        const userFiles = response.data;
        console.log('User files:', userFiles);
        const filesList = document.getElementById('file-records-tbody');
        const cols = ['clinic', 'doctor', 'observations']
        userFiles.forEach((file) => {
            const fileRow = document.createElement('tr');
            cols.forEach((col) => {
                const fileCol = document.createElement('td');
                fileCol.innerHTML = file[col];
                fileRow.appendChild(fileCol);
            });
            const actionsTd = document.createElement('td');
            const viewButton = document.createElement('button');
            viewButton.innerHTML = 'Ver';
            viewButton.addEventListener('click', async () => {
                localStorage.setItem('file', JSON.stringify(file));
                location.href = './file-form.html';
            });
            actionsTd.appendChild(viewButton);
            fileRow.appendChild(actionsTd);
            filesList.appendChild(fileRow);
        });
    } catch (error) {
        throw error;
    }
}