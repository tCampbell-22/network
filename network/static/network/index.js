
function updateLikes(element) {
    elemId = element.id;
    id = elemId.substring(4);
    like = (element.innerHTML == "Like"); 
    likeCountElem = document.querySelector(`#numLikes${id}`);

    form = new FormData();
    form.append("id", id);

    fetch("/like/", {
        method: "POST",
        body: form,
    })
    .then(response => response.json())
    .then(response => {
        element.innerHTML = like ? "Unlike" : "Like";
        likeCountElem.innerHTML = response['likes'];
        element.className = `btn border border-${!like ? 'success' : 'danger'}`;
        console.log(response);
    })

}

function updateFollow(element) {
    curUsername = document.querySelector("#user-title").innerHTML;
    wasFollowing = (element.innerHTML != "Follow"); 
    followCountElem = document.querySelector('#follower-count');

    form = new FormData();
    form.append("profileName", curUsername);

    fetch("/follow/", {
        method: "POST",
        body: form,
    })
    .then(response => response.json())
    .then(response => {
        element.innerHTML = wasFollowing ? "Follow" : "Unfollow";
        followCountElem.innerHTML = response['numFollowers'];
        element.className = `btn ${!wasFollowing ? 'border border-secondary' : 'btn-primary'} mx-3`;
        console.log(response);
    })
}

function editPost(element) {
    id = element.id.substring(4);
    btnText = element.innerHTML
    editArea = document.querySelector(`#edit-area${id}`);
    console.log(`edit-area${id}`);
    if (btnText == "Edit") {
        editArea.style.display = "inline-block";
        element.innerHTML = "Save";
        document.querySelector(`#body${id}`).style.display = "none"
    } else {
        newText = editArea.value;
        console.log(newText);
        element.innerHTML = "Edit"; 
        form = new FormData();
        console.log(form);
        form.append("id", id);
        form.append("newText", newText);

        fetch("/edit/", {
            method: "POST",
            body: form,
        })
        .then(res => res.json())
        .then(res => {
            editArea.innerHTML = res['post'];
            editArea.style.display = "none";
            document.querySelector(`#body${id}`).style.display = "inline-block";
            document.querySelector(`#body${id}`).innerHTML = res['post']
        })
    }

    

}