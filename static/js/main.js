const champSelect = document.getElementById('champ-select');
const addChampBtn = document.getElementById('add-champ-btn');
const enemyDraftBox = document.getElementById('enemy-draft');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsArea = document.getElementById('results-area');
const resultsLoader = document.getElementById('results-loader');

const explanationsList = document.getElementById('explanations-list');
const champResults = document.getElementById('champ-results');
const itemResults = document.getElementById('item-results');

let currentDraft = [];

function updateUI() {
    enemyDraftBox.innerHTML = '';
    currentDraft.forEach((champ, index) => {
        const dItem = document.createElement('div');
        dItem.className = 'draft-item';
        dItem.innerHTML = `
            <span>${champ.name}</span>
            <button class="remove-btn" onclick="removeChamp(${index})">×</button>
        `;
        enemyDraftBox.appendChild(dItem);
    });

    if (currentDraft.length > 0) {
        analyzeBtn.disabled = false;
        analyzeBtn.classList.remove('disabled');
    } else {
        analyzeBtn.disabled = true;
        analyzeBtn.classList.add('disabled');
        resultsArea.classList.add('hidden');
    }

    if (currentDraft.length >= 5) {
        addChampBtn.disabled = true;
    } else {
        addChampBtn.disabled = false;
    }
}

addChampBtn.addEventListener('click', () => {
    if (champSelect.value && currentDraft.length < 5) {
        const id = champSelect.value;
        const nameText = champSelect.options[champSelect.selectedIndex].text.split(' - ')[0];

        if (!currentDraft.find(c => c.id === id)) {
            currentDraft.push({ id, name: nameText });
            updateUI();
        } else {
            alert('El campeón ya está en el draft.');
        }
    }
});

// Need to make removeChamp global for inline onclick
window.removeChamp = function (index) {
    currentDraft.splice(index, 1);
    updateUI();
}

analyzeBtn.addEventListener('click', async () => {
    if (currentDraft.length === 0) return;

    resultsArea.classList.add('hidden');
    resultsLoader.classList.remove('hidden');

    const enemy_draft = currentDraft.map(c => c.id);

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ enemy_draft })
        });

        const data = await response.json();
        if (data.success) {
            renderResults(data.data);
        } else {
            alert("Error: " + data.error);
        }
    } catch (e) {
        console.error(e);
        alert("Fallo de comunicación con la API del Sis. Experto.");
    } finally {
        resultsLoader.classList.add('hidden');
    }
});

function renderResults(data) {
    explanationsList.innerHTML = '';
    champResults.innerHTML = '';
    itemResults.innerHTML = '';

    if (!data.explanations || data.explanations.length === 0) {
        explanationsList.innerHTML = '<li>No se han detectado combinaciones críticas. Se recomienda una build estándar balanceada.</li>';
    } else {
        data.explanations.forEach(exp => {
            const li = document.createElement('li');
            li.textContent = exp;
            explanationsList.appendChild(li);
        });
    }

    if (data.recommended_champions.length === 0) {
        champResults.innerHTML = '<span class="result-desc">No hay recomendaciones disponibles o todos están pickeados.</span>';
    } else {
        data.recommended_champions.forEach(champ => {
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `
                <div class="result-item-header">
                    <span class="result-name">${champ.name} (${champ.role})</span>
                    <span class="result-score">WR Ponderado: ${champ.score}%</span>
                </div>
                <span class="result-desc">${champ.reason}</span>
            `;
            champResults.appendChild(div);
        });
    }

    if (data.recommended_items.length === 0) {
        itemResults.innerHTML = '<span class="result-desc">No hay objetos críticos específicos recomendados para esta comp.</span>';
    } else {
        data.recommended_items.forEach(item => {
            const tags = item.matching_tags ? item.matching_tags.join(', ') : '';
            const desc = item.description || '';
            const div = document.createElement('div');
            div.className = 'result-item';
            div.innerHTML = `
                <div class="result-item-header">
                    <span class="result-name">${item.name}</span>
                    <span class="result-score">Relevancia: ${item.score}</span>
                </div>
                <span class="result-desc" style="margin-bottom:0.5rem">${desc}</span>
                <span class="result-desc">Específico para: ${tags}</span>
            `;
            itemResults.appendChild(div);
        });
    }

    // Smooth scroll down to results
    setTimeout(() => {
        resultsArea.scrollIntoView({ behavior: 'smooth' });
    }, 100);

    resultsArea.classList.remove('hidden');
}
