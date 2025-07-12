
let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');

async function render() {
    const result = await fetch('http://127.0.0.1:8000/api/tracks/',{
        method: 'GET',
        headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
    })
    let html = ''
    let json = await result.json()
    json.forEach(element => {
        html += `
        <div class="card mb-3" style="max-width: 540px;" >
    <div class="row g-0">
        <div class="col-md-4">
            <img
                src="Image Source"
                class="img-fluid rounded-start"
                alt="Card title"
            />
        </div>
        <div class="col-md-8">
            <div class="card-body">
                <h5 class="card-title">${element.subject}</h5>
                <p class="card-text">
            ${element.description}
                </p>
                <p class="card-text">
                    <small class="text-muted"
                        >${element.created_at}</small
                    >
                </p>
            </div>
        </div>
    </div>
</div>
`
    });
    document.querySelector('#container')
    .innerHTML = html
}
render()