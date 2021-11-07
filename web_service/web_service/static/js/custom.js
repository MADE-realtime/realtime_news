window.onload = (event) => {
    document.querySelectorAll('.show-more-button').forEach(item => {
        item.addEventListener('click', function() {
        // If text is shown less, then show complete
            if(this.getAttribute('data-more') == 0) {
                this.setAttribute('data-more', 1);
                this.style.display = 'block';
                this.innerHTML = 'Скрыть';

                this.parentElement.parentElement.querySelector('.full-text').style.display = 'inline';
                this.parentElement.parentElement.querySelector('.text-dots').style.display = 'none';

                this.previousElementSibling.style.display = 'none';
                this.previousElementSibling.previousElementSibling.style.display = 'inline';
            }
            // If text is shown complete, then show less
            else if(this.getAttribute('data-more') == 1) {
                this.setAttribute('data-more', 0);
                this.style.display = 'inline';
                this.innerHTML = 'Читать полностью';

                this.parentElement.parentElement.querySelector('.full-text').style.display = 'none';
                this.parentElement.parentElement.querySelector('.text-dots').style.display = 'inline';

                this.previousElementSibling.style.display = 'inline';
                this.previousElementSibling.previousElementSibling.style.display = 'none';
            }
        });
    });
};
