/**
 * Expert Mode Civilization Renderers
 * Handles rendering of complex civilization sub-structures
 */

import { getCurrentData, markDirty } from '../state.js';
import { createNumberField, createStringArrayField, createTextField } from '../form/fields.js';

export function renderStartBiasTerrains(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentTerrains = data.civilization?.start_bias_terrains || [];
        currentTerrains.forEach((terrain, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.start_bias_terrains.${idx}.terrain_type`, 'Terrain Type', terrain.terrain_type || ''));
            itemDiv.appendChild(createNumberField(`civilization.start_bias_terrains.${idx}.score`, 'Score', terrain.score || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.start_bias_terrains.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add Terrain Bias';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.start_bias_terrains) {
            data.civilization.start_bias_terrains = [];
        }
        data.civilization.start_bias_terrains.push({ terrain_type: '', score: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderCivilizationUnlocks(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentUnlocks = data.civilization?.civilization_unlocks || [];
        currentUnlocks.forEach((unlock, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.age_type`, 'Age Type', unlock.age_type || ''));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.type`, 'Type', unlock.type || ''));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.kind`, 'Kind', unlock.kind || ''));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.name`, 'Name', unlock.name || ''));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.description`, 'Description', unlock.description || ''));
            itemDiv.appendChild(createTextField(`civilization.civilization_unlocks.${idx}.icon`, 'Icon', unlock.icon || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.civilization_unlocks.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add Civilization Unlock';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.civilization_unlocks) {
            data.civilization.civilization_unlocks = [];
        }
        data.civilization.civilization_unlocks.push({ age_type: '', type: '', kind: '', name: '', description: '', icon: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderLeaderCivilizationBiases(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentBiases = data.civilization?.leader_civilization_biases || [];
        currentBiases.forEach((bias, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.leader_civilization_biases.${idx}.leader_type`, 'Leader Type', bias.leader_type || ''));
            itemDiv.appendChild(createNumberField(`civilization.leader_civilization_biases.${idx}.bias`, 'Bias', bias.bias || ''));
            itemDiv.appendChild(createTextField(`civilization.leader_civilization_biases.${idx}.reason_type`, 'Reason Type', bias.reason_type || ''));
            itemDiv.appendChild(createTextField(`civilization.leader_civilization_biases.${idx}.choice_type`, 'Choice Type', bias.choice_type || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.leader_civilization_biases.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add Leader Bias';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.leader_civilization_biases) {
            data.civilization.leader_civilization_biases = [];
        }
        data.civilization.leader_civilization_biases.push({ leader_type: '', bias: '', reason_type: '', choice_type: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderLocalizations(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentLocs = data.civilization?.localizations || [];
        currentLocs.forEach((loc, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.entity_id`, 'Entity ID (optional)', loc.entity_id || ''));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.name`, 'Name', loc.name || ''));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.description`, 'Description', loc.description || ''));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.full_name`, 'Full Name', loc.full_name || ''));
            itemDiv.appendChild(createTextField(`civilization.localizations.${idx}.adjective`, 'Adjective', loc.adjective || ''));

            if (loc.city_names) {
                itemDiv.appendChild(createStringArrayField(`civilization.localizations.${idx}.city_names`, 'City Names', loc.city_names || [], 'civilization'));
            }

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.localizations.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add Localization';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.localizations) {
            data.civilization.localizations = [];
        }
        data.civilization.localizations.push({ name: '', description: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderLoadingInfoCivilizations(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentInfos = data.civilization?.loading_info_civilizations || [];
        currentInfos.forEach((info, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.civilization_text`, 'Civilization Text', info.civilization_text || ''));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.subtitle`, 'Subtitle', info.subtitle || ''));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.tip`, 'Tip', info.tip || ''));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.background_image_high`, 'Background Image (High)', info.background_image_high || ''));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.background_image_low`, 'Background Image (Low)', info.background_image_low || ''));
            itemDiv.appendChild(createTextField(`civilization.loading_info_civilizations.${idx}.foreground_image`, 'Foreground Image', info.foreground_image || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.loading_info_civilizations.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add Loading Info';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.loading_info_civilizations) {
            data.civilization.loading_info_civilizations = [];
        }
        data.civilization.loading_info_civilizations.push({ civilization_text: '', subtitle: '', tip: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderLeaderCivPriorities(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentPriorities = data.civilization?.leader_civ_priorities || [];
        currentPriorities.forEach((priority, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.leader_civ_priorities.${idx}.leader_type`, 'Leader Type', priority.leader_type || ''));
            itemDiv.appendChild(createNumberField(`civilization.leader_civ_priorities.${idx}.priority`, 'Priority', priority.priority || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.leader_civ_priorities.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add Priority';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.leader_civ_priorities) {
            data.civilization.leader_civ_priorities = [];
        }
        data.civilization.leader_civ_priorities.push({ leader_type: '', priority: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderAIListTypes(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentListTypes = data.civilization?.ai_list_types || [];
        currentListTypes.forEach((listType, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.ai_list_types.${idx}.list_type`, 'List Type', listType.list_type || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.ai_list_types.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add AI List Type';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.ai_list_types) {
            data.civilization.ai_list_types = [];
        }
        data.civilization.ai_list_types.push({ list_type: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderAILists(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentAILists = data.civilization?.ai_lists || [];
        currentAILists.forEach((aiList, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.ai_lists.${idx}.list_type`, 'List Type', aiList.list_type || ''));
            itemDiv.appendChild(createTextField(`civilization.ai_lists.${idx}.leader_type`, 'Leader Type', aiList.leader_type || ''));
            itemDiv.appendChild(createTextField(`civilization.ai_lists.${idx}.system`, 'System', aiList.system || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.ai_lists.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add AI List';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.ai_lists) {
            data.civilization.ai_lists = [];
        }
        data.civilization.ai_lists.push({ list_type: '', leader_type: '', system: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}

export function renderAIFavoredItems(container) {
    container.innerHTML = '';

    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'space-y-3';

    const rerenderItems = () => {
        itemsDiv.innerHTML = '';
        const data = getCurrentData();
        const currentItems = data.civilization?.ai_favored_items || [];
        currentItems.forEach((item, idx) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'p-3 bg-slate-900/50 rounded border border-slate-600 space-y-2';

            itemDiv.appendChild(createTextField(`civilization.ai_favored_items.${idx}.list_type`, 'List Type', item.list_type || ''));
            itemDiv.appendChild(createTextField(`civilization.ai_favored_items.${idx}.item`, 'Item', item.item || ''));
            itemDiv.appendChild(createNumberField(`civilization.ai_favored_items.${idx}.value`, 'Value', item.value || ''));

            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'px-3 py-1 bg-red-600/20 hover:bg-red-600/40 border border-red-600 rounded text-red-400 text-xs';
            removeBtn.type = 'button';
            removeBtn.onclick = () => {
                const data = getCurrentData();
                data.civilization.ai_favored_items.splice(idx, 1);
                markDirty();
                rerenderItems();
            };
            itemDiv.appendChild(removeBtn);

            itemsDiv.appendChild(itemDiv);
        });
    };

    rerenderItems();

    const addBtn = document.createElement('button');
    addBtn.textContent = '+ Add Favored Item';
    addBtn.className = 'px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm';
    addBtn.type = 'button';
    addBtn.onclick = () => {
        const data = getCurrentData();
        if (!data.civilization.ai_favored_items) {
            data.civilization.ai_favored_items = [];
        }
        data.civilization.ai_favored_items.push({ list_type: '', item: '', value: '' });
        markDirty();
        rerenderItems();
    };

    container.appendChild(itemsDiv);
    container.appendChild(addBtn);
}
