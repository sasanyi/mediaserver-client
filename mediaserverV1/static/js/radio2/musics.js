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
        url: "/api/musics",
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
                        return '<a href="/music-edit/' + row.id + '"><button type="button" class="btn mb-1 btn-primary">Edit<span class="btn-icon-right"><i class="fa fa-edit"></i></span></button></a>'
                    },
                    title: 'Edit'
                }
            ]
        });
    });


});