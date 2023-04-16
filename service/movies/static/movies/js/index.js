function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}
async function create_film_select_div(external_access_token, film_works_data) {
    for (let [pos, film_work] of Object.entries(film_works_data)) {
        document.getElementById('film_select_div').innerHTML += `
        <label class="control control--radio">${film_work['film_work_name']}
            <input type="radio" name="film_work" ${(pos == 0) ? 'checked="checked"': ''} value="${film_work['id']}):(${film_work['film_work_name']}"/>
            <div class="control__indicator"></div>
        </label>
        `
    }
    document.getElementById('film_select_div').innerHTML += `<button onclick="create_room('${external_access_token}', '${parseJwt(external_access_token)['first_name']}', '${parseJwt(external_access_token)['last_name']}');">Создать комнату</button>`;
}
async function create_room(external_access_token, first_name, last_name) {
    selected_film = document.querySelector('input[name="film_work"]:checked').value;
    var response = await create_room_r(external_access_token, selected_film.split('):(')[0]);
    if (response['success']) {
        if (!document.getElementById('user_room')) {
            document.getElementById('room_select_div').innerHTML += `
            <button class="border-top" style="display: flex;" onclick="join_room('${external_access_token}', '${response['data']['room_id']}');">
                <div class="Box-row clearfix d-flex flex-items-center js-repo-access-entry adminable">
                    <div class="d-flex flex-column flex-auto col-6">
                        <a><strong>${selected_film.split('):(')[1]}</strong></a>
                        <span class="f6 color-fg-muted">${first_name} ${last_name}</span>
                        <i class="fa-solid fa-check"></i>
                    </div>
                </div>
            </button>
            `;
        } else {
            document.getElementById('user_room').innerHTML = `
                <button class="border-top" style="display: flex;" id='user_room' onclick="join_room('${external_access_token}', '${response['data']['room_id']}');">
                    <div class="Box-row clearfix d-flex flex-items-center js-repo-access-entry adminable">
                        <div class="d-flex flex-column flex-auto col-6">
                            <a><strong>${selected_film.split('):(')[1]}</strong></a>
                            <span class="f6 color-fg-muted">${first_name} ${last_name}</span>
                            <i class="fa-solid fa-check"></i>
                        </div>
                    </div>
                </button>
                `;
            document.getElementById('user_room').onclick = `join_room('${external_access_token}', '${response['data']['room_id']}');`;
        }
    } else {
        delete_room(external_access_token);
        var response = await create_room_r(external_access_token, selected_film.split('):(')[0]);
        if (response['success']) {
            if (!document.getElementById('user_room')) {
                document.getElementById('room_select_div').innerHTML += `
                <button class="border-top" style="display: flex;" id='user_room' onclick="join_room('${external_access_token}', '${response['data']['room_id']}');">
                    <div class="Box-row clearfix d-flex flex-items-center js-repo-access-entry adminable">
                        <div class="d-flex flex-column flex-auto col-6">
                            <a><strong>${selected_film.split('):(')[1]}</strong></a>
                            <span class="f6 color-fg-muted">${first_name} ${last_name}</span>
                            <i class="fa-solid fa-check"></i>
                        </div>
                    </div>
                </button>
                `;
            } else {
                document.getElementById('user_room').innerHTML = `
                <button class="border-top" style="display: flex;" onclick="join_room('${external_access_token}', '${response['data']['room_id']}');">
                    <div class="Box-row clearfix d-flex flex-items-center js-repo-access-entry adminable">
                        <div class="d-flex flex-column flex-auto col-6">
                            <a><strong>${selected_film.split('):(')[1]}</strong></a>
                            <span class="f6 color-fg-muted">${first_name} ${last_name}</span>
                            <i class="fa-solid fa-check"></i>
                        </div>
                    </div>
                </button>
                `;
                document.getElementById('user_room').onclick = `join_room('${external_access_token}', '${response['data']['room_id']}');`;
            }
        }
    }
}
async function delete_room(external_access_token) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/delete`, {
        method: 'delete',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + external_access_token
        }
    });
    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }
    await response.json();
}

async function create_room_r(external_access_token, film_work_id) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/${film_work_id}`, {
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

async function invite_user(external_access_token, user_id) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/${user_id}/invite`, {
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
        document.getElementById(`${user_id}_in_room`).innerHTML = '<i class="fa-brands fa-tiktok"></i>';
    }
}
async function check_is_user_in_room(user_id, users) {
    for (let user of Object.values(users)) {
        if (user_id == user['user_uuid']) {
            return true
        }
    }
    return false
}

async function join_room(external_access_token, room_id) {
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
        change_chosen_room_id(room_id);
        window.location.replace('cinema_together');
    }
}

function change_chosen_room_id(chosen_room_id) {
    var response = fetch(`http://localhost/change_chosen_room_id/${chosen_room_id}`, {
        method: 'get',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
        }
    });

}

