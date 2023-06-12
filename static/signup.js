var password = document.getElementById("password")
, confirm_password = document.getElementById("confirmPassword")

function validatePassword(){
    if(password.value != confirm_password.value){
        confirm_password.setCustomValidity("Password doesn't match!")
    }else{
        confirm_password.setCustomValidity("");
    }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
