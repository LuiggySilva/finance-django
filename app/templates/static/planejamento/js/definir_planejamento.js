window.onload = () => {
    var salvar_planejamento_btns = document.querySelectorAll('.bnt-salvar-planejamento');
    salvar_planejamento_btns.forEach(btn => {
        btn.addEventListener('click', () => {
            const categoria_id = btn.getAttribute('data-categoria-id'); 
            const fetch_url = btn.getAttribute('data-url') 
            var valor_planejamento = document.getElementById(`categoria-id-${categoria_id}`).value;
            fetch(fetch_url, {
                method:'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({valor: valor_planejamento})
            }).then((result) => {
                return result.json();
            }).then((data) => {
                console.log(data);
            });
        });
    });
}