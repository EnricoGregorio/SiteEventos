// Comando para deixar o ícone X do menu de navegação 'escondido' por padrão.
window.document.querySelector(".fa-times").style.display = 'none'

// Bloco para sempre atualizar o ano de direito autoral do site.
let now = new Date
let year = now.getFullYear()
window.document.getElementById('cyear').innerHTML = year

$(function() {
    // Função para quando pressionar o botão do menu, ele altere.
    $(".menu-button").click(function() {
        const menuMobile = $('nav.mobile')
        if (menuMobile.is(':hidden') == false) {
            menuMobile.slideToggle()
            window.document.querySelector(".fa-bars").style.display = 'block'
            window.document.querySelector(".fa-times").style.display = 'none'
        } else {
            menuMobile.slideToggle()
            window.document.querySelector(".fa-bars").style.display = 'none'
            window.document.querySelector(".fa-times").style.display = 'block'
        }
    })
})

