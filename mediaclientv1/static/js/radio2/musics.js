$(document).ready(function () {
    $(".loader").hide().bind({
        ajaxStart: function () {
            $(this).show();
        },
        ajaxStop: function () {
            $(this).hide();
        }
    });
    $.ajax({
        url: "http://mmnhu.ddns.net:9000/api/musics",
    }).done(function (data) {
        console.log(data)
        $("#musics-table").dataTable({
            data: data["musics"],
            lengthMenu: [[2, 5, 10, 25, 50, -1], [2, 5, 10, 25, 50, "All"]],
            columns: [
                {data: 'real_path', title: 'Path'},
                {data: 'meta.title', title: 'Title'},
                {data: 'meta.artist', title: 'Artist(s)'},
                {data: 'meta.date', title: 'Year'},
                {data: 'meta.genre', title: 'Genre'},
                {
                    "render": function (data, type, row, meta) {
                        return '<form method="POST" action="/download"><input type="hidden" name="path" value="'+row.real_path+'" /><button type="submit" class="btn mb-1 btn-primary">Letöltés<span class="btn-icon-right"><i class="fa fa-download"></i></span></button></form>'
                    },
                    title: 'Download'
                }
            ]
        });
    });


});