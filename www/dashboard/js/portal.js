$(document).ready(function() {
    $('.card').each(function(index, element) {
        $(element).on('click', function(e) {
            $(this).effect('puff', {}, 500);
        });

        if ((index + 1) % 4 == 0) {
            $(element).attr('class', $(element).attr('class') + ' green');
            return;
        }
        if ((index + 1) % 3 == 0) {
            $(element).attr('class', $(element).attr('class') + ' purple');
            return;
        }
        if ((index + 1) % 2 == 0) {
            $(element).attr('class', $(element).attr('class') + ' blue');
            return;
        }
        if ((index + 1) % 1 == 0) {
            $(element).attr('class', $(element).attr('class') + ' orange');
            return;
        }
    });
});
