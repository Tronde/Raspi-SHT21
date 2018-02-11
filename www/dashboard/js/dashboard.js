$(document).ready(function() {
    var update = function() {
        $.ajax({
            type: "GET",
            url: "",
            async: false,
            dataType: 'json'
        }).done(function(json) {
            $('#data').html('');
            $(json.status.service_status).each(function(index, element) {
                var html = '<tr class="' + element.status + ' row-data">';
                html += '<td>' + element.host_display_name + '</td>';
                html += '<td>' + element.service_display_name + '</td>';
                html += '<td>' + element.last_check + '</td>';
                html += '<td>' + element.status_information + '</td>';
                html += '</tr>';
                $('#data').append(html);
            });
        });
    }

    setInterval(update, 30000);
});
