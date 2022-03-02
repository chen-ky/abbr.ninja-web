const API_BASE_URL = "https://api.abbr.ninja/api/v1"
const getRootPage = () => {
    let url = new URL(document.URL);
    return url.protocol + "//" + url.host;
};
const FRONTEND_URL = getRootPage();
const DEFAULT_SCHEME = "https://"

function isEmpty(id) {
    const input_box = document.getElementById(id);
    if (input_box.value === "") {
        input_box.className = "required";
        return true
    }
    input_box.className = "";
    return false
}

function setResultText(msg, is_error=false, as_html=false) {
    const result_box = document.getElementById("result");
    if (is_error) {
        result_box.className = "error-text";
    } else {
        result_box.className = "";
    }
    if (!as_html) {
        result_box.innerText = msg;
    } else {
        result_box.innerHTML = msg;
    }
}

function shorten() {
    if (isEmpty("uri-input")) {
        setResultText(null);
        return;
    }

    try {
        const long_uri = parseInputURI();
        shortenReq(long_uri);
    } catch (e) {
        document.getElementById("uri-input").className = "required"; // Make input box red
        setResultText("Invalid URI, please check your input", true);
        return;
    }
}

function parseInputURI() {
    const uri = document.getElementById("uri-input")
    try {
        return new URL(uri.value);
    } catch (TypeError) {
        if (uri.value != "") {
            uri.value = DEFAULT_SCHEME + uri.value;
        }
        return new URL(uri.value);
    }
}

function shortenReq(long_uri) {
    setResultText("Shortening... Please wait...");
    let http_code;
    postReq(`${API_BASE_URL}/shorten`, {"uri": long_uri.href})
        .then(response => {
            http_code = response.status;
            if (response.status === 200 || response.status === 400) {
                return response.json();
            } else {
                setResultText(`${response.status}: ${response.statusText}`, true);
                return null;
            }
        })
        .catch( error => {
            console.error(error);
            setResultText("Network error, please try again later.", true);
            return null;
        })
        .then(val => {
            if (val === null) {
                return;
            }
            if (http_code === 200) {
                const path = `/r/${val["id"]}`;
                const retrieve_link = `${FRONTEND_URL}${path}`;
                setResultText(`<a id="result-link" href=${path} target="_blank" rel="noopener nofollow">${retrieve_link}</a>`, false, true);
            } else if (http_code === 400) {
                setResultText(`Bad request: ${val["msg"]}`, true);
            } else {
                setResultText(`Something has gone wrong. Please try again later.`, true);
                console.error(`$ERROR: ${http_code}`);
            }
        });
}

async function postReq(url = "", data = {}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return response;
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
