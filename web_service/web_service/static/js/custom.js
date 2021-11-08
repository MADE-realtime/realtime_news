window.onload = (event) => {
    const newsNumber = document.getElementById("news-number");
    const newsTopic = document.getElementById("news-topic");

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

    newsNumber.addEventListener("keyup", function(event) {
        updateUrlParams("number", event.target.value)
    });

    newsTopic.addEventListener("change", function(event) {
        updateUrlParams("topic", event.target.value)
    });

};

function clearDefaultUrlParams(){
    var newsTopic = document.getElementById("news-topic");
    if (newsTopic.value == ''){
        let searchParams = new URLSearchParams(window.location.search);
        searchParams.delete("topic");
        if (window.history.replaceState) {
            const url = window.location.protocol
                        + "//" + window.location.host
                        + window.location.pathname
                        + "?"
                        + searchParams.toString();

            window.history.replaceState({
                path: url
            }, "", url)
        }
    }
}

function updateUrlParams(param, target){
    clearDefaultUrlParams();
    let searchParams = new URLSearchParams(window.location.search);
    searchParams.set(param, target);
    if (window.history.replaceState) {
        const url = window.location.protocol
                    + "//" + window.location.host
                    + window.location.pathname
                    + "?"
                    + searchParams.toString();

        window.history.replaceState({
            path: url
        }, "", url)
    }
    location.reload();
}
