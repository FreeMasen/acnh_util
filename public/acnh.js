
(function () {
    const ELEMENTS = Object.freeze({
        FISH_BODY: document.querySelector('#fish-table tbody'),
        BUGS_BODY: document.querySelector('#bug-table tbody'),
        SEA_CREATURE_BODY: document.querySelector('#sea-creature-table tbody'),
        TOGGLE_CAUGHT: document.getElementById('global-toggle-caught'),
        TOGGLE_DONATED: document.getElementById('global-toggle-donated'),
    });
    let now = new Date(1970, 1, 1);
    let show_caught = (localStorage.getItem('show_caught') || 'true') === 'true';
    let show_donated = (localStorage.getItem('show_donated') || 'true')=== 'true';
    ELEMENTS.TOGGLE_CAUGHT.addEventListener('click', async () => {
        show_caught = !show_caught;
        localStorage.setItem('show_caught', show_caught);
        await main();
    });
    ELEMENTS.TOGGLE_DONATED.addEventListener('click', async () => {
        show_donated = !show_donated;
        localStorage.setItem('show_donated', show_donated);
        await main();
    });
    async function main() {
        let res = await fetch(`/available/${now.getHours()}/${now.getMonth() + 1}`);
        if (res.status !== 200) {
            console.error('failed to get active', res);
            return;
        }
        let available = await res.json();
        console.log(available);
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
    
    function render_fishes(fish) {
        clear_dom_node(ELEMENTS.FISH_BODY);
        for (let f of fish.filter(filter_creature)) {
            ELEMENTS.FISH_BODY.appendChild(render_fish(f));
        }
    }

    function render_fish(f) {
        let tr = document.createElement('tr');
        tr.innerHTML = `
        <td class="cell-name">${f.name}</td>
        <td class="cell-image">
            <img src="${generate_image_src(f.name)}" class="thumbnail-image" />
        </td>
        <td class="cell-location">${f.location}</td>
        <td class="cell-value">${f.value}</td>
        <td class="cell-size">${f.size.size}</td>
        <td class="cell-active">${active_marker(f)}</td>
        <td class="cell-status">${status_as_text(f.caught, f.donated)}</td>`;
        tr.appendChild(render_action_cell(f, 'fish'))
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
        tr.innerHTML = `
        <td class="cell-name">${c.name}</td>
        <td class="cell-image">
            <img src="${generate_image_src(c.name)}" class="thumbnail-image" />
        </td>
        <td class="cell-value">${c.value}</td>
        <td class="cell-speed">${c.speed}</td>
        <td class="cell-size">${c.size}</td>
        <td class="cell-active">${active_marker(c)}</td>
        <td class="cell-status">${status_as_text(c.caught, c.donated)}</td>`;
        tr.appendChild(render_action_cell(c, 'sea_creature'))
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
        let caught_btn = document.createElement('button');
        caught_btn.innerText = creature.caught ? 'Uncatch' : 'Catch';
        caught_btn.addEventListener('click', () => {
            creature.caught = !creature.caught;
            creature.donated = false;
            fetch(`/update/${kind}`, {method: 'POST', body: JSON.stringify(creature),
            headers: {'Content-Type': 'application/json'}})
                .then(main().then(() => {}))
        });
        td.appendChild(caught_btn);
        if (creature.caught) {
            let donated_btn = document.createElement('button');
            donated_btn.innerText = creature.donated ? 'Undonate' : 'Donate';
            donated_btn.addEventListener('click', () => {
                creature.donated = !creature.donated;
                fetch(`/update/${kind}`, {method: 'POST', body: JSON.stringify(creature),
                headers: {'Content-Type': 'application/json'}})
                    .then(main().then(() => {}))
            });
            td.appendChild(donated_btn);
        }
        return td;
    }

    function render_bug(b) {
        let tr = document.createElement('tr');
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
        tr.appendChild(render_action_cell(b, 'bug'))
        return tr;
    }

    function active_marker(creature) {
        let now = new Date();
        if (!creature.months_active[now.getMonth()]) {
            console.error('error, month is not active for ', creature.name);
            return '◎';
        }
        if (!creature.hours_active[now.getHours()]) {
            console.error('error, hour is not active for ', creature.name, now.getHours(), creature.hours_active.slice(now.getHours() - 2, now.getHours() + 2));
            return '◎';
        }
        return '◉';
    }

    function status_as_text(caught, donated) {
        let ret = '❌';
        if (caught) {
            ret = '🎒';
        }
        if (donated) {
            ret += '🦉';
        }
        return ret;
    }
    function clear_dom_node(node) {
        while (node.hasChildNodes()) {
            node.removeChild(node.lastChild);
        }
    }
    function generate_image_src(name) {
        let base = name.replace(/[-\s]/g, '').toLowerCase();
        return `/images/${base}.png`;
    }
    function tick() {
        function time_eq(then, now) {
            return now.getFullYear() == then.getFullYear()
            && now.getHours() == then.getHours();
        }
        let new_now = new Date();
        if (!time_eq(now, new_now)) {
            now = new_now
            main().then(() => {
                setTimeout(tick, 1000 * 60);
            });
        } else {
            setTimeout(tick, 1000 * 60);
        }
    }
    tick()
})();