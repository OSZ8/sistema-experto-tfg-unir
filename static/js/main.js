// Constante Académica estática para garantizar la presentación offline en DDragon
const DD_VERSION = '16.7.1';
const DD_URL = `https://ddragon.leagueoflegends.com/cdn/${DD_VERSION}/img/champion/`;

let CHAMPIONS_DATA = [];
let allyDraft = [null, null, null, null, null];
let enemyDraft = [null, null, null, null, null];
let activeSlot = null; // Guardará a qué equipo y slot corresponde el popup Modal

// DOM Pointers
const allyContainer = document.getElementById('ally-slots');
const enemyContainer = document.getElementById('enemy-slots');
const analyzeBtn = document.getElementById('analyze-btn');
const draftWarning = document.getElementById('draft-warning');

// Debug Console Elements
const toggleDebugBtn = document.getElementById('toggle-debug-btn');
const debugConsole = document.getElementById('debug-console');
const debugOutputText = document.getElementById('debug-output-text');

if (toggleDebugBtn) {
    toggleDebugBtn.addEventListener('click', () => {
        debugConsole.classList.toggle('hidden');
    });
}

// Modal Elements
const modal = document.getElementById('roster-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const champSearch = document.getElementById('champ-search');
const rosterGrid = document.getElementById('champion-roster');
const modalTitle = document.getElementById('modal-title');

// Startup UI Builder
function initSlots() {
    renderSlots(allyDraft, allyContainer, 'ally');
    renderSlots(enemyDraft, enemyContainer, 'enemy');
    checkAnalyzeState();
}

function renderSlots(draftArray, container, teamType) {
    container.innerHTML = '';
    draftArray.forEach((champ, idx) => {
        const slot = document.createElement('div');
        slot.className = `draft-slot ${champ ? 'filled' : 'empty'}`;

        const posLabels = ['Top', 'Jungla', 'Medio', 'ADC', 'Apoyo'];
        const posLabel = teamType === 'ally' ? posLabels[idx] : `Rival ${idx + 1}`;

        if (champ) {
            slot.innerHTML = `
                <div class="pos-badge-ally">${posLabel}</div>
                <img src="${DD_URL}${champ.id}.png" alt="${champ.name}" title="${champ.name}" class="slot-img fade-in" onerror="this.onerror=null; this.src='https://ui-avatars.com/api/?name=${champ.name}&background=1a1e29&color=c8aa6e&size=100&bold=true';">
                <div class="slot-name">${champ.name}</div>
                <button class="remove-slot" onclick="removeChamp('${teamType}', ${idx}, event)">×</button>
            `;
        } else {
            slot.innerHTML = `
                <div class="pos-badge-empty">${posLabel}</div>
                <div class="empty-plus">+</div>
            `;
        }

        slot.onclick = () => openModal(teamType, idx);
        container.appendChild(slot);
    });
}

// Funciones Globales de Limpieza
window.removeChamp = function (team, idx, event) {
    event.stopPropagation(); // Previene cierre indeseado.
    if (team === 'ally') allyDraft[idx] = null;
    else enemyDraft[idx] = null;
    initSlots();
}

function openModal(team, idx) {
    const posLabels = ['Top', 'Jungla', 'Medio', 'ADC', 'Apoyo'];
    activeSlot = { team, index: idx };
    modalTitle.innerText = team === 'ally' ? `Selecciona: Tu Composición (Para ${posLabels[idx]})` : `Selecciona: Enemigo (Posición ${idx + 1})`;
    champSearch.value = '';
    renderRoster('');
    modal.classList.remove('hidden');
    champSearch.focus();
}

function closeModal() {
    modal.classList.add('hidden');
    activeSlot = null;
}

closeModalBtn.onclick = closeModal;
modal.querySelector('.modal-bg').onclick = closeModal;

// Input en tiempo real de cuadrícula
champSearch.addEventListener('input', (e) => {
    renderRoster(e.target.value.toLowerCase());
});

function renderRoster(filterText) {
    rosterGrid.innerHTML = '';

    // Filtra campeones ya seleccionados localmente.
    const allPickedIds = [...allyDraft.filter(c => c).map(c => c.id), ...enemyDraft.filter(c => c).map(c => c.id)];

    CHAMPIONS_DATA.forEach(champ => {
        if (champ.name.toLowerCase().includes(filterText)) {
            const isPicked = allPickedIds.includes(champ.id);
            const div = document.createElement('div');
            div.className = `roster-item ${isPicked ? 'disabled' : ''}`;

            // Define fallback genérico estilizado para campeones nuevos que no existan en el CDN
            div.innerHTML = `
                <img src="${DD_URL}${champ.id}.png" alt="${champ.name}" loading="lazy" onerror="this.onerror=null; this.src='https://ui-avatars.com/api/?name=${champ.name}&background=1a1e29&color=c8aa6e&size=100&bold=true';">
                <span>${champ.name}</span>
            `;

            if (!isPicked) {
                div.onclick = () => selectChampion(champ);
            }
            rosterGrid.appendChild(div);
        }
    });
}

function selectChampion(champ) {
    if (!activeSlot) return;
    if (activeSlot.team === 'ally') {
        allyDraft[activeSlot.index] = champ;
    } else {
        enemyDraft[activeSlot.index] = champ;
    }
    closeModal();
    initSlots();
}

function checkAnalyzeState() {
    const enemies = enemyDraft.filter(c => c).length;
    if (enemies > 0) {
        analyzeBtn.disabled = false;
        analyzeBtn.classList.remove('disabled');
        draftWarning.classList.add('hidden');
    } else {
        analyzeBtn.disabled = true;
        analyzeBtn.classList.add('disabled');
        draftWarning.classList.remove('hidden');
    }
}

// -----------------------------------------
// REST API Communication a Backend App.py
// -----------------------------------------
analyzeBtn.addEventListener('click', async () => {
    const enemy_draft = enemyDraft.filter(c => c).map(c => c.id);
    const ally_draft = {};
    const posLabels = ['Top', 'Jungla', 'Medio', 'ADC', 'Apoyo'];
    allyDraft.forEach((c, idx) => {
        ally_draft[posLabels[idx]] = c ? c.id : null;
    });

    if (enemy_draft.length === 0) return;

    document.getElementById('results-area').classList.add('hidden');
    document.getElementById('results-loader').classList.remove('hidden');

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ enemy_draft, ally_draft })
        });

        const data = await response.json();

        // Valida escudo defensivo código 400 backend.
        if (data.success) {
            renderResults(data.data);
        } else {
            alert("Respuesta API denegada: " + data.error);
        }
    } catch (e) {
        console.error(e);
        alert("Fallo de infraestructura con Backend.");
    } finally {
        document.getElementById('results-loader').classList.add('hidden');
    }
});

