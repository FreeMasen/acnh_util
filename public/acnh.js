
(function () {
    const ELEMENTS = Object.freeze({
        FISH_BODY: document.querySelector('#fish-table tbody'),
        BUGS_BODY: document.querySelector('#bug-table tbody'),
        SEA_CREATURE_BODY: document.querySelector('#sea-creature-table tbody'),
        TOGGLE_CAUGHT: document.getElementById('global-toggle-caught'),
        TOGGLE_DONATED: document.getElementById('global-toggle-donated'),
        USER_LIST: document.getElementById('user-list-wrapper'),
    });
    const SORT_ORDERS = {
        fish: {
            key: 'name',
            desc: true,
        },
        bugs: {
            key: 'name',
            desc: true,
        },
        sea_creatures: {
            key: 'name',
            desc: true,
        },
    }
    let now = new Date(1970, 1, 1);
    let show_caught = (localStorage.getItem('show_caught') || 'true') === 'true';
    let show_donated = (localStorage.getItem('show_donated') || 'true') === 'true';
    let users = [];
    let selected_user_id = localStorage.getItem('selected_user_id') || -1;
    let pending_timeout = null;
    handle_btn_classes(ELEMENTS.TOGGLE_CAUGHT, show_caught);
    handle_btn_classes(ELEMENTS.TOGGLE_DONATED, show_donated);
    ELEMENTS.TOGGLE_CAUGHT.addEventListener('click', async () => {
        show_caught = !show_caught;
        localStorage.setItem('show_caught', show_caught);
        handle_btn_classes(ELEMENTS.TOGGLE_CAUGHT, show_caught);
        await main();
    });
    ELEMENTS.TOGGLE_DONATED.addEventListener('click', async () => {
        show_donated = !show_donated;
        localStorage.setItem('show_donated', show_donated);
        handle_btn_classes(ELEMENTS.TOGGLE_DONATED, show_donated);
        await main();
    });
    function handle_btn_classes(btn, flag) {
        console.log('handle_btn_classes', btn, flag);
        if (flag) {
            btn.classList.add('is-error');
            btn.classList.remove('is-success');
        } else {
            btn.classList.add('is-success');
            btn.classList.remove('is-error');
        }
    }
    async function main() {
        if (!!pending_timeout) {
            clearTimeout(pending_timeout);
            pending_timeout = setTimeout(tick, 1000 * 60)
        }
        await get_user_list();
        if (selected_user_id === -1) {
            if (users.length === 0) {
                return;
            }
            selected_user_id = users[0].user_id;
        }
        render_user_tabs();
        let res = await fetch(`/${selected_user_id}/available/${now.getHours()}/${now.getMonth() + 1}`);
        if (res.status !== 200) {
            console.error('failed to get active', res);
            return;
        }
        let available = await res.json();
        sort_collection(available.AvailableFor.fish);
        sort_collection(available.AvailableFor.bugs);
        sort_collection(available.AvailableFor.sea_creatures);
        render_fishes(available.AvailableFor.fish);
        render_bugs(available.AvailableFor.bugs);
        render_sea_creatures(available.AvailableFor.sea_creatures);
    }

    function filter_creature(c) {
        if (!show_caught && c.caught) {
            return false;
        }
        if (!show_donated && creature.donated) {
            return false;
        }
        return true;
    }

    function render_user_tabs() {
        clear_dom_node(ELEMENTS.USER_LIST);
        for (const user of users) {
            let btn = document.createElement('button');
            btn.dataset.userId = user.user_id;
            btn.classList.add('nes-btn');
            if (user.user_id === selected_user_id) {
                btn.classList.add('is-success');
            } else {
                btn.classList.remove('is-success');
            }
            btn.innerText = user.name;
            btn.addEventListener('click', ev => {
                console.log(ev.currentTarget.dataset)
                if (!!ev.currentTarget.dataset.userId) {
                    selected_user_id = parseInt(ev.currentTarget.dataset.userId);
                    let container = ev.currentTarget.parentElement;
                    for (let i = 0; i < container.childElementCount; i++) {
                        container.children[i].classList.remove('is-success');
                    }
                    ev.currentTarget.classList.add('is-success');
                    main().then(() => {});
                }
            });
            ELEMENTS.USER_LIST.appendChild(btn);
        }
    }
    
    function render_fishes(fish) {
        clear_dom_node(ELEMENTS.FISH_BODY);
        for (let f of fish.filter(filter_creature)) {
            ELEMENTS.FISH_BODY.appendChild(render_fish(f));
        }
    }

    function render_fish(f) {
        let tr = document.createElement('tr');
        tr.dataset.name = f.name;
        tr.dataset.location = f.location;
        tr.dataset.size = size_as_number(f.size.size);
        tr.dataset.value = f.value;
        tr.dataset.active = is_active(f);
        tr.dataset.status = f.caught + f.donated;
        let size_text = size_as_words(f.size.size);
        if (f.size.modifier) {
            size_text += ` ${f.size.modifier}`;
        }
        tr.innerHTML = `
        <td class="cell-name">${f.name}</td>
        <td class="cell-image">
            <img src="${generate_image_src(f.name)}" class="thumbnail-image nes-avatar" />
        </td>
        <td class="cell-location">${f.location}</td>
        <td class="cell-value">${f.value}</td>
        <td class="cell-size">${size_text}</td>
        <td class="cell-active">${active_marker(f)}</td>
        <td class="cell-status">${status_as_text(f.caught, f.donated)}</td>`;
        tr.appendChild(render_action_cell(f, 'fish'));
        tr.appendChild(render_warning_cell(f));
        return tr;
    }
    function render_sea_creatures(creatures) {
        clear_dom_node(ELEMENTS.SEA_CREATURE_BODY);
        for (let c of creatures.filter(filter_creature)) {
            ELEMENTS.SEA_CREATURE_BODY.appendChild(render_sea_creature(c));
        }
    }

    function render_sea_creature(c) {
        let tr = document.createElement('tr');
        tr.dataset.name = c.name;
        tr.dataset.size = c.size
        tr.dataset.value = c.value;
        tr.dataset.active = is_active(c);
        tr.dataset.speed = c.speed;
        tr.dataset.status = c.caught + c.donated;
        tr.innerHTML = `
        <td class="cell-name">${c.name}</td>
        <td class="cell-image">
            <img src="${generate_image_src(c.name)}" class="thumbnail-image" />
        </td>
        <td class="cell-value">${c.value}</td>
        <td class="cell-speed">${speed_as_text(c.speed)}</td>
        <td class="cell-size">${size_as_words(c.size)}</td>
        <td class="cell-active">${active_marker(c)}</td>
        <td class="cell-status">${status_as_text(c.caught, c.donated)}</td>`;
        tr.appendChild(render_action_cell(c, 'sea_creature'));
        tr.appendChild(render_warning_cell(c));
        return tr;
    }

    function render_bugs(bugs) {
        clear_dom_node(ELEMENTS.BUGS_BODY);
        for (let b of bugs.filter(filter_creature)) {
            ELEMENTS.BUGS_BODY.appendChild(render_bug(b));
        }
    }

    function render_action_cell(creature, kind) {
        let td = document.createElement('td');
        td.classList.add('cell-action');
        let div = document.createElement('div');
        div.classList.add('cell-action-buttons');
        let caught_btn = document.createElement('button');
        caught_btn.innerHTML = '<i title="status" class="nes-icon trophy is-small"></i>';
        caught_btn.title = 'Toggle Caught';
        if (creature.caught) {
            caught_btn.classList.add('is-error');
            
        } else {
            caught_btn.classList.add('is-success');
        }
        caught_btn.classList.add('nes-btn');
        caught_btn.addEventListener('click', () => {
            creature.caught = !creature.caught;
            creature.donated = false;
            let update_body = {
                id: creature.id,
                caught: creature.caught,
                donated: creature.donated,
            };
            fetch(`${selected_user_id}/update/${kind}`, {method: 'POST', body: JSON.stringify(update_body),
            headers: {'Content-Type': 'application/json'}})
                .then(main().then(() => {}))
        });
        div.appendChild(caught_btn);
        if (creature.caught) {
            let donated_btn = document.createElement('button');
            donated_btn.innerHTML = '<i title="donated" class="nes-icon coin is-small"></i>';
            donated_btn.title = 'toggle donated';
            if (creature.donated) {
                donated_btn.classList.add('is-error');
            } else {
                donated_btn.classList.add('is-success');
            }
            
            donated_btn.classList.add('nes-btn');
            donated_btn.addEventListener('click', () => {
                creature.donated = !creature.donated;
                let update_body = {
                    id: creature.id,
                    caught: creature.caught,
                    donated: creature.donated,
                };
                fetch(`${selected_user_id}/update/${kind}`, {method: 'POST', body: JSON.stringify(update_body),
                headers: {'Content-Type': 'application/json'}})
                    .then(main().then(() => {}))
            });
            div.appendChild(donated_btn);
        }
        td.appendChild(div);
        return td;
    }

    function render_bug(b) {
        let tr = document.createElement('tr');
        tr.dataset.name = b.name;
        tr.dataset.location = b.location;
        tr.dataset.value = b.value;
        tr.dataset.active = is_active(b);
        tr.dataset.status = b.caught + b.donated;
        
        tr.innerHTML = `
        <td class="cell-name">${b.name}</td>
        <td class="cell-image">
            <img src="${generate_image_src(b.name)}" class="thumbnail-image" />
        </td>
        <td class="cell-location">${b.location}</td>
        <td class="cell-value">${b.value}</td>
        <td class="cell-active">${active_marker(b)}</td>
        <td class="cell-status">${status_as_text(b.caught, b.donated)}</td>
        `;
        tr.appendChild(render_action_cell(b, 'bug'));
        tr.appendChild(render_warning_cell(b));
        return tr;
    }

    function active_marker(creature) {
        let ret = '<label><input type="checkbox" class="nes-checkbox"';
        if (is_active(creature)) {
            ret += ' checked';
        }

        return ret + ' disabled /><span></span></label>';
    }

    function is_active(creature) {
        let now = new Date();
        if (!creature.months_active[now.getMonth()]) {
            console.error('error, month is not active for ', creature.name);
            return false;
        }
        if (!creature.hours_active[now.getHours()]) {
            console.error('error, hour is not active for ', creature.name, now.getHours(), creature.hours_active.slice(now.getHours() - 2, now.getHours() + 2));
            return false;
        }
        return true;
    }

    function size_as_number(size) {
        switch(size) {
            case 'Small': return 1;
            case 'Medium': return 2;
            case 'Large': return 3;
            case 'ExtraLarge': return 4;
            case 'Gargantuan': return 5;
            case 'Humongous': return 6;
        }
    }

    function size_as_words(size) {
        switch(size) {
            case 'Small': return 'XS';
            case 'Medium': return 'S';
            case 'Large': return 'M';
            case 'ExtraLarge': return 'L';
            case 'Gargantuan': return 'XL';
            case 'Humongous': return 'XXL';
        }
    }

    function status_as_text(caught, donated) {
        let ret = '<i title="not caught" class="nes-icon close is-small"></i>';
        if (caught) {
            ret = '<i title="caught" class="nes-icon trophy is-small"></i>';
        }
        if (donated) {
            ret += '<i title="donated" class="nes-icon coin is-small"></i>';
        }
        return ret;
    }

    function speed_as_text(speed) {
        switch (speed) {
            case 'Stationary': return 'None';
            case 'VerySlow': return 'V. Slow';
            case 'Slow': return 'Slow';
            case 'Medium': return 'Medium';
            case 'Fast': return 'Fast';
            case 'VeryFast': return 'V. Fast';
        }
    }

    function render_warning_cell(creature) {
        let td = document.createElement('td');
        td.classList.add('warning-cell');
        let hour = now.getHours() + 1;
        let month = now.getMonth() + 1;
        if (hour >= creature.hours_active.length) {
            hour = 0;
        }
        if (month >= creature.months_active.length) {
            month = 0;
        }
        let inner = '';
        let title = '';
        let next_hour = creature.hours_active[hour];
        let next_month = creature.hours_active[month];
        let size = 'is-small';
        let fill = 'is-empty';
        if (next_hour) {
            size = 'is-medium';
        }
        if (next_month) {
            fill = ''
        }
        const clock_img = '<img class="warning-image" src="/images/clock.png" />';
        const cal_img = '<img class="warning-image" src="/images/calendar.png" />';
        if (!next_hour && !next_month) {
            title = '"will not be around after hour\nwill not be around next month';
            inner = clock_img + cal_img;
        } else if (!next_hour) {
            title = 'will not be around after this hour';
            inner = clock_img;
        } else if (!next_month) {
            title = 'will not be around next month';
            inner = cal_img;
        } else {
            title = 'Will be around for the next hour and month';
        }
        
        td.innerHTML = inner;
        return td;
    }
    function clear_dom_node(node) {
        while (node.hasChildNodes()) {
            node.removeChild(node.lastChild);
        }
    }
    function generate_image_src(name) {
        let base = name.replace(/[-\s']/g, '').toLowerCase();
        return `/images/${base}.png`;
    }

    function sort_table(table, data_key, desc) {
        console.log('sort table', data_key, desc);
        let rows = [];
        while (table.hasChildNodes()) {
            rows.push(table.removeChild(table.firstChild));
        }
        let updated = rows.sort((l, r) => {
            let left, right;
            if (desc) {
                left = l.dataset[data_key];
                right = r.dataset[data_key];
            } else {
                left = r.dataset[data_key];
                right = l.dataset[data_key];
            }
            console.log(left, right);
            try {
                left = parseInt(left);
                right = parseInt(right);
                return left - right;
            } catch (e) {
                console.log('string cmp');
                return left.toLowerCase().localeCompare(right.toLowerCase());
            }
        });
        for (const row of updated) {
            table.appendChild(row);
        }
    }

    function sort_collection(collection, key, desc) {
        collection.sort((l, r) => {
            let left, right;
            if (desc) {
                left = l[key];
                right = r[key];
            } else {
                left = r[key];
                right = l[key];
            }
            try {
                left = parseInt(left);
                right = parseInt(right);
                return left - right;
            } catch (e) {
                return left.toLowerCase().localeCompare(right.toLowerCase());
            }
        });
    }

    function setup_sorters() {
        let headers = document.querySelectorAll('#fish-table thead tr th');
        for (let i = 0; i < headers.length; i++) {
            let header = headers[i];
            if (!!header.dataset.sort) {
                header.addEventListener('click', (ev) => {
                    let header = ev.currentTarget;
                    if (header.dataset.desc && header.dataset.desc === 'true') {
                        header.dataset.desc = false;
                    } else {
                        header.dataset.desc = true;
                    }
                    SORT_ORDERS.fish.key = header.dataset.sort;
                    SORT_ORDERS.fish.desc = header.dataset.desc;
                    sort_table(ELEMENTS.FISH_BODY, header.dataset.sort, header.dataset.desc);
                });
            }
        }
        headers = document.querySelectorAll('#bug-table thead tr th');
        for (let i = 0; i < headers.length; i++) {
            let header = headers[i];
            if (!!header.dataset.sort) {
                header.addEventListener('click', (ev) => {
                    let header = ev.currentTarget;
                    header.dataset.desc = !header.dataset.desc;
                    SORT_ORDERS.bugs.key = header.dataset.sort;
                    SORT_ORDERS.bugs.desc = header.dataset.desc;
                    sort_table(ELEMENTS.BUGS_BODY, header.dataset.sort, header.dataset.desc);
                });
            }
        }
        headers = document.querySelectorAll('#sea-creature-table thead tr th');
        for (let i = 0; i < headers.length; i++) {
            let header = headers[i];
            if (!!header.dataset.sort) {
                header.addEventListener('click', (ev) => {
                    let header = ev.currentTarget;
                    header.dataset.desc = !header.dataset.desc;
                    SORT_ORDERS.sea_creatures.key = header.dataset.sort;
                    SORT_ORDERS.sea_creatures.desc = header.dataset.desc;
                    sort_table(ELEMENTS.SEA_CREATURE_BODY, header.dataset.sort, header.dataset.desc);
                });
            }
        }

    }
    async function get_user_list() {
        let r = await fetch('/users');
        if (r.status != 200) {
            console.error('failed to get users:', await r.text());
            return;
        }
        let user_raw = await r.json();
        console.log(user_raw);
        users = user_raw.Users;
    }
    function tick() {
        pending_timeout = null;
        function time_eq(then, now) {
            return now.getFullYear() == then.getFullYear()
            && now.getHours() == then.getHours();
        }
        let new_now = new Date();
        if (!time_eq(now, new_now)) {
            now = new_now
            main().then(() => {
                pending_timout = setTimeout(tick, 1000 * 60);
            });
        } else {
            pending_timeout = setTimeout(tick, 1000 * 60);
        }
    }
    tick()
    setup_sorters();
})();