window.onload = (event) => {
    const newsNumber = document.getElementById("news-number");
    const newsTopic = document.getElementById("news-topic");
    const dateStart = document.getElementById("date-start");
    const dateEnd = document.getElementById("date-end");
    const queryParams = new URLSearchParams(window.location.search);

    var newsNumberParam = queryParams.get("number");
    var topicParam = queryParams.get("topic");
    var startDateParam = queryParams.get("start_date");
    var endDateParam = queryParams.get("end_date");
    newsNumber.value = newsNumberParam;
    for (var i, j = 1; i = newsTopic.options[j]; j++) {
        if (i.value == topicParam) {
            newsTopic.selectedIndex = j;
            break;
        } else {
            newsTopic.selectedIndex = 0;
        }
    };
    dateStart.value = startDateParam;
    dateEnd.value = endDateParam;

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

    dateStart.addEventListener("change", function(event) {
        updateUrlParams("start_date", event.target.value)
    });

    dateEnd.addEventListener("change", function(event) {
        updateUrlParams("end_date", event.target.value)
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

function clearFilters(){
    document.getElementById("news-number").value = 10;
    document.getElementById("news-topic").selectedIndex = 0;
    document.getElementById("date-start").value = "";
    document.getElementById("date-end").value = "";
    let searchParams = new URLSearchParams(window.location.search);
    searchParams.set("number", 10)
    searchParams.delete("topic");
    searchParams.delete("start_date");
    searchParams.delete("end_date");
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