let currentOperand = '';
let previousOperand = '';
let operation = undefined;
let useRemoteService = true;
let resultDisplayed = false;

// Fetch the remote server address from the configuration file
const remoteServerAddress = window.config.remoteServerAddress;
const webServerAddress = window.config.webServerAddress;

function appendNumber(number) {
    if (resultDisplayed) {
        currentOperand = '';  // Clear the current operand if result is displayed
        resultDisplayed = false;  // Reset the flag
    }
    if (number === '.' && currentOperand.includes('.')) return;
    currentOperand = currentOperand.toString() + number.toString();
    updateScreen();
    logToTextWindow(number.toString());
}

function chooseOperation(op) {
    if (currentOperand === '') return;
    if (previousOperand !== '') {
        computeResult();
    }
    operation = op;
    previousOperand = currentOperand;
    currentOperand = '';
    resultDisplayed = false;  // Ensure flag is reset when choosing a new operation
    logToTextWindow(op);
}

function computeResult() {
    if (useRemoteService) {
        computeResultRemote();
    } else {
        computeResultLocal();
    }
}

function computeResultLocal() {
    let result;
    const prev = parseFloat(previousOperand);
    const current = parseFloat(currentOperand);
    if (isNaN(prev) || isNaN(current)) return;
    switch (operation) {
        case '+':
            result = prev + current;
            break;
        case '-':
            result = prev - current;
            break;
        case '*':
            result = prev * current;
            break;
        case '/':
            result = prev / current;
            break;
        default:
            return;
    }
    currentOperand = result;
    operation = undefined;
    previousOperand = '';
    resultDisplayed = true;  // Set the flag when a result is displayed
    updateScreen();
    logToTextWindow('=' + result + '\n');
}

function computeResultRemote() {
    const prev = parseFloat(previousOperand);
    const current = parseFloat(currentOperand);
    if (isNaN(prev) || isNaN(current)) return;

    const operationsMap = {
        '+': 'add',
        '-': 'subtract',
        '*': 'multiply',
        '/': 'divide'
    };

    const payload = {
        operand1: prev,
        operand2: current,
        operation: operationsMap[operation]
    };

    fetch(`${remoteServerAddress}/calculate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            currentOperand = data.result;
            operation = undefined;
            previousOperand = '';
            resultDisplayed = true;  // Set the flag when a result is displayed
            updateScreen();
            logToTextWindow('=' + data.result + '\n');
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function clearScreen() {
    currentOperand = '';
    previousOperand = '';
    operation = undefined;
    resultDisplayed = false;  // Ensure flag is reset when clearing the screen
    updateScreen();
}

function updateScreen() {
    document.getElementById('calculator-screen').value = currentOperand;
}

function logToTextWindow(content) {
    const textWindow = document.getElementById('history');
    textWindow.value += content;
}

function clearTextWindow(content) {
    const textWindow = document.getElementById('history');
    textWindow.value = "";
}

function toggleTextWindow() {
    const textWindow = document.getElementById('text-window');
    const toggleButton = document.getElementById('toggle-button');
    if (textWindow.style.right === '0px') {
        textWindow.style.right = '-320px';
        toggleButton.textContent = '>>';
    } else {
        textWindow.style.right = '0px';
        toggleButton.textContent = '<<';
    }
}

function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    loginWith(username, password, "login");
}

function loginWith(username, password, form) {
    const payload = {
        username: username,
        password: password
    };
    console.log(payload)

    document.getElementById(form + '-form').style.display = 'none';
    document.getElementById('spinner').style.display = 'block';

    fetch(`${remoteServerAddress}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => {
            document.getElementById('spinner').style.display = 'none';
            document.getElementById('login-form').removeAttribute('style');
            if (!response.ok) {
                if (response.status === 400) {
                    console.log("failed login: 401")
                    document.getElementById('errormsg').style.display = "block";
                }
            } else {
                window.location.replace(`${webServerAddress}/index.html`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function logout() {
    fetch(`${remoteServerAddress}/logout`, {
        method: 'POST'
    })
        .then(response => {
            if (response.ok) {
                window.location.replace(`${webServerAddress}/login.html`);
            } else {
                console.error("Could not logout!");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function goToRegister() {
    window.location.replace(`${webServerAddress}/register.html`);
}

function register() {
    var username = document.getElementById('username').value;
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var error = document.getElementById('errormsg')

    if (password1 === password2) {
        const payload = {
            username: username,
            password: password1
        };
        fetch(`${remoteServerAddress}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (response.ok) {
                    loginWith(username, password1, "register");
                    window.location.replace(`${webServerAddress}/index.html`);
                } else {
                    if (response.status === 409) {
                        error.style.display = "block";
                        error.textContent = "User already exists!"
                    }
                    console.error("Could not logout!");
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        error.style.display = "block";
        error.textContent = "Passwords does not match!"
    }
}


function getUserName() {
    fetch(`${remoteServerAddress}/users/current`, {
        method: 'GET'
    })
        .then(response => {
            if (response.status === 204) {
                window.location.replace(`${webServerAddress}/login.html`);
            } else {
                response.json().then(body => {
                    console.log(body.username)
                    document.getElementById('user-name').textContent = body.username;
                })
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function toggleRemoteService() {
    useRemoteService = !useRemoteService;
    const remoteToggleButton = document.getElementById('remote-toggle');
    if (useRemoteService) {
        remoteToggleButton.classList.add('enabled');
    } else {
        remoteToggleButton.classList.remove('enabled');
    }
}
