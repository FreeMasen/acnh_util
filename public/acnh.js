
(function () {
    const ELEMENTS = Object.freeze({
        FISH_BODY: document.querySelector('#fish-table tbody'),
        BUGS_BODY: document.querySelector('#bug-table tbody'),
        FISH_ROW_TEMPLATE: document.querySelector('#fish-row-template'),
        BUGS_ROW_TEMPLATE: document.querySelector('#bug-row-template'),

    });
    Promise.all([
        fetch('/fish'),
        fetch('/bugs'),
    ]).then(([fish, bugs]) => {
        return Promise.all([
            fish.json(),
            bugs.json(),
        ]);
    }).then(([fish, bugs]) => {
        render_fish(fish.Fish);
        render_bugs(bugs.Bugs);
    });
    
    function render_fish(fish) {
        clear_dom_node(ELEMENTS.FISH_BODY);
        for (let f of fish) {
            const template = document.getElementById('fish-row-template').cloneNode(true);
            const node = template.querySelector('tr');
            node.querySelector('.cell-name').innerText = f.name
            node.querySelector('.cell-location').innerText = f.location;
            node.querySelector('.cell-size').innerText = f.size.size;
            node.querySelector('.cell-value').innerText = f.value.toString();
            node.querySelector('.cell-active').innerText = f.months_active[new Date().getMonth()] ? '◉' : '◎';
            node.querySelector('.cell-status').innerText = status_as_text(f.caught, f.donated);
            ELEMENTS.FISH_BODY.appendChild(node);
        }
    }

    function render_bugs(bugs) {
        clear_dom_node(ELEMENTS.BUGS_BODY);
        for (let f of fish) {
            let node = document.getElementById('bug-row-template').cloneNode(true).querySelector('tr');
            node.querySelector('.cell-name').innerText = f.name
            node.querySelector('.cell-location').innerText = f.location;
            node.querySelector('.cell-value').innerText = f.value.toString();
            node.querySelector('.cell-active').innerText = f.months_active[new Date().getMonth()] ? '◉' : '◎';
            node.querySelector('.cell-status').innerText = status_as_text(f.caught, f.donated);
            ELEMENTS.BUGS_BODY.appendChild(node);
        }
    }

    function status_as_text(caught, donated) {
        let ret = '';
        if (caught) {
            ret += '🎒';
        }
        if (donated) {
            ret += '🎒🦉';
        }
        return ret;
    }
    function clear_dom_node(node) {
        while (node.hasChildNodes()) {
            node.removeChild(node.lastChild);
        }
    }
})();