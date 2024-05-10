var currentFile = JSON.parse(localStorage.getItem('file') ?? '{}');
document.addEventListener('DOMContentLoaded', async () => {
    if (currentFile && currentFile !== 'null') {
        const { date, type, clinic, doctor, observations } = currentFile;
        document.getElementById('date').value = date;
        document.getElementById('type').value = type;
        document.getElementById('clinic').value = clinic;
        document.getElementById('doctor').value = doctor;
        document.getElementById('observations').value = observations;
        document.getElementById('submit-file-button').innerHTML = 'Guardar';
    } else {
        document.getElementById('date').value = new Date().toISOString().split('T')[0];
    }
});

// Cancel file form event listener
const cancelFileButton = document.getElementById('cancel-file-button');
if(cancelFileButton) {
    cancelFileButton.addEventListener('click', async (event) => {
        event.preventDefault();
        console.log('Cancelling file form');
        localStorage.setItem('file', null);
        location.href = './index.html';
    });
}

// File form submit event listener
const submiteFileButton = document.getElementById('submit-file-button');
if(submiteFileButton) {
    submiteFileButton.addEventListener('click', async (event) => {
        event.preventDefault();
        console.log('Submitting file form');
        const file = {
            id: currentFile.id,
            date: document.getElementById('date').value,
            type: document.getElementById('type').value,
            clinic: document.getElementById('clinic').value,
            doctor: document.getElementById('doctor').value,
            file: document.getElementById('file').files[0],
            observations: document.getElementById('observations').value,
            fileName: document.getElementById('file').files[0]?.name ?? currentFile.fileName,
        };
        try {
            console.log(currentFile);
            const downloadURL = await uploadFileToFirebaseStorage(file.file) ?? currentFile.fileUrl;
            console.log('File available at', downloadURL);
            const response = !!currentFile.id ? await updateFile({ ...file, fileUrl: downloadURL }) : await createFile({ ...file, fileUrl: downloadURL });
            await response;
            console.log('File uploaded:', response);
            alert('Archivo subido exitosamente');
            location.href = './index.html';
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error subiendo archivo');
        }
    });
}

function createFile(file) {
    axios({
        method: 'POST',
        url: 'http://localhost:3100/upload-file',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        data: file
    });
}

function updateFile(file) {
    axios({
        method: 'PATCH',
        url: 'http://localhost:3100/update-file',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        data: file
    });
}

async function uploadFileToFirebaseStorage(file) {
    if(!file) return null;
    const user = await getUserData();
    const storage = firebase.storage();
    const storageRef = storage.ref();

    const fileExtension = file.name.split('.').pop();
    const uploadTask = storageRef.child(`userFiles/${user.id}/${uuidv4()}.${fileExtension}`).put(file);

    return new Promise((resolve, reject) => {
        uploadTask.on('state_changed', (snapshot) => {
            const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            console.log('Upload is ' + progress + '% done');
            switch (snapshot.state) {
                case firebase.storage.TaskState.PAUSED:
                    console.log('Upload is paused');
                    break;
                case firebase.storage.TaskState.RUNNING:
                    console.log('Upload is running');
                    break;
            }
        }, (error) => {
            reject(error);
        }, async () => {
            uploadTask.snapshot.ref.getDownloadURL().then((downloadURL) => {
                console.log('File available at', downloadURL);
                resolve(downloadURL);
            });
        });
    });
}
