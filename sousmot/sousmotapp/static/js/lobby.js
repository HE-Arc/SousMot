let url = `ws://${window.location.host}/ws/socket-server/`;

const chatSocket = new WebSocket(url);



function createHtmlUser(username, is_guest)
{
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
}

chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data);
    console.log('Data', data);

    if(data.type === 'response' || data.type === 'user_check')
    {
        console.log(data.message);
    }

    if(data.type === 'users')
    {
        listUsers = data.message.split(';');
        var element = document.getElementById("contestant-list"); 
        element.innerHTML = '';
        var userHere = document.getElementById('user-here').getAttribute('value');

        listUsers.forEach(val => {
            if(val !== userHere)
            {
                element.insertAdjacentHTML("beforeend", createHtmlUser(val, true));
            }
            
        });
            
        
    }

}
