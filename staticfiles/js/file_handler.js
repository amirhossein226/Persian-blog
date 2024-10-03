function fileHandler(cb, value, meta) {
    const csrftoken = getCsrfToken();

    console.log(csrftoken);

    const input = document.createElement('input');

    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*,video/*');

    //event listeners
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];


        const formData = new FormData();
        formData.append('file', file);
        formData.append('post_id', document.querySelector('.action.delete').dataset['id']);

        const url = '/file_url_constructor/';
        const options = {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        }


        fetch(url, options)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("File added successfully!")

                    cb(data.url, { title: file.name })
                } else {
                    console.error('Upload failed:', data.error);

                }
            })
            .catch(error => {
                console.error('error', error)
            });
    });
    input.click();
}