function renderResults(data) {
    const expList = document.getElementById('explanations-list');
    const champRes = document.getElementById('champ-results');
    const itemRes = document.getElementById('item-results');
    const resultsArea = document.getElementById('results-area');

    expList.innerHTML = '';
    champRes.innerHTML = '';
    itemRes.innerHTML = '';

    // Procesa explicaciones teóricas (XAI).
    if (!data.explanations || data.explanations.length === 0) {
        expList.innerHTML = '<li>No se han detonado reglas críticas en tu contra. Sinergia estándar.</li>';
    } else {
        data.explanations.forEach(exp => {
            const li = document.createElement('li');
            li.textContent = exp;
            expList.appendChild(li);
        });
    }

    // Renderiza resultados por posición.
    if (!data.recommended_champions_grouped || Object.keys(data.recommended_champions_grouped).length === 0) {
        champRes.innerHTML = '<span class="result-desc">No se encontraron campeones óptimos bajo estos criterios.</span>';
    } else {
        const iconsMap = { 'Top': '', 'Jungla': '', 'Medio': '', 'ADC': '', 'Apoyo': '' };

        for (const [posName, candidates] of Object.entries(data.recommended_champions_grouped)) {
            const block = document.createElement('div');
            block.className = 'role-recommendation-block';
            block.innerHTML = `<h4 class="role-block-title">Top 3 Mejores: ${posName.toUpperCase()}</h4>`;
            
            candidates.forEach(champ => {
                const div = document.createElement('div');
                div.className = 'result-row result-champ fade-in';
                div.innerHTML = `
                    <img src="${DD_URL}${champ.id}.png" class="result-icon champ-icon" alt="${champ.name}" onerror="this.onerror=null; this.src='https://ui-avatars.com/api/?name=${champ.name}&background=1a1e29&color=c8aa6e&size=100&bold=true';">
                    <div class="result-details">
                        <span class="result-name">${champ.name} <span class="badge-role">${champ.role}</span></span>
                        <span class="result-reason">${champ.reason}</span>
                    </div>
                    <div class="result-score-badge">${champ.score}%</div>
                `;
                block.appendChild(div);
            });
            champRes.appendChild(block);
        }
    }

    // Renderiza objetos recomendados.
    if (data.recommended_items.length === 0) {
        itemRes.innerHTML = '<span class="result-desc">No requiere cambios dramáticos de inventario.</span>';
    } else {
        data.recommended_items.forEach(item => {
            const tags = item.matching_tags ? item.matching_tags.join(', ') : '';
            const div = document.createElement('div');
            div.className = 'result-row result-item-row fade-in';

            div.innerHTML = `
                <div class="result-details">
                    <span class="result-name item-name">${item.name}</span>
                    <span class="result-reason">${item.description}</span>
                    <span class="item-tags-meta">Contramedida activada por Tag/s: <b style="color:#fff">${tags}</b></span>
                </div>
                <div class="item-score">Relevancia: ${item.score}</div>
            `;
            itemRes.appendChild(div);
        });
    }

    // Exporta logs RAW por pantalla en debug terminal.
    if (data.debug_info) {
        debugOutputText.textContent = JSON.stringify(data.debug_info, null, 2);
    }

    resultsArea.classList.remove('hidden');
    setTimeout(() => {
        resultsArea.scrollIntoView({ behavior: 'smooth' });
    }, 150);
}

// Start application
async function startApp() {
    try {
        const response = await fetch('/api/champions');
        CHAMPIONS_DATA = await response.json();
        initSlots();
    } catch (e) {
        console.error("Error al arrancar el DataDragon local:", e);
    }
}

startApp();
