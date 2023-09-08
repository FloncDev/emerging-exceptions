console.log("ha")

const upload = document.getElementById("image");

upload.addEventListener("dragover", e => {
    e.preventDefault()
})

upload.addEventListener("drop", e => {
    upload.classList.remove("flash_red", "flash_green")

    upload.style.animation = 'none';
    upload.offsetHeight;
    upload.style.animation = null;

    console.log("Dropped file");

    e.preventDefault()

    if (e.dataTransfer.items) {
        [...e.dataTransfer.items].forEach((item, i) => {
            if (item.kind === "file") {
                const file = item.getAsFile()

                let file_extention = file.name.split(".").slice(-1)[0]

                if (!["png", "jpg", "jpeg"].includes(file_extention)) {
                    console.log("Not accepted", file_extention)
                    upload.classList.add("flash_red")
                    return
                } else {
                    upload.classList.add("flash_green")
                }

                console.log(file)
                // Send file to backend
            }
        })
    }
})
