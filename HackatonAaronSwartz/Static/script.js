document.getElementById('search-button').addEventListener('click', async () => {
    const searchQuery = document.getElementById('search-bar').value.trim();
    const resultsContainer = document.getElementById('results');
    const loader = document.getElementById('loader'); // Loader

    if (!searchQuery) {
        resultsContainer.innerHTML = `<p>Por favor, digite um nome para buscar.</p>`;
        return;
    }

    // Show the loader
    loader.style.display = 'block';
    resultsContainer.innerHTML = ''; // Clear previous results

    try {
        const response = await fetch(`/govbuster?nome=${encodeURIComponent(searchQuery)}`);
        const data = await response.json();

        if (response.ok) {
            if (data.processos.length === 0) {
                resultsContainer.innerHTML = `<p>Nenhum processo encontrado para: <strong>${searchQuery}</strong></p>`;
            } else {
                let resultHtml = `<p>Resultados para: <strong>${searchQuery}</strong></p>`;
                resultHtml += `<div class="perfil">;`
                resultHtml += `<img src="${data.foto_url || 'Foto não disponível'}" alt="Foto do candidato" />`;
                resultHtml += `</div>;`
                resultHtml += `<p>Total de processos em andamento: <strong>${data.processos.length}</strong></p>`;
                resultHtml += `<p>Partido: <strong>${data.partido || 'Partido não encontrado'}</strong></p>`;
                resultHtml += `<ul>`;

                data.processos.forEach((processo) => {
                    resultHtml += `
                        <li class="styled-item">
                            <strong>Processo:</strong> ${processo.numero_cnj}<br>
                            <strong>Fonte:</strong> ${processo.fonte}<br>
                            <strong>Data de Início:</strong> ${processo.data_inicio}<br>
                            <strong>Última Movimentação:</strong> ${processo.ultima_movimentacao || 'Nenhuma movimentação disponível'}<br>
                        </li>
                    `;
                });

                resultHtml += `</ul>`;
                resultsContainer.innerHTML = resultHtml;
            }
        } else {
            resultsContainer.innerHTML = `<p>Erro: ${data.erro || 'Erro desconhecido ao buscar processos.'}</p>`;
        }
    } catch (error) {
        console.error('Erro:', error);
        resultsContainer.innerHTML = `<p>Erro ao buscar processos. Por favor, tente novamente mais tarde.</p>`;
    } finally {
        // Hide the loader
        loader.style.display = 'none';
    }
});