async function check_is_your_friend(user_id, friends) {
    for (let friend_id of Object.values(friends)) {
        if (friend_id == user_id) {
            return true
        }
    }
    return false
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
        document.getElementById(`${user_id}_star`).innerHTML = `<i class="fa-solid fa-star" onclick="delete_friend('${external_access_token}', '${user_id}');"></i>`;
    }
}

async function delete_friend(external_access_token, user_id) {
    var response = await fetch(`http://localhost:80/v1/delete_friend?friend_id=${user_id}`, {
        method: 'delete',
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
        document.getElementById(`${user_id}_star`).innerHTML = `<i class="fa-solid fa-star-half-stroke" onclick="add_friend('${external_access_token}', '${user_id}');"></i>`;
    }
}

async function get_room_users(external_access_token) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/users`, {
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
    return await response.json();
}

async function create_users_div(external_access_token) {
    var response = await fetch('http://localhost:80/v1/user_info', {
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
        if (parseJwt(external_access_token)['sub'] != user['id'] && user['login'] != 'admin') {
            document.getElementById('users_div').innerHTML += `
            <div class="d-flex flex-column flex-auto col-6" style="width: 300px;" id='${user['id']}'>
                <a><strong>${user['first_name']} ${user['last_name']}</strong></a>
                <a id='${user['id']}_star'>${(await check_is_your_friend(user['id'], all_users_and_friends['friends']) == true) ? `<i class="fa-solid fa-star" onclick="delete_friend('${external_access_token}', '${user['id']}');"></i>` :`<i class="fa-solid fa-star-half-stroke" onclick="add_friend('${external_access_token}', '${user['id']}');"></i>`}</a>
                <a id='${user['id']}_in_room'>${(await check_is_user_in_room(user['id'], get_room_users(external_access_token)) == true)? '<i class="fa-brands fa-tiktok"></i>' :`<i class="fa-solid fa-arrow-right" onclick="invite_user('${external_access_token}', '${user['id']}');"></i>`}</a>

            </div>
            `
        }
    }
    return all_users_and_friends['users'];

}

async function get_film_work_name_by_id(film_work_id, film_works_data) {
    for (let film_work of Object.values(film_works_data)) {
        if (film_work['id'] == film_work_id) {
            return film_work['film_work_name'];
        }
    }
}
async function get_user_name_by_id(user_id, users) {
    for (let user of Object.values(users)) {
        if (user['id'] == user_id) {
            return `${user['first_name']} ${user['last_name']}`
        }
    }
}

async function create_room_select_div(external_access_token, film_works_data, users) {
    var response = await fetch(`http://localhost:80/cinema_v1/room/rooms`, {
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
    var rooms = await response.json();
    console.log(rooms)
    for (let room of Object.values(rooms)) {
        document.getElementById('room_select_div').innerHTML += `
        <button class="border-top" style="display: flex;" ${(room['owner_uuid'] == parseJwt(external_access_token)['sub']) ? "id='user_room'": ''} onclick="join_room('${external_access_token}', '${room['id']}');">
            <div class="Box-row clearfix d-flex flex-items-center js-repo-access-entry adminable">
                <div class="d-flex flex-column flex-auto col-6">
                    <a><strong>${await get_film_work_name_by_id(room['film_work_uuid'], film_works_data)}</strong></a>
                    <span class="f6 color-fg-muted">${await get_user_name_by_id(room['owner_uuid'], users)}</span>
                    <i class="fa-solid fa-check"></i>
                </div>
            </div>
        </button>
        `;
    }
}