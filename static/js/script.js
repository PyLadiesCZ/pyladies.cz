document.addEventListener("DOMContentLoaded", function () {
    if (!document.body.className.includes('index-page')) {
        var hamburger = document.getElementById('hamburger-menu');
        hamburger.addEventListener("click", function () {
            document.body.classList.toggle('menu-shown');
            return false;
        });
        document.body.classList.add('have-menu');
    }
});
