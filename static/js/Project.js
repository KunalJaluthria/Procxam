function Change_nav(){
    var navbar = document.getElementById('navbar');
    var scrollVal = window.scrollY;
    if(scrollVal>0)
    {
        navbar.classList.add('ChangeNav');
    }
    else
    {
        navbar.classList.remove('ChangeNav');
    }
}

function Remove_pic(){
    var pic = document.getElementById('LensId');
    var scrollValue = window.scrollY;
    if(scrollValue>280)
    {
        pic.classList.add('Remove');
    }
    else
    {
        pic.classList.remove('Remove');
    }
}

window.addEventListener('scroll', Change_nav);
window.addEventListener('scroll', Remove_pic);

window.onload = function checklogin(){
    var login = document.getElementById("loginn");
    var logout = document.getElementById("log_out");
    $.post("http://127.0.0.1:5000/checklogin",
    {
    },
    function(data){
        var value = data;
        if(value=="user")
        {
            login.classList.add('log_inn');
            logout.classList.add('loggout');
            host_test.removeAttribute('disabled');
            host_meet.removeAttribute('disabled');
        }
        else
        {
            logout.classList.add('log');
            host_test.setAttribute('disabled', 'disabled');
            host_meet.setAttribute('disabled', 'disabled');
        }
    });
}