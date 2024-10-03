document.addEventListener('DOMContentLoaded', () => {

    const csrftoken = window.getCsrfToken();
    post_options = {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    };

    document.querySelector('.action.delete').addEventListener('click', function () {
        deletePost(csrftoken, post_options, this);
    })



})

function deletePost(csrftoken, post_options, deleteBtn) {

    const post_id = deleteBtn.dataset.id;

    let confirmBox = document.querySelector('#confirmation');
    let confirmBtn = confirmBox.lastElementChild;
    confirmBox.children[1].firstElementChild.innerText = 'از حذف این پست اطمینان دارید؟'
    confirmBox.style.display = 'block';

    const confirmHandler = function () {
        confirmBox.style.display = 'none';

        // request body:
        let formData = new FormData();
        formData.append('id', post_id);
        post_options['body'] = formData;

        fetch('/posts/delete/', post_options)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data['status'] === 'ok') {
                    // if the action applied to the post was deletion and if the deletion was successful, we will hide the related post
                    const targetId = deleteBtn.dataset.targetid;

                    const postsContainer = document.querySelector(`#post-${targetId}`);

                    if (postsContainer) {
                        // set the post container's display to none
                        postsContainer.style.display = 'none';

                    }

                    // create message box
                    const parentDiv = document.createElement('div');
                    parentDiv.innerHTML = `
                        <p>پست مورد نظر با موفقیت حذف گردید.</p>
                    `;

                    parentDiv.setAttribute('class', 'js-message');

                    // going to check if user is on post detail page or not, if the user is on post detail page, then redirect it to post list page
                    let currentPageLocation = document.location.href;

                    document.body.appendChild(parentDiv);

                    const detailPagePattern = /\/posts\/\d{4}\/(\d{1}|\d{2})\/(\d{1}|\d{2})/ig
                    if (currentPageLocation.match(detailPagePattern)) {
                        parentDiv.innerHTML = `
                        <p>پست مورد نظر با موفقیت حذف گردید.در حال انتقال به صفحه ی پست ها....</p>
                        `;
                        setTimeout(
                            () => window.location.href = '/posts/',
                            3000
                        )
                    }


                }
            })

        confirmBtn.removeEventListener('click', confirmHandler);

    };
    confirmBtn.addEventListener('click', confirmHandler);
}