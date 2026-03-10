const API = "http://127.0.0.1:5000";

let dark = true;
let lastFile = null;


// ================= LOGIN =================
async function login() {

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch(API + "/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (data.status === "ok") {

        loginPage.classList.add("hidden");
        appPage.classList.remove("hidden");

        loadDashboard();
        loadLogs();
        loadStaff();

    } else {
        alert("Invalid credentials");
    }
}


// ================= LOGOUT =================
async function logout() {

    await fetch(API + "/api/logout");
    location.reload();
}


// ================= FORGOT PASSWORD =================
async function forgotPassword() {

    const username = prompt("Enter username");
    const newPass = prompt("Enter new password");

    if (!username || !newPass) return;

    const res = await fetch(API + "/api/change_password", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username,
            new_password: newPass
        })
    });

    const data = await res.json();

    if (data.status === "ok") {
        alert("Password updated");
    } else {
        alert("Invalid username");
    }
}


// ================= PAGE SWITCH =================
function showPage(page) {

    dashboardPage.classList.add("hidden");
    staffPage.classList.add("hidden");
    logsPage.classList.add("hidden");

    document.getElementById(page + "Page").classList.remove("hidden");
}



// ================= THEME =================
themeBtn.onclick = () => {

    dark = !dark;

    if (dark) {
        document.documentElement.setAttribute("data-theme", "dark");
        themeBtn.innerText = "☀️";
    } else {
        document.documentElement.setAttribute("data-theme", "light");
        themeBtn.innerText = "🌙";
    }
};



// ================= DASHBOARD =================
async function loadDashboard() {

    try {

        const res = await fetch(API + "/api/latest_intrusion");
        const data = await res.json();

        const img = document.getElementById("intruderImg");
        const noText = document.getElementById("noIntrusionText");
        const timeText = document.getElementById("intruderTime");

        if (data.status !== "ok") {

            img.src = "";
            timeText.innerText = "";
            noText.style.display = "block";
            return;
        }

        const filename = data.filename;
        timeText.innerText = "Detected at: " + data.timestamp;

        if (lastFile && lastFile !== filename) {

            const alarm = document.getElementById("alarmSound");
            const banner = document.getElementById("intrusionBanner");

            if (alarm) {
                alarm.currentTime = 0;
                alarm.play().catch(() => {});
            }

            if (banner) {

                banner.classList.remove("hidden");

                setTimeout(() => {
                    banner.classList.add("hidden");
                }, 5000);
            }
        }

        lastFile = filename;

        img.src =
            API + data.image_url +
            "?t=" + Date.now();

        noText.style.display = "none";

    } catch (err) {
        console.log("Dashboard error:", err);
    }
}



// ================= LOGS =================
async function loadLogs() {

    const res = await fetch(API + "/api/logs");
    const logs = await res.json();

    logsTable.innerHTML = "";

    logs.slice(0, 30).forEach(l => {

        logsTable.innerHTML += `
            <tr class="border-t border-gray-700">
                <td class="p-2">${l.timestamp}</td>
                <td class="p-2">${l.filename}</td>
            </tr>
        `;
    });

    intrusionCount.innerText = logs.length;
}



// ================= STAFF =================
async function loadStaff() {

    const res = await fetch(API + "/api/staff");
    const staff = await res.json();

    staffDropdown.innerHTML = "";

    staff.forEach(s => {
        staffDropdown.innerHTML += `<option>${s}</option>`;
    });

    staffCount.innerText = staff.length;
}



// ================= ADD STAFF =================
async function addStaff() {

    const name = staffName.value;
    const files = staffImages.files;

    const form = new FormData();
    form.append("name", name);

    for (let f of files) {
        form.append("images", f);
    }

    await fetch(API + "/api/add_staff", {
        method: "POST",
        body: form
    });

    alert("Staff Added");
    loadStaff();
}



// ================= DELETE STAFF =================
async function deleteStaff() {

    const name = staffDropdown.value;

    await fetch(API + "/api/delete_staff", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });

    alert("Deleted");
    loadStaff();
}



// ================= REGENERATE =================
async function regenerate() {

    await fetch(API + "/api/regenerate", {
        method: "POST"
    });

    alert("Embeddings Updated");
}



// ================= AUTO REFRESH =================
setInterval(() => {

    loadDashboard();
    loadLogs();

}, 3000);