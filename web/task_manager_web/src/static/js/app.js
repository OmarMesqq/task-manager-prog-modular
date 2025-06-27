/**
 * Task Manager - Frontend JavaScript Application
 * 
 * Este arquivo contém toda a lógica frontend para interagir com a API
 * do sistema de gerenciamento de tarefas.
 */

// Configuração da API
const API_BASE_URL = '/api';

// Estado global da aplicação
let appState = {
    currentSection: 'dashboard',
    tasks: [],
    users: [],
    teams: [],
    tags: [],
    stats: {},
    selectedTags: []
};

// Variável global para o gráfico de status
let statusChart = null;

// Variável para debounce da atualização de status
let statusUpdateTimeout = null;

// Utilitários
const utils = {
    // Formata data para exibição
    formatDate: (dateString) => {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // Formata status para exibição
    formatStatus: (status) => {
        const statusMap = {
            'aberta': 'Aberta',
            'em_progresso': 'Em Progresso',
            'concluida': 'Concluída'
        };
        return statusMap[status] || status;
    },
    
    // Obtém classe CSS para status
    getStatusClass: (status) => {
        const classMap = {
            'aberta': 'status-aberta',
            'em_progresso': 'status-em-progresso',
            'concluida': 'status-concluida'
        };
        return classMap[status] || 'status-aberta';
    },
    
    // Trunca texto
    truncateText: (text, maxLength = 100) => {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
};

// API Client
const api = {
    // Requisição base
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Erro na requisição');
            }
            
            return data;
        } catch (error) {
            console.error(`Erro na API (${endpoint}):`, error);
            throw error;
        }
    },
    
    // Tasks
    tasks: {
        list: () => api.request('/tasks'),
        create: (task) => api.request('/tasks', {
            method: 'POST',
            body: JSON.stringify(task)
        }),
        get: (id) => api.request(`/tasks/${id}`),
        update: (id, task) => api.request(`/tasks/${id}`, {
            method: 'PUT',
            body: JSON.stringify(task)
        }),
        delete: (id) => api.request(`/tasks/${id}`, {
            method: 'DELETE'
        }),
        stats: () => api.request('/tasks/stats')
    },
    
    // Users
    users: {
        list: () => api.request('/users'),
        create: (user) => api.request('/users', {
            method: 'POST',
            body: JSON.stringify(user)
        }),
        get: (id) => api.request(`/users/${id}`),
        update: (id, user) => api.request(`/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(user)
        })
    },
    
    // Teams
    teams: {
        list: () => api.request('/teams'),
        create: (team) => api.request('/teams', {
            method: 'POST',
            body: JSON.stringify(team)
        }),
        get: (id) => api.request(`/teams/${id}`),
        update: (id, team) => api.request(`/teams/${id}`, {
            method: 'PUT',
            body: JSON.stringify(team)
        }),
        addMember: (teamId, userId) => api.request(`/teams/${teamId}/members/${userId}`, {
            method: 'POST'
        }),
        removeMember: (teamId, userId) => api.request(`/teams/${teamId}/members/${userId}`, {
            method: 'DELETE'
        })
    },
    
    // Tags
    tags: {
        list: () => api.request('/tags'),
        create: (tag) => api.request('/tags', {
            method: 'POST',
            body: JSON.stringify(tag)
        }),
        get: (id) => api.request(`/tags/${id}`),
        update: (id, tag) => api.request(`/tags/${id}`, {
            method: 'PUT',
            body: JSON.stringify(tag)
        })
    }
};

// UI Components
const ui = {
    // Mostra loading
    showLoading: () => {
        document.getElementById('loading').classList.remove('hidden');
    },
    
    // Esconde loading
    hideLoading: () => {
        document.getElementById('loading').classList.add('hidden');
    },
    
    // Mostra toast notification
    showToast: (message, type = 'info') => {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        
        const bgColor = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            warning: 'bg-yellow-500',
            info: 'bg-blue-500'
        }[type] || 'bg-blue-500';
        
        toast.className = `${bgColor} text-white px-6 py-3 rounded-lg shadow-lg fade-in`;
        toast.innerHTML = `
            <div class="flex items-center">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            </div>
        `;
        
        container.appendChild(toast);
        lucide.createIcons();
        
        // Remove automaticamente após 5 segundos
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
};

// Navigation
function showSection(sectionName) {
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('text-primary-600', 'bg-primary-50');
        link.classList.add('text-gray-500');
    });
    
    // Add active class to current nav link (only if event exists)
    if (event && event.target) {
        event.target.classList.remove('text-gray-500');
        event.target.classList.add('text-primary-600', 'bg-primary-50');
    } else {
        // Find the correct nav link and activate it
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            if (link.textContent.toLowerCase().includes(sectionName.toLowerCase()) || 
                link.getAttribute('onclick')?.includes(sectionName)) {
                link.classList.remove('text-gray-500');
                link.classList.add('text-primary-600', 'bg-primary-50');
            }
        });
    }
    
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    
    // Show selected section
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.classList.remove('hidden');
    }
    
    // Update app state
    appState.currentSection = sectionName;
    
    // Load section data
    loadSectionData(sectionName);
}

function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

// Data Loading
async function loadSectionData(sectionName) {
    ui.showLoading();
    
    try {
        switch (sectionName) {
            case 'dashboard':
                await loadDashboardData();
                break;
            case 'tasks':
                await loadTasksData();
                break;
            case 'users':
                await loadUsersData();
                break;
            case 'teams':
                await loadTeamsData();
                break;
            case 'tags':
                await loadTagsData();
                break;
        }
    } catch (error) {
        ui.showToast(`Erro ao carregar dados: ${error.message}`, 'error');
    } finally {
        ui.hideLoading();
    }
}

async function loadDashboardData() {
    try {
        // Carrega todas as entidades necessárias
        const [tasksResponse, usersResponse, teamsResponse, tagsResponse, statsResponse] = await Promise.all([
            api.tasks.list(),
            api.users.list(),
            api.teams.list(),
            api.tags.list(),
            api.tasks.stats()
        ]);
        
        // Atualiza o estado apenas se os dados mudaram
        const newTasks = tasksResponse.data || [];
        const newUsers = usersResponse.data || [];
        const newTeams = teamsResponse.data || [];
        const newTags = tagsResponse.data || [];
        const newStats = statsResponse.data || {};
        
        // Verifica se os dados mudaram antes de atualizar
        const tasksChanged = JSON.stringify(newTasks) !== JSON.stringify(appState.tasks);
        const usersChanged = JSON.stringify(newUsers) !== JSON.stringify(appState.users);
        const teamsChanged = JSON.stringify(newTeams) !== JSON.stringify(appState.teams);
        const tagsChanged = JSON.stringify(newTags) !== JSON.stringify(appState.tags);
        
        // Verifica se é o carregamento inicial (estado vazio)
        const isInitialLoad = appState.tasks.length === 0 && appState.users.length === 0;
        
        appState.tasks = newTasks;
        appState.users = newUsers;
        appState.teams = newTeams;
        appState.tags = newTags;
        appState.stats = newStats;
        
        // Atualiza cards de estatísticas
        document.getElementById('total-tasks').textContent = appState.tasks.length;
        document.getElementById('total-users').textContent = appState.users.length;
        document.getElementById('total-teams').textContent = appState.teams.length;
        document.getElementById('total-tags').textContent = appState.tags.length;
        
        // Renderiza gráfico se as tarefas mudaram OU se é carregamento inicial
        if (tasksChanged || isInitialLoad) {
            renderStatusChart();
        }
        
        // Renderiza tarefas recentes se as tarefas mudaram OU se é carregamento inicial
        if (tasksChanged || isInitialLoad) {
            renderRecentTasks();
        }
        
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
        throw error;
    }
}

async function loadTasksData() {
    try {
        // Carrega todas as entidades necessárias
        const [tasksResponse, usersResponse, teamsResponse, tagsResponse] = await Promise.all([
            api.tasks.list(),
            api.users.list(),
            api.teams.list(),
            api.tags.list()
        ]);
        
        appState.tasks = tasksResponse.data || [];
        appState.users = usersResponse.data || [];
        appState.teams = teamsResponse.data || [];
        appState.tags = tagsResponse.data || [];
        
        // Popula filtros
        populateTaskFilters();
        
        // Renderiza tarefas
        renderTasks();
        
    } catch (error) {
        console.error('Erro ao carregar tarefas:', error);
        throw error;
    }
}

async function loadUsersData() {
    try {
        const response = await api.users.list();
        appState.users = response.data || [];
        renderUsers();
    } catch (error) {
        console.error('Erro ao carregar usuários:', error);
        throw error;
    }
}

async function loadTeamsData() {
    try {
        const response = await api.teams.list();
        appState.teams = response.data || [];
        renderTeams();
    } catch (error) {
        console.error('Erro ao carregar times:', error);
        throw error;
    }
}

async function loadTagsData() {
    try {
        const response = await api.tags.list();
        appState.tags = response.data || [];
        renderTags();
    } catch (error) {
        console.error('Erro ao carregar tags:', error);
        throw error;
    }
}

// Rendering Functions
function renderStatusChart() {
    const ctx = document.getElementById('statusChart');
    
    // Destrói o gráfico anterior se existir
    if (statusChart) {
        statusChart.destroy();
    }
    
    const statusCounts = {
        'aberta': 0,
        'em_progresso': 0,
        'concluida': 0
    };
    
    appState.tasks.forEach(task => {
        if (task.status && statusCounts.hasOwnProperty(task.status)) {
            statusCounts[task.status]++;
        }
    });
    
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Abertas', 'Em Progresso', 'Concluídas'],
            datasets: [{
                data: [
                    statusCounts['aberta'],
                    statusCounts['em_progresso'],
                    statusCounts['concluida']
                ],
                backgroundColor: [
                    '#3b82f6',
                    '#f59e0b',
                    '#10b981'
                ],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#ffffff',
                    borderWidth: 1
                }
            },
            cutout: '60%',
            animation: {
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

function renderRecentTasks() {
    const container = document.getElementById('recent-tasks');
    const recentTasks = appState.tasks
        .sort((a, b) => new Date(b.prazo) - new Date(a.prazo))
        .slice(0, 5);
    
    if (recentTasks.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">Nenhuma tarefa encontrada</p>';
        return;
    }
    
    container.innerHTML = recentTasks.map(task => `
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex-1">
                <h4 class="font-medium text-gray-900">${task.titulo}</h4>
                <p class="text-sm text-gray-600">${utils.truncateText(task.descricao, 50)}</p>
            </div>
            <span class="px-2 py-1 text-xs font-medium rounded-full ${utils.getStatusClass(task.status)}">
                ${utils.formatStatus(task.status)}
            </span>
        </div>
    `).join('');
}

function renderTasks() {
    const container = document.getElementById('tasks-grid');
    
    if (appState.tasks.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i data-lucide="clipboard-list" class="w-16 h-16 text-gray-300 mx-auto mb-4"></i>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Nenhuma tarefa encontrada</h3>
                <p class="text-gray-600">Crie sua primeira tarefa para começar.</p>
            </div>
        `;
        lucide.createIcons();
        return;
    }
    
    container.innerHTML = appState.tasks.map(task => {
        const user = appState.users.find(u => u.id === task.usuario_responsavel_id);
        const taskTags = appState.tags.filter(tag => task.tags_ids && task.tags_ids.includes(tag.id));
        
        return `
            <div class="bg-white p-6 rounded-lg shadow card-hover">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-lg font-semibold text-gray-900">${task.titulo}</h3>
                    <span class="px-2 py-1 text-xs font-medium rounded-full ${utils.getStatusClass(task.status)}">
                        ${utils.formatStatus(task.status)}
                    </span>
                </div>
                
                <p class="text-gray-600 mb-4">${utils.truncateText(task.descricao)}</p>
                
                <div class="flex items-center text-sm text-gray-500 mb-3">
                    <i data-lucide="user" class="w-4 h-4 mr-1"></i>
                    <span>${user ? user.nome : 'Usuário não encontrado'}</span>
                </div>
                
                <div class="flex items-center text-sm text-gray-500 mb-4">
                    <i data-lucide="calendar" class="w-4 h-4 mr-1"></i>
                    <span>${utils.formatDate(task.prazo)}</span>
                </div>
                
                ${taskTags.length > 0 ? `
                    <div class="flex flex-wrap gap-1 mb-4">
                        ${taskTags.map(tag => `
                            <span class="px-2 py-1 text-xs rounded-full text-white" style="background-color: ${tag.cor}">
                                ${tag.nome}
                            </span>
                        `).join('')}
                    </div>
                ` : ''}
                
                <div class="flex justify-end space-x-2">
                    <button onclick="updateTaskStatus(${task.id})" class="text-blue-600 hover:text-blue-800 text-sm">
                        Alterar Status
                    </button>
                    <button onclick="deleteTask(${task.id})" class="text-red-600 hover:text-red-800 text-sm">
                        Excluir
                    </button>
                </div>
            </div>
        `;
    }).join('');
    
    lucide.createIcons();
}

