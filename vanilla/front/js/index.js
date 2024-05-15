document.addEventListener('DOMContentLoaded', async () => {
    getUserFiles();
    const userData = await getUserData();
    let element = document.getElementById('welcome');
    if(element) element.innerHTML = replaceTextWithVariable(element.innerHTML, 'name', userData.name);
    element = document.getElementById('curp');
    if(element) element.innerHTML = replaceTextWithVariable(element.innerHTML, 'curp', userData.curp);
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

            const editButton = document.createElement('button');
            editButton.innerHTML = 'Editar';
            editButton.addEventListener('click', async () => {
                localStorage.setItem('file', JSON.stringify(file));
                location.href = './file-form.html';
            });
            
            const downloadFileButton = document.createElement('button');
            downloadFileButton.innerHTML = 'Ver archivo';
            downloadFileButton.addEventListener('click', async () => {
                const link = document.createElement('a');
                link.href = file.fileUrl;
                link.target = '_blank';
                link.download = file.fileName;
                link.click();
            });

            const deleteFileButton = document.createElement('button');
            deleteFileButton.innerHTML = 'Eliminar';
            deleteFileButton.addEventListener('click', async () => {
                try {
                    if(confirm('¿Estas seguro que deseas eliminar este archivo?')) {
                        try {
                            await axios({
                                method: 'DELETE',
                                url: 'http://localhost:3100/delete-file',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'Authorization': `Bearer ${token}`
                                },
                                data: {
                                    filePath: file.filePath
                                }
                            });
                            alert('Archivo eliminado exitosamente');
                            window.location.reload();
                        } catch (error) {
                            alert('Error eliminando archivo');
                        }
                    }
                } catch (error) {
                    console.error('Error deleting file:', error);
                    alert('Error eliminando archivo');
                }
            });
            
            const actionsTd = document.createElement('td');
            actionsTd.appendChild(editButton);
            actionsTd.appendChild(downloadFileButton);
            actionsTd.appendChild(deleteFileButton);
            fileRow.appendChild(actionsTd);
            filesList.appendChild(fileRow);
        });
    } catch (error) {
        throw error;
    }
}