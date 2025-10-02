const API_URL = 'http://localhost:5000/api';

/**
 * Récupère les articles via l'API et les affiche dans la div 'items'.
 */
async function loadItems() {
    try {
        const response = await fetch(`${API_URL}/items`);
        // Le Backend (Flask) gère la logique de cache (source: cache/database)
        const data = await response.json();
        
        const itemsDiv = document.getElementById('items');
        itemsDiv.innerHTML = `<p><em>Source: ${data.source}</em></p>`;

        if (data.items.length === 0) {
            itemsDiv.innerHTML += '<p>No items yet.</p>';
        } else {
            data.items.forEach(item => {
                itemsDiv.innerHTML += `
                    <div class="item">
                        <h3>${item.name}</h3>
                        <p>${item.description}</p>
                    </div>
                `;
            });
        }
    } catch (error) {
        document.getElementById('items').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}

/**
 * Envoie un nouvel article au Backend via POST.
 */
async function addItem() {
    const name = document.getElementById('itemName').value;
    const description = document.getElementById('itemDescription').value;

    if (!name) {
        alert('Name is required');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description })
        });

        if (response.ok) {
            // Efface les champs et recharge la liste pour voir le nouvel article
            document.getElementById('itemName').value = '';
            document.getElementById('itemDescription').value = '';
            loadItems();
        } else {
             // Afficher un message d'erreur si l'API répond mal
             const errorData = await response.json();
             alert(`Failed to add item. Status: ${response.status}. Detail: ${errorData.message || 'Unknown error'}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Charge les articles au chargement initial de la page.
window.onload = loadItems;