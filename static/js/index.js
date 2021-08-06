const API_BASE_URL = "https://api.abbr.ninja/api/v1"
const FRONTEND_URL = "abbr.ninja"

function isEmpty(id) {
    const input_box = document.getElementById(id);
    if (input_box.value === "") {
        input_box.className = "required";
        return true
    }
    input_box.className = "";
    return false
}

function shorten() {
    if (isEmpty("uri-input")) {
        document.getElementById("result").innerHTML = null;
        document.getElementById("result").innerText = null;
        return
    }
    document.getElementById("result").style.color = "inherit";
    document.getElementById("result").innerText = "Shortening... Please wait...";
    
    const txt = document.getElementById("uri-input").value;
    const req = new XMLHttpRequest();
    const payload = {'uri': txt}
    // console.log(payload);
    req.open("POST", `${API_BASE_URL}/shorten`);
    req.setRequestHeader("Content-Type", "application/json");
    req.send(JSON.stringify(payload));
    req.onload = function() {
        const result = document.getElementById("result");
        if (req.status === 400) {
            const msg = JSON.parse(req.response)["msg"];
            result.style.color = "red";
            result.innerText = msg;
        } else if (req.status === 200) {
            const response = JSON.parse(req.response);
            const path = `/r/${response["id"]}`;
            const retrieve_link = `${FRONTEND_URL}${path}`;
            result.innerHTML = `<a id="result-link" href=${path} target="_blank" rel="noopener"></a>`
            document.getElementById("result-link").innerText = retrieve_link;
        } else {
            result.style.color = "red";
            result.innerText = `${req.status}: ${req.statusText}`;
        }
    };
    req.onerror = function() {
        const result = document.getElementById("result");
        result.style.color = "red";
        result.innerText = `Network error.`;
    };
}

function listenShortReq() {
    const long_uri = document.getElementById('uri-input');
    const shorten_btn = document.getElementById("submit-btn");
    long_uri.addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            shorten_btn.click();
        }
    });

    shorten_btn.addEventListener('click', function() {shorten()});
}

listenShortReq()