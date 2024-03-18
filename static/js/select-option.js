// Função para atualizar o gráfico com base no ano selecionado
function updateGraph(year) {
    $.ajax({
        url: `/graph/${year}`,
        type: 'GET',
        success: function (data) {
            $('#chart').html(data);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
}

// Manipulador de evento para a mudança na seleção do ano
$(document).ready(function () {
    $('#yearSelect').change(function () {
        var selectedYear = $(this).val();
        updateGraph(selectedYear);
    });
});
