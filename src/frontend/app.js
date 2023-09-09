const upload = document.getElementById("image");
const center_upload = document.getElementById("upload");

upload.addEventListener("dragover", e => {
    e.preventDefault()
})

let file = null;

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
                file = item.getAsFile()

                let file_extention = file.name.split(".").slice(-1)[0]

                if (!["png", "jpg", "jpeg"].includes(file_extention)) {
                    console.log("Not accepted", file_extention)
                    upload.classList.add("flash_red")
                    file = null
                    return
                } else {
                    upload.classList.add("flash_green")
                }

                console.log(file, file.type)
                // Send file to backend

                upload.innerHTML = ``

                let reader = new FileReader()
                reader.onload = (e) => {
                    upload.style.backgroundImage = `url(${e.target.result})`
                }

                reader.readAsDataURL(file)

            }
        })
    }
})

let fourier_btn = document.getElementById("fourier_btn")
let steg_btn = document.getElementById("steg_btn")
let datastamp_btn = document.getElementById("datastamp_btn")

let nav_items = document.getElementsByClassName("nav_item")

let output_panel = document.getElementsByClassName("out_panel")[0]

for (let i = 0; i < nav_items.length; i++) {
    let el = nav_items[i]

    el.addEventListener("click", e => {
        document.getElementsByClassName("selected")[0].classList.remove("selected")

        el.classList.add("selected")
    })
}

fourier_btn.addEventListener("click", e => {
    // Needs both input and output panel
    output_panel.hidden = false
    get_inputs("fourier")
})

steg_btn.addEventListener("click", e => {
    // Only needs input
    output_panel.hidden = true
    get_inputs("steg")
})

datastamp_btn.addEventListener("click", e => {
    // Only needs input
    output_panel.hidden = true
    get_inputs("datastamp")
})

let controls = document.getElementsByClassName("controls")[0]

function get_inputs(module) {
    fetch(window.location.origin + "/components?module="+module)
    .then(resp => resp.text())
    .then(text => {
        controls.innerHTML = text
        console.log(text)
    })
}

get_inputs("fourier")
