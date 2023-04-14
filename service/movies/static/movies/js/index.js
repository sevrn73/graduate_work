async function create_film_select_div(film_works_data) {
    for (let [pos, film_work] of Object.entries(film_works_data)) {
        document.getElementById('film_select_div').innerHTML += `
        <label class="control control--radio">${film_work['film_work_name']}
            <input type="radio" name="radio" ${(pos == 0) ? 'checked="checked"': ''} id='${film_work['id']}' value="${film_work['film_work_url_id']}"/>
            <div class="control__indicator"></div>
        </label>
        `
    }
    document.getElementById('film_select_div').innerHTML += '<button onclick="create_room();">Создать комнату</button>';
}
async function create_room() {
    var response = await create_room_r();
    if (result['success']) {
        document.getElementById(user_id).innerHTML += `
        <button class="border-top" style="display: flex;">
            <div class="Box-row clearfix d-flex flex-items-center js-repo-access-entry adminable">
                <div class="d-flex flex-column flex-auto col-6">
                    <a><strong>Название фильма</strong></a>
                    <span class="f6 color-fg-muted">Владелец</span>
                    <i class="fa-solid fa-check"></i>
                </div>
            </div>
        </button>
        `;
    } else {
        delete_room();
        var response = await create_room_r();
        if (result['success']) {
            document.getElementById(user_id).innerHTML += `
            <button class="border-top" style="display: flex;">
                <div class="Box-row clearfix d-flex flex-items-center js-repo-access-entry adminable">
                    <div class="d-flex flex-column flex-auto col-6">
                        <a><strong>Название фильма</strong></a>
                        <span class="f6 color-fg-muted">Владелец</span>
                        <i class="fa-solid fa-check"></i>
                    </div>
                </div>
            </button>
            `;
        }
    }
}
async function delete_room() {

}

async function create_room_r() {
    var response = await fetch(`http://localhost:80/cinema_v1/room/`, {
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + external_access_token
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    return await response.json();
}

async function invite_user(room_id, user_id) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/${room_id}/${user_id}/invite`, {
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + external_access_token
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    var result = await response.json();
    if (result['success']) {
        document.getElementById(user_id).innerHTML += '<i class="fa-solid fa-check"></i>';
    }
}

async function join_room(room_id) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/${room_id}/join`, {
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + external_access_token
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    var result = await response.json();
    if (result['success']) {
        await change_chosen_room_id(room_id);
        window.location.replace(window.location.host + '/cinema_together');
    }
}
async function change_chosen_room_id(chosen_room_id) {
    var response = await fetch(`http://localhost/change_chosen_room_id/${chosen_room_id}`, {
        method: 'get',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    await response.json();

}

async function check_is_your_friend(user_id, friends) {

}
async function add_friend(external_access_token, user_id) {
    var response = await fetch(`http://localhost:80/v1/add_friend?friend_id=${user_id}`, {
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + external_access_token
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    var result = await response.json();
    if (result) {
        document.getElementById(`${user['id']}_star`).innerHTML = '<i class="fa-solid fa-star"></i>';
    }
}

async function create_users_div(external_access_token) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/${room_id}/users/`, {
        method: 'get',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + external_access_token
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    var all_users_and_friends = await response.json();

    for (let user of Object.values(all_users_and_friends['users'])) {
        document.getElementById('users_div').innerHTML += `
        <div class="d-flex flex-column flex-auto col-6" style="width: 300px;" id='${user['id']}'>
            <a><strong>${user['']} ${user['']}</strong></a>
            <a id='${user['id']}_star'>${(user['id'], all_users_and_friends['friends'])? '<i class="fa-solid fa-star"></i>' :`<i class="fa-solid fa-star-half-stroke" onclick="add_friend('${external_access_token}', '${user['id']}');"></i>`}</a>
            <a></a>

        </div>
        `
        // <i class="fa-solid fa-calendar-circle-user"></i> добавить в комнату
        // <i class="fa-solid fa-calendar-users"></i> в комнате
    }

}