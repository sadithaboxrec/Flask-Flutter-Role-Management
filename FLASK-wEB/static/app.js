async function createUser() {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;
  const msgDiv = document.getElementById("message");

  const res = await fetch("/create-user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password, role })
  });

  const data = await res.json();
  msgDiv.style.display = "block";

  if (res.ok) {
    msgDiv.className = "success";
    msgDiv.innerHTML = `✔ Account created! UID: <strong>${data.uid}</strong>`;
    clearForm();
    loadUsers();
  } else {
    msgDiv.className = "error";
    msgDiv.innerHTML = `✖ Error: ${data.error}`;
  }
}

function clearForm() {
  document.getElementById("name").value = "";
  document.getElementById("email").value = "";
  document.getElementById("password").value = "";
  document.getElementById("role").value = "";
}

async function loadUsers() {
  const res = await fetch("/list-users");
  const users = await res.json();
  const tbody = document.getElementById("userBody");
  tbody.innerHTML = "";

  users.forEach(u => {
    tbody.innerHTML += `
      <tr>
        <td>${u.name}</td>
        <td>${u.email}</td>
        <td>${u.role}</td>
      </tr>
    `;
  });
}

window.onload = loadUsers;