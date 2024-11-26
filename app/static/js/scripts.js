document.getElementById('consult-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const patente = document.getElementById('patente').value;
    fetch(`/consultapatente/${patente}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result').innerText = data.error;
            } else {
                window.location.href = `/patenteinfo?patente=${data.patente}&timestamp=${data.timestamp}&ubicacion=${data.ubicacion}`;
            }
        })
        .catch(error => {
            document.getElementById('result').innerText = 'Error fetch data';
        });
});