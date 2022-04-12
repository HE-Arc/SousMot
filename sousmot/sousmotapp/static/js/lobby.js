let url = `ws://${window.location.host}/ws/socket-server/`;

const gameSocket = new WebSocket(url);



function createHtmlUser(username, is_guest)
{
    if(is_guest)
        return `
        <article class="media">
            <figure class="media-left">
                <i class="fa fa-user fa-2x" aria-hidden="true"></i>
            </figure>
            <div class="media-content">
                <div class="content">
                    <p><strong>${username}</strong> <span class="tag is-link">Guest</span></p>
                </div>
            </div>
        </article>
        `;
    else
        return `
        <article class="media">
            <figure class="media-left">
                <i class="fa fa-user fa-2x" aria-hidden="true"></i>
            </figure>
            <div class="media-content">
                <div class="content">
                    <p><strong>${username}</strong> <span class="tag is-warning">Host</span></p>
                </div>
            </div>
        </article>
        `;
}

gameSocket.onmessage = function(e){
    let data = JSON.parse(e.data);
    // console.log('Data', data);

    if(data.type === 'redirection')
    {
        // Simulate an HTTP redirect:
        setTimeout(function(){
            window.location.href = urlredirect;
         }, 1500);
    }

    if(data.type === 'users')
    {
        listUsers = data.message.split(';');
        var element = document.getElementById("contestant-list"); 
        element.innerHTML = '';
        var userHere = document.getElementById('user-here').getAttribute('value');

        listUsers.forEach( val => {

            is_guest_val = val.slice(-1);
            is_guest = true;
            if(is_guest_val === "0")
            {
                is_guest = false;
            }

            val = val.slice(0, -1);
            if(val !== userHere)
            {
                element.insertAdjacentHTML("beforeend", createHtmlUser(val, is_guest));
            }
            
        });
    }
}

function redirectEveryone(){
    gameSocket.send(JSON.stringify({
        "message": "startgame"
    }))
}
