    $(function() {
        $("#createPlace").validate(

        );
        $.extend( $.validator.messages, {
            required: "필수 항목입니다.",
            number: "숫자를 입력해 주십시오.",
            min: $.validator.format( "{0} 이상의 값을 입력하세요." )
        });
    });
