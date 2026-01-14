/* --- CONFIGURATION & STATE --- */
const appState = {
    notifications: [
        { id: 1, title: 'Server Maintenance', desc: 'Scheduled for 3:00 AM EST', icon: 'dns', type: 'info' },
        { id: 2, title: 'New Message', desc: 'Sarah commented on your project', icon: 'chat', type: 'action' },
        { id: 3, title: 'Support Ticket', desc: 'Ticket #492 has been resolved', icon: 'check_circle', type: 'success' }
    ],
    projects: [
        { title: 'Convo Dashboard', status: 'In Progress', desc: 'Refactoring UI/UX' },
        { title: 'API Integration', status: 'Pending', desc: 'Connect Python Backend' },
        { title: 'Mobile App', status: 'Review', desc: 'iOS styling updates' },
        { title: 'Database Migration', status: 'Done', desc: 'Moved to PostgreSQL' }
    ]
};

/* --- INITIALIZATION --- */
document.addEventListener('DOMContentLoaded', () => {
    initDateTime();
    renderDashboard();
    renderProjects();
});

/* --- LAYOUT LOGIC --- */
function toggleLayout() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const floatBtn = document.getElementById('floatingBtn');

    sidebar.classList.toggle('closed');
    content.classList.toggle('expanded');

    if (sidebar.classList.contains('closed')) {
        floatBtn.classList.add('visible');
    } else {
        floatBtn.classList.remove('visible');
    }
}

/* --- TAB SWITCHING LOGIC --- */
function switchTab(tabName, element) {
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('projects-view').classList.add('hidden');
    document.getElementById('settings-view').classList.add('hidden');

    document.getElementById(`${tabName}-view`).classList.remove('hidden');

    const navItems = document.querySelectorAll('.sidebar-item');
    navItems.forEach(item => item.classList.remove('active'));
    element.classList.add('active');
}

/* --- DYNAMIC RENDERING --- */
function renderDashboard() {
    const feed = document.getElementById('dashboard-feed');
    feed.innerHTML = ''; 

    const supportHTML = `
        <div class="card searchable-item" data-term="support help">
            <div class="card-left">
                <div class="icon-box">
                    <svg viewBox="0 0 24 24"><polygon points="12,2 2,22 22,22"/></svg>
                </div>
                <div class="card-info">
                    <h3>Support Center</h3>
                    <p>Get help with your account</p>
                </div>
            </div>
            <button class="card-action">Contact</button>
        </div>
    `;
    feed.innerHTML += supportHTML;

    if (appState.notifications.length === 0) {
        feed.innerHTML += `
            <div class="card">
                <div class="card-left">
                    <div class="icon-box"><span class="material-symbols-outlined">notifications_off</span></div>
                    <span>No new notifications</span>
                </div>
            </div>`;
    } else {
        appState.notifications.forEach(notif => {
            const html = `
                <div class="card searchable-item" id="notif-${notif.id}" data-term="${notif.title.toLowerCase()}">
                    <div class="card-left">
                        <div class="icon-box">
                            <span class="material-symbols-outlined">${notif.icon}</span>
                        </div>
                        <div class="card-info">
                            <h3>${notif.title}</h3>
                            <p>${notif.desc}</p>
                        </div>
                    </div>
                    <button class="card-action danger" onclick="dismissNotification(${notif.id})">Dismiss</button>
                </div>
            `;
            feed.innerHTML += html;
        });
    }
}

function renderProjects() {
    const grid = document.getElementById('projects-grid');
    grid.innerHTML = '';

    appState.projects.forEach(proj => {
        const html = `
            <div class="project-card searchable-item" data-term="${proj.title.toLowerCase()}">
                <div class="status-badge">${proj.status}</div>
                <h3 style="margin:0">${proj.title}</h3>
                <p style="color:#888; margin:0">${proj.desc}</p>
                <div style="margin-top:auto; padding-top:15px; display:flex; gap:10px;">
                     <button class="card-action" style="width:100%">Open</button>
                </div>
            </div>
        `;
        grid.innerHTML += html;
    });
}

/* --- FUNCTIONALITY --- */
function dismissNotification(id) {
    appState.notifications = appState.notifications.filter(n => n.id !== id);
    const el = document.getElementById(`notif-${id}`);
    if(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(-10px)';
        setTimeout(() => { renderDashboard(); }, 300);
    }
}

function handleSearch() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const items = document.querySelectorAll('.searchable-item');

    items.forEach(item => {
        const term = item.getAttribute('data-term');
        if (term.includes(filter)) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
    });
}

function initDateTime() {
    const dateEl = document.getElementById('date-display');
    const greetEl = document.getElementById('greeting');
    const now = new Date();
    const hours = now.getHours();

    dateEl.textContent = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

    let greeting = "Welcome Back,";
    if (hours < 12) greeting = "Good Morning,";
    else if (hours < 18) greeting = "Good Afternoon,";
    else greeting = "Good Evening,";
    
    greetEl.childNodes[0].nodeValue = greeting + " ";
}
