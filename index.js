// גלובלים
let currentUser = null;
let userTabs = [];
let selectedPhones = [];
let defaultReply = "אין תגובה מתאימה.";
let managers = [];
let groups = {};

async function login() {
    const username = document.getElementById('loginUser').value.trim();
    const password = document.getElementById('loginPass').value.trim();
    if (!username || !password) return;
    const res = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    if (res.status === 200) {
        const data = await res.json();
        currentUser = username;
        userTabs = data.tabs;
        localStorage.setItem('user', currentUser);
        localStorage.setItem('tabs', JSON.stringify(userTabs));
        showApp();
    } else {
        document.getElementById('loginError').style.display = 'block';
    }
}

function showApp() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('mainApp').style.display = 'block';
    const tabsArea = document.getElementById('tabsArea');
    tabsArea.innerHTML = '';
    userTabs.forEach(tab => {
        const btn = document.createElement('button');
        btn.innerText = getTabName(tab);
        btn.onclick = () => openTab(tab + 'Tab');
        tabsArea.appendChild(btn);
    });
    if (userTabs.length > 0) openTab(userTabs[0] + 'Tab');
}

function getTabName(tab) {
    const names = {
        responses: "תגובות",
        contacts: "אנשי קשר",
        groups: "קבוצות",
        calls: "טלפנייה",
        send: "שליחת הודעה",
        phoneSend: "שליחה מהטלפון",
        settings: "הגדרות",
        manage: "ניהול משתמשים"
    };
    return names[tab] || tab;
}

function openTab(tabId) {
    document.querySelectorAll('.tabContent').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelectorAll('.tabs button').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`.tabs button[onclick="openTab('${tabId}')"]`)?.classList.add('active');

    // טעינת מידע לכל לשונית
    if (tabId === 'responsesTab') loadResponses();
    if (tabId === 'contactsTab') loadContacts();
    if (tabId === 'groupsTab') updateGroups();
    if (tabId === 'phoneSendTab') updateManagers();
    if (tabId === 'manageTab') loadUsers();
}

// כל הפונקציות נוספות כמו loadResponses, loadContacts, updateGroups וכו'...
