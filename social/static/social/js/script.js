document.addEventListener("DOMContentLoaded", function () {
    initConfirmLinks();
    initImageModal();
    initImagePreview();
    initProfileCropper();
    initFormSubmission();
    initButtonHandlers();
});

function initConfirmLinks() {
    const confirmLinks = document.querySelectorAll(".confirm-action");

    confirmLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            const message = link.getAttribute("data-message") || "Are you sure?";
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });
}

function initImageModal() {
    const modal = document.getElementById("imageModal");
    const modalImage = document.getElementById("modalImage");
    const closeModal = document.querySelector(".close-modal");
    const images = document.querySelectorAll(".open-image");

    images.forEach(function (image) {
        image.addEventListener("click", function () {
            if (modal) {
                modal.style.display = "block";
            }
            if (modalImage) {
                modalImage.src = image.src;
            }
        });
    });

    if (closeModal && modal) {
        closeModal.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    if (modal) {
        modal.addEventListener("click", function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    }
}

function initImagePreview() {
    const postImageInput = document.querySelector("input[name='post_image']");
    const postImagePreview = document.getElementById("postImagePreview");

    if (!postImageInput || !postImagePreview) {
        return;
    }

    postImageInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            postImagePreview.src = e.target.result;
            postImagePreview.style.display = "block";
        };
        reader.readAsDataURL(file);
    });
}

let cropper;

function initProfileCropper() {
    const profileInput = document.getElementById("profilePhotoInput");
    const cropPreview = document.getElementById("cropPreview");

    if (!profileInput) {
        return;
    }

    profileInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            if (!cropPreview) {
                return;
            }

            cropPreview.src = e.target.result;
            cropPreview.style.display = "block";

            if (cropper) {
                cropper.destroy();
            }

            cropper = new Cropper(cropPreview, {
                aspectRatio: 1,
                viewMode: 1,
                autoCropArea: 1
            });
        };
        reader.readAsDataURL(file);
    });
}

function initFormSubmission() {
    const forms = document.querySelectorAll("form");
    const croppedImageInput = document.getElementById("croppedImage");

    if (!forms.length) {
        return;
    }

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            if (!cropper || !croppedImageInput) {
                return;
            }

            const canvas = cropper.getCroppedCanvas({
                width: 400,
                height: 400
            });
            croppedImageInput.value = canvas.toDataURL("image/png");
        });
    });
}

function initButtonHandlers() {
    initSaveButtons();
    initShareButtons();
    initTogglePasswordButtons();
    initCommentToggleButtons();
    initLikeButtons();
}

function initSaveButtons() {
    const saveButtons = document.querySelectorAll(".save-btn");

    saveButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const icon = button.querySelector("i");
            if (!icon) {
                return;
            }
            icon.classList.toggle("bi-bookmark");
            icon.classList.toggle("bi-bookmark-fill");
        });
    });
}


function initShareButtons() {
    const shareButtons = document.querySelectorAll(".share-btn");

    shareButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            alert("Post link copied/share feature demo.");
        });
    });
}


function initTogglePasswordButtons() {
    const togglePasswordButtons = document.querySelectorAll(".toggle-password");

    togglePasswordButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const input = button.parentElement.querySelector("input");
            const icon = button.querySelector("i");

            if (!input || !icon) {
                return;
            }

            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");
            } else {
                input.type = "password";
                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");
            }
        });
    });
}


function initCommentToggleButtons() {
    const commentToggleButtons = document.querySelectorAll(".comment-toggle");

    commentToggleButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const targetId = button.getAttribute("data-target");
            const target = document.getElementById(targetId);

            if (target) {
                target.classList.toggle("d-none");
            }
        });
    });
}


function initLikeButtons() {
    const likeButtons = document.querySelectorAll(".ajax-like-btn");

    likeButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const url = button.getAttribute("data-url");
            const tokenMeta = document.querySelector("meta[name='csrf-token']");
            const csrfToken = tokenMeta ? tokenMeta.getAttribute("content") : null;

            if (!url || !csrfToken) {
                return;
            }

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                const icon = button.querySelector("i");
                const count = button.querySelector(".like-count");

                if (count) {
                    count.textContent = data.likes_count;
                }

                if (!icon) {
                    return;
                }

                if (data.liked) {
                    button.classList.add("liked");
                    icon.classList.remove("bi-heart");
                    icon.classList.add("bi-heart-fill");
                } else {
                    button.classList.remove("liked");
                    icon.classList.remove("bi-heart-fill");
                    icon.classList.add("bi-heart");
                }
            });
        });
    });
}
