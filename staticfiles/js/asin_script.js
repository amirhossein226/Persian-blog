document.addEventListener('DOMContentLoaded', (event) => {

    // getting the csrftoken using getCsrfToken function which defined at the end of this file
    const csrftoken = getCsrfToken()

    // for post requests
    var post_options = {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    }
    // for get requests
    var get_options = {
        method: 'GET',
        headers: { 'X-CSRFToken': csrftoken },
        mode: "same-origin"
    }

    let archiveAnchors = document.querySelectorAll('a.archive');
    if (archiveAnchors) {
        archiveAnchors.forEach(arch => {
            arch.addEventListener('click', function (e) {
                e.preventDefault();
                let archiveButton = arch;
                checkAuth(post_options).then(loggedIn => {
                    if (loggedIn) {
                        sendArchiveRequest(archiveButton, post_options);
                    }
                    else {
                        const nextUrl = encodeURIComponent(document.location.href);
                        window.location.href = `/accounts/login/?next=${nextUrl}`;
                    }
                })


            })
        })
    }


    // manage click on like button
    let likeAnchor = document.querySelector('a.like');
    if (likeAnchor) {
        likeAnchor.addEventListener('click', function (e) {
            e.preventDefault();

            // check whether the user is authenticated or not:
            var likeButton = this;
            checkAuth(get_options).then(loggedIn => {
                console.log(`the result of checkAuth was ${loggedIn}`)
                if (loggedIn) {
                    sendLikeRequest(likeButton, post_options);
                }
                else {
                    const nextUrl = encodeURIComponent(document.location.href);
                    window.location.href = `/accounts/login/?next=${nextUrl}`;
                }
            })
            // ensure user is authenticated

        })
    }
    // manage click on archive button
})

function checkAuth(options) {
    return fetch('/check-auth/', options)
        .then(response => response.json())
        .then(data => data['logged_in'])
}


// function for sending like ot unlike request
function sendLikeRequest(likeButton, options) {
    const postId = likeButton.dataset.id
    const action = likeButton.dataset.action
    const url = likeButton.dataset.url

    // push the id and to a FormData object and then add it to options as body 
    var formData = new FormData()
    formData.append('id', postId)
    formData.append('action', action)

    options['body'] = formData

    fetch(url, options)
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'ok') {

                // define the text of the a tag be what 
                nowActionText = action === 'like' ? 'unlike' : 'like';

                // change the action dataset for future actions
                likeButton.dataset.action = nowActionText;

                // if user like the post, the image will be change to red heart and if unlike it the image will be change to empty heart image 
                likeButton.children[0].src = action == 'like' ? likeButton.dataset.limg : likeButton.dataset.unlimg;

                // change the total number of likes based on like and unlike
                counterElement = document.querySelector('div.post-footer .total');
                counterNumber = parseInt(counterElement.innerHTML);

                counterElement.innerHTML = action === 'like' ? counterNumber += 1 : counterNumber -= 1;
            }
            else {
                window.alert('مشکلی رخ داده، لطفا دقایقی دیگر امتحان کنید.')
            }
        });



}

function sendArchiveRequest(archiveButton, options) {
    const postId = archiveButton.dataset.id;
    const action = archiveButton.dataset.action;
    const url = archiveButton.dataset.url;

    const formData = new FormData();
    formData.append('id', postId);
    formData.append('action', action);

    options['body'] = formData;

    fetch(url, options)
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'ok') {
                // change the data-action's value for future actions
                archiveButton.dataset.action = action === 'archive' ? 'unarchive' : 'archive';

                archiveButton.children[0].src = action === 'archive' ? archiveButton.dataset.archimg : archiveButton.dataset.unarchimg;
                console.log(`Intended Post ${action === "archive" ? 'added to' : 'removed from'} archived posts.`)

            }
        })

}
// this function will get csrftoken from cookiesa
function getCsrfToken() {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }

    return null; // CSRF token not found
}