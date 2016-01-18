$(function () {
        function onSelect(obj){ /*TODO Сделать без костыля с разбитием значений знаком ^ */
            $('#id_view_path').val(obj.view_path);
            console.log(obj);
            return obj.text;
        }
        function tResult(obj){
            console.log('template result', obj);
            return obj.text;
            //splitted = obj.text.split('^');
            //return splitted[0];
        }
        function pResults(data, params){
                return {
                    results: data.results,
                    pagination: {
                      more: (params.page * 30) < data.total_count
                    }
                };
            }


        var data = [{ id: 0, text: 'enhancement','children':[{ id: 1, text: 'bug' }, { id: 2, text: 'duplicate' }]}, { id: 3, text: 'invalid' }, { id: 4, text: 'wontfix' }];

        $('.django-select2[name="name"]').djangoSelect2({
            templateSelection: onSelect,
            templateResult: tResult,
            }
        );
        //$('#test').select2({
        //        ajax: {
        //            url: "http://127.0.0.1:8000/kb_name/",
        //            dataType: 'json',
        //            delay: 250,
        //            data: function (params) {
        //              return {
        //                q: params.term, // search term
        //                page: params.page
        //              };
        //            },
        //            processResults: pResults,
        //            cache: true
        //        },
        //        minimumInputLength: 0,
        //    }
        //)
    });