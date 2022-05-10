 function sign_up() {
     let username = $("#input-id").val()
     let password = $("#input-password").val()
     let password2 = $("#check_password").val()
     let nickname = $('#input-nickname').val()
     console.log(username, password, password2, nickname)


     if ($("#check_id_msg").hasClass("is-danger")) {
         alert("아이디를 다시 확인해주세요.")
         return;
     } else if (!$("#check_id_msg").hasClass("is-success")) {
         alert("아이디 중복확인을 해주세요.")
         return;
     }

     if (password == "") {
         $("#check_pw_msg").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
         $("#input-password").focus()
         return;
     } else if (!is_password(password)) {
         $("#check_pw_msg").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
         $("#input-password").focus()
         return
     } else {
         $("#check_pw_msg").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
     }
     if (password2 == "") {
         $("#check_pw_msg2").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
         $("#check_password").focus()
         return;
     } else if (password2 != password) {
         $("#check_pw_msg2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
         $("#check_password").focus()
         return;
     } else {
         $("#check_pw_msg2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
     }
     $.ajax({
         type: "POST",
         url: "/sign_up/save",
         data: {
             username_give: username,
             password_give: password,
             nickname_give: nickname
         },
         success: function (response) {
             alert("회원가입을 축하드립니다!")
             window.location.replace("/")
         }
     });

 }

function go_signup() {
    $('#check_id').toggleClass("hidden")
    $('#check_id_msg').toggleClass("hidden")
    $('#check_pw_msg').toggleClass("hidden")
    $('#check_signup_box').toggleClass("hidden")
    $('#sign-up-box').toggleClass("hidden")
}

 function is_nickname(asValue) {
     var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
     return regExp.test(asValue);
 }

 function is_password(asValue) {
     var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
     return regExp.test(asValue);
 }

 function check_dup() {
     let username = $("#input-id").val()
     console.log(username)
     if (username == "") {
         $("#check_id_msg").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
         $("#input-id").focus()
         return;
     }
     if (!is_nickname(username)) {
         $("#check_id_msg").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이").removeClass("is-safe").addClass("is-danger")
         $("#input-id").focus()
         return;
     }
     $("#check_id_msg").addClass("is-loading")
     $.ajax({
         type: "POST",
         url: "/sign_up/check_dup",
         data: {
             username_give: username
         },
         success: function (response) {

             if (response["exists"]) {
                 $("#check_id_msg").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                 $("#input-id").focus()
             } else {
                 $("#check_id_msg").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
             }
             $("#check_id_msg").removeClass("is-loading")

         }
     });
 }

 function login() {
     let username = $("#input-id").val()
     let password = $("#input-password").val()

     if (username == "") {
         $("#check_id_msg").text("아이디를 입력해주세요.")
         $("#input-username").focus()
         return;
     } else {
         $("#check_id_msg").text("")
     }

     if (password == "") {
         $("#help-password-login").text("비밀번호를 입력해주세요.")
         $("#input-password").focus()
         return;
     } else {
         $("#help-password-login").text("")
     }
     alert(username);
     $.ajax({
         type: "POST",
         url: "/sign_in",
         data: {
             username_give: username,
             password_give: password
         },
         success: function (response) {
             if (response['result'] == 'success') {
                 $.cookie('mytoken', response['token'], {path: '/'});
                 window.location.replace("main")
             } else {
                 alert(response['msg'])
             }
         }
     });
 }