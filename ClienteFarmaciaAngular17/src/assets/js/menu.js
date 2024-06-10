window.addEventListener("load", inicializar)

function inicializar(){
    document.getElementById('mobile-menu').addEventListener('click', function() {
    document.querySelector('.menu-expansible').classList.toggle('active');
  });
}