let encode = true;
let module = "fourier"

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

                upload.innerHTML = ``

                let reader = new FileReader()
                reader.onload = (e) => {
                    upload.style.backgroundImage = ""
                    upload.style.backgroundImage = `url(${e.target.result})`
                }

                reader.readAsDataURL(file)
                let meta = upload.parentElement.children[1]

                let left_table = meta.children[0].children[0]
                let right_table = meta.children[1].children[0]

                // File size
                left_table.children[0].children[0].innerHTML = "Size"
                left_table.children[0].children[1].innerHTML = Math.round(file.size / 1000).toString() + " KB"

                // File ext
                right_table.children[0].children[0].innerHTML = "Format"
                right_table.children[0].children[1].innerHTML = file_extention.toUpperCase()

                // Type
                left_table.children[1].children[0].innerHTML = "Type"
                left_table.children[1].children[1].innerHTML = file.type

                // Supported
                right_table.children[1].children[0].innerHTML = "Supported"
                right_table.children[1].children[1].innerHTML = "True"

                // Last Modified
                left_table.children[2].children[0].innerHTML = "Modified"
                left_table.children[2].children[1].innerHTML = file.lastModified
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
    module = "fourier"
    get_inputs()
})

steg_btn.addEventListener("click", e => {
    // Only needs input
    module = "steg"
    get_inputs()
})

datastamp_btn.addEventListener("click", e => {
    // Only needs input
    module = "datastamp"
    get_inputs()
})

let controls = document.getElementsByClassName("controls")[0]

function get_inputs() {
    fetch(window.location.origin + `/components?module=${module}&encode=${encode}`)
    .then(resp => resp.text())
    .then(text => {
        controls.innerHTML = text
    })
}

function read_inputs() {
    let data = {}

    for (let i=0; i<controls.children.length; i++) {
        let e = controls.children.item(i)

        switch (e.className.split(" ")[0]) {
            case "text_small":
                input = e.children[1]

                data[input.id] = input.value
                break

            case "text_large":
                input = e.children[1]

                data[input.id] = input.value
                break

            case "select":
                form = e.children[1]

                for (let i=0;i<form.length;i++) {
                    element = form.elements[i]
                    if (element.checked) {
                        data[form.id] = element.id
                        break
                    }
                }

                data[form.id] = form.children[0].id

                break

            case "dropdown":
                select = e.children[1]
                selected = select.value

                for (let i=0;i<select.length;i++) {
                    element = select.children[i]

                    if (element.value == selected) {
                        data[select.id] = element.id
                        break
                    }
                }

                break
        }
    }

    return data
}

const submit_btn = document.getElementById("submit")

submit_btn.addEventListener("click", e => {
    let data = new FormData()
    data.append("image", file)
    data.append("data", JSON.stringify({
        "module": module,
        "is_encode": encode,
        "inputs": JSON.stringify(read_inputs())
        // Get data from inputs
    }))

    fetch("/process", {
        method: "POST",
        body: data
    })
    .then(resp => {
        console.log(resp.headers.get("Content-Type"))
        if (resp.headers.get("Content-Type") == "image/png") {
            resp.blob().then(blob => {
                url = URL.createObjectURL(blob)
                output_panel.children[0].children[0].src = url
                output_panel.children[0].children[0].hidden= false
            })
        } else {
            resp.text().then(text => {
                output_panel.children[0].innerHTML = text
            })
        }
    })
})

const encode_btn = document.getElementById("encode_btn")
const decode_btn = document.getElementById("decode_btn")

encode_btn.addEventListener("click", e => {
    encode = true
    get_inputs()
})

decode_btn.addEventListener("click", e => {
    encode = false
    get_inputs()
})

get_inputs()
