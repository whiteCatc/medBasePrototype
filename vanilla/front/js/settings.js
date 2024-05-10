document.addEventListener('DOMContentLoaded', async () => {
    const userData = await getUserData();
    document.getElementById('name').value = userData.name;
    document.getElementById('curp').value = userData.curp;
    document.getElementById('email').value = userData.email;
    document.getElementById('plan').value = userData.plan;
});

const cancelButton = document.getElementById('cancel-button');
if(cancelButton) {
    cancelButton.addEventListener('click', (event) => {
        event.preventDefault();
        location.href = './index.html';
    });
}

const userForm = document.getElementById('user-form');
if(userForm) {
    userForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const user = {
            name: document.getElementById('name').value,
            curp: document.getElementById('curp').value,
            email: document.getElementById('email').value,
            plan: document.getElementById('plan').value,
        };
        try {
            const response = await updateUser(user);
            alert('Usuario actualizado exitosamente');
            location.href = './index.html';
        } catch (error) {
            console.error('Error updating user:', error);
            alert('Error actualizando usuario');
        }
    });
}

async function updateUser(user) {
    try {
        const response = await axios({
            method: 'PATCH',
            url: 'http://localhost:3100/user',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            data: user
        });
        return response;
    } catch (error) {
        throw error;
    }
}