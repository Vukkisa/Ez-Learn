function checkPassword(form) {
    password1 = form.password.value;
    password2 = form.con_password.value;

    if (password1.length < 8) {
        alert('password should be of minimum 8 charecters')
        return false
    }

    // If password not entered
    else if (password1 == ''){
        alert ("Please enter Password");
        return false
    }     
    // If confirm password not entered
    else if (password2 == ''){
        alert ("Please enter confirm password");
        return false
    }

    else if (password1.search(/[a-z]/) < 0) {
        alert ("Your password must contain at least one lowercase letter.");
        return false
    }

    else if (password1.search(/[A-Z]/) < 0) {
        alert ("Your password must contain at least one uppercase letter.");
        return false
    }


    else if (password1.search(/[0-9]/) < 0) {
        alert ("Your password must contain at least one digit.");
        return false
    }
    
    else if (password1.search(/[\!\@\#\$\%\^\&\*\(\)\_\+\.\,\;\:\-]/) < 0) {
        alert ("Your password must contain at least one special character.");
        return false
    }
          
    // If Not same return False.    
    else if (password1 != password2) {
        alert ("\nPassword did not match: Please try again...")
        return false;
    }

    // If same return True.
    else{
        return true;
    }
}
    
function hello(){
    alert('hello')
}