function renderUsers() {
    const tbody = document.getElementById('users-table-body');
    
    if (appState.users.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="3" class="px-6 py-12 text-center text-gray-500">
                    Nenhum usuário encontrado
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = appState.users.map(user => `
        <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                        <div class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                            <i data-lucide="user" class="w-5 h-5 text-gray-600"></i>
                        </div>
                    </div>
                    <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">${user.nome}</div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${user.email}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button onclick="editUser(${user.id})" class="text-indigo-600 hover:text-indigo-900 mr-3">
                    Editar
                </button>
                <button onclick="viewUserTasks(${user.id})" class="text-green-600 hover:text-green-900">
                    Ver Tarefas
                </button>
            </td>
        </tr>
    `).join('');
    
    lucide.createIcons();
}

function renderTeams() {
    const container = document.getElementById('teams-grid');
    
    if (appState.teams.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i data-lucide="users-2" class="w-16 h-16 text-gray-300 mx-auto mb-4"></i>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Nenhum time encontrado</h3>
                <p class="text-gray-600">Crie seu primeiro time para começar.</p>
            </div>
        `;
        lucide.createIcons();
        return;
    }
    
    container.innerHTML = appState.teams.map(team => `
        <div class="bg-white p-6 rounded-lg shadow card-hover">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-gray-900">${team.nome}</h3>
                <div class="flex items-center text-sm text-gray-500">
                    <i data-lucide="users" class="w-4 h-4 mr-1"></i>
                    <span>${team.qtd_membros} membros</span>
                </div>
            </div>
            
            <div class="flex justify-end space-x-2">
                <button onclick="manageTeamMembers(${team.id})" class="text-blue-600 hover:text-blue-800 text-sm">
                    Gerenciar Membros
                </button>
                <button onclick="viewTeamTasks(${team.id})" class="text-green-600 hover:text-green-800 text-sm">
                    Ver Tarefas
                </button>
            </div>
        </div>
    `).join('');
    
    lucide.createIcons();
}

function renderTags() {
    const container = document.getElementById('tags-grid');
    
    if (appState.tags.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i data-lucide="tag" class="w-16 h-16 text-gray-300 mx-auto mb-4"></i>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Nenhuma tag encontrada</h3>
                <p class="text-gray-600">Crie sua primeira tag para começar.</p>
            </div>
        `;
        lucide.createIcons();
        return;
    }
    
    container.innerHTML = appState.tags.map(tag => `
        <div class="bg-white p-4 rounded-lg shadow card-hover">
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <div class="w-4 h-4 rounded-full mr-3" style="background-color: ${tag.cor}"></div>
                    <span class="font-medium text-gray-900">${tag.nome}</span>
                </div>
                <button onclick="editTag(${tag.id})" class="text-gray-400 hover:text-gray-600">
                    <i data-lucide="edit-2" class="w-4 h-4"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    lucide.createIcons();
}

// Modal Functions
function openTaskModal() {
    // Popula selects
    populateTaskModal();
    document.getElementById('task-modal').classList.remove('hidden');
}

function closeTaskModal() {
    document.getElementById('task-modal').classList.add('hidden');
    document.getElementById('task-form').reset();
    appState.selectedTags = [];
}

function openUserModal() {
    document.getElementById('user-modal').classList.remove('hidden');
}

function closeUserModal() {
    document.getElementById('user-modal').classList.add('hidden');
    document.getElementById('user-form').reset();
}

function openTeamModal() {
    document.getElementById('team-modal').classList.remove('hidden');
}

function closeTeamModal() {
    document.getElementById('team-modal').classList.add('hidden');
    document.getElementById('team-form').reset();
}

function openTagModal() {
    document.getElementById('tag-modal').classList.remove('hidden');
}

function closeTagModal() {
    document.getElementById('tag-modal').classList.add('hidden');
    document.getElementById('tag-form').reset();
}

// Form Handlers
async function handleTaskForm(event) {
    event.preventDefault();
    ui.showLoading();
    
    try {
        const formData = new FormData(event.target);
        const taskData = {
            titulo: document.getElementById('task-title').value,
            descricao: document.getElementById('task-description').value,
            usuario_id: parseInt(document.getElementById('task-user').value),
            time_id: parseInt(document.getElementById('task-team').value),
            prazo: document.getElementById('task-deadline').value,
            tags_ids: appState.selectedTags
        };
        
        await api.tasks.create(taskData);
        ui.showToast('Tarefa criada com sucesso!', 'success');
        closeTaskModal();
        
        if (appState.currentSection === 'tasks') {
            await loadTasksData();
        }
        
    } catch (error) {
        ui.showToast(`Erro ao criar tarefa: ${error.message}`, 'error');
    } finally {
        ui.hideLoading();
    }
}

async function handleUserForm(event) {
    event.preventDefault();
    ui.showLoading();
    
    try {
        const userData = {
            nome: document.getElementById('user-name').value,
            email: document.getElementById('user-email').value
        };
        
        await api.users.create(userData);
        ui.showToast('Usuário criado com sucesso!', 'success');
        closeUserModal();
        
        if (appState.currentSection === 'users') {
            await loadUsersData();
        }
        
    } catch (error) {
        ui.showToast(`Erro ao criar usuário: ${error.message}`, 'error');
    } finally {
        ui.hideLoading();
    }
}

async function handleTeamForm(event) {
    event.preventDefault();
    ui.showLoading();
    
    try {
        const teamData = {
            nome: document.getElementById('team-name').value
        };
        
        await api.teams.create(teamData);
        ui.showToast('Time criado com sucesso!', 'success');
        closeTeamModal();
        
        if (appState.currentSection === 'teams') {
            await loadTeamsData();
        }
        
    } catch (error) {
        ui.showToast(`Erro ao criar time: ${error.message}`, 'error');
    } finally {
        ui.hideLoading();
    }
}

async function handleTagForm(event) {
    event.preventDefault();
    ui.showLoading();
    
    try {
        const tagData = {
            nome: document.getElementById('tag-name').value,
            cor: document.getElementById('tag-color').value
        };
        
        await api.tags.create(tagData);
        ui.showToast('Tag criada com sucesso!', 'success');
        closeTagModal();
        
        if (appState.currentSection === 'tags') {
            await loadTagsData();
        }
        
    } catch (error) {
        ui.showToast(`Erro ao criar tag: ${error.message}`, 'error');
    } finally {
        ui.hideLoading();
    }
}

// Helper Functions
function populateTaskModal() {
    // Popula usuários
    const userSelect = document.getElementById('task-user');
    userSelect.innerHTML = '<option value="">Selecione um usuário</option>';
    appState.users.forEach(user => {
        userSelect.innerHTML += `<option value="${user.id}">${user.nome}</option>`;
    });
    
    // Popula times
    const teamSelect = document.getElementById('task-team');
    teamSelect.innerHTML = '<option value="">Selecione um time</option>';
    appState.teams.forEach(team => {
        teamSelect.innerHTML += `<option value="${team.id}">${team.nome}</option>`;
    });
    
    // Popula tags
    const tagsContainer = document.getElementById('task-tags');
    tagsContainer.innerHTML = appState.tags.map(tag => `
        <label class="flex items-center cursor-pointer">
            <input type="checkbox" value="${tag.id}" onchange="toggleTagSelection(${tag.id})" class="sr-only">
            <span class="px-3 py-1 text-sm rounded-full text-white tag-checkbox" style="background-color: ${tag.cor}; opacity: 0.5">
                ${tag.nome}
            </span>
        </label>
    `).join('');
}

function populateTaskFilters() {
    // Popula filtro de usuários
    const userFilter = document.getElementById('user-filter');
    userFilter.innerHTML = '<option value="">Todos os Usuários</option>';
    appState.users.forEach(user => {
        userFilter.innerHTML += `<option value="${user.id}">${user.nome}</option>`;
    });
    
    // Popula filtro de times
    const teamFilter = document.getElementById('team-filter');
    teamFilter.innerHTML = '<option value="">Todos os Times</option>';
    appState.teams.forEach(team => {
        teamFilter.innerHTML += `<option value="${team.id}">${team.nome}</option>`;
    });
}

function toggleTagSelection(tagId) {
    const index = appState.selectedTags.indexOf(tagId);
    const checkbox = event.target;
    const span = checkbox.nextElementSibling;
    
    if (index === -1) {
        appState.selectedTags.push(tagId);
        span.style.opacity = '1';
        checkbox.checked = true;
    } else {
        appState.selectedTags.splice(index, 1);
        span.style.opacity = '0.5';
        checkbox.checked = false;
    }
}

// Action Functions
async function updateTaskStatus(taskId) {
    // Cancela a atualização anterior se existir
    if (statusUpdateTimeout) {
        clearTimeout(statusUpdateTimeout);
    }
    
    // Aplica debounce de 300ms
    statusUpdateTimeout = setTimeout(async () => {
        const task = appState.tasks.find(t => t.id === taskId);
        if (!task) return;
        
        const statusOptions = [
            { value: 'aberta', label: 'Aberta' },
            { value: 'em_progresso', label: 'Em Progresso' },
            { value: 'concluida', label: 'Concluída' }
        ];
        
        const currentIndex = statusOptions.findIndex(s => s.value === task.status);
        const nextIndex = (currentIndex + 1) % statusOptions.length;
        const newStatus = statusOptions[nextIndex].value;
        
        try {
            ui.showLoading();
            
            // Envia apenas o status atualizado
            const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: newStatus })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erro ao atualizar status');
            }
            
            ui.showToast('Status atualizado com sucesso!', 'success');
            
            // Recarrega os dados da seção atual
            if (appState.currentSection === 'dashboard') {
                await loadDashboardData();
            } else if (appState.currentSection === 'tasks') {
                await loadTasksData();
            }
        } catch (error) {
            ui.showToast(`Erro ao atualizar status: ${error.message}`, 'error');
        } finally {
            ui.hideLoading();
        }
    }, 300);
}

async function deleteTask(taskId) {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return;
    
    try {
        ui.showLoading();
        await api.tasks.delete(taskId);
        ui.showToast('Tarefa excluída com sucesso!', 'success');
        await loadTasksData();
    } catch (error) {
        ui.showToast(`Erro ao excluir tarefa: ${error.message}`, 'error');
    } finally {
        ui.hideLoading();
    }
}

function applyTaskFilters() {
    // Implementar filtros de tarefas
    ui.showToast('Filtros aplicados!', 'info');
}

function clearTaskFilters() {
    document.getElementById('status-filter').value = '';
    document.getElementById('user-filter').value = '';
    document.getElementById('team-filter').value = '';
    renderTasks();
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa ícones Lucide
    lucide.createIcons();
    
    // Configura event listeners dos formulários
    document.getElementById('task-form').addEventListener('submit', handleTaskForm);
    document.getElementById('user-form').addEventListener('submit', handleUserForm);
    document.getElementById('team-form').addEventListener('submit', handleTeamForm);
    document.getElementById('tag-form').addEventListener('submit', handleTagForm);
    
    // Sincroniza color picker com input de texto
    const colorPicker = document.getElementById('tag-color');
    const colorText = document.getElementById('tag-color-text');
    
    colorPicker.addEventListener('change', function() {
        colorText.value = this.value;
    });
    
    colorText.addEventListener('change', function() {
        if (/^#[0-9A-F]{6}$/i.test(this.value)) {
            colorPicker.value = this.value;
        }
    });
    
    // Carrega dados iniciais com pequeno delay para garantir DOM carregado
    setTimeout(() => {
        showSection('dashboard');
    }, 100);
});

// Funções globais para serem chamadas do HTML
window.showSection = showSection;
window.toggleMobileMenu = toggleMobileMenu;
window.openTaskModal = openTaskModal;
window.closeTaskModal = closeTaskModal;
window.openUserModal = openUserModal;
window.closeUserModal = closeUserModal;
window.openTeamModal = openTeamModal;
window.closeTeamModal = closeTeamModal;
window.openTagModal = openTagModal;
window.closeTagModal = closeTagModal;
window.toggleTagSelection = toggleTagSelection;
window.updateTaskStatus = updateTaskStatus;
window.deleteTask = deleteTask;
window.applyTaskFilters = applyTaskFilters;
window.clearTaskFilters = clearTaskFilters;

