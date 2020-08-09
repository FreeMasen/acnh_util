import Dexie from 'https://unpkg.com/dexie@latest/dist/dexie.mjs';

let app;

const URL_PREFIX = (() => {
    if (location.hostname.includes('github.io')) {
        return '/acnh_util'
    }
    return '';
})()

window.addEventListener('DOMContentLoaded', async () => {
    let db = await Db.initialize();
    app = new App(db);
});


class App { 
    constructor(
        db,
    ) {
        this.selected_island = (() => {
            let id_str = localStorage.getItem('selected_island_id');
            if (!!id_str) {
                try {
                    return parseInt(id_str);
                } catch (e) {
                    console.error('invalid id', e)
                }
            }
        })();
        this.show_caught = (localStorage.getItem('show_caught') || 'true') === 'true';
        this.show_donated = (localStorage.getItem('show_donated') || 'true') === 'true';
        this.show_unavailable = (localStorage.getItem('show_unavailable') || 'true') === 'true';
        this.sort_orders = {
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
        };
        this.current_time = App.get_current_time();
        this.db = db;
        this.fish_table_header = document.querySelector('#fish-table thead');
        this.fish_table_body = document.querySelector('#fish-table tbody');
        this.bug_table_header = document.querySelector('#bug-table thead');
        this.bug_table_body = document.querySelector('#bug-table tbody');
        this.sea_creature_table_header = document.querySelector('#sea-creature-table thead');
        this.sea_creature_table_body = document.querySelector('#sea-creature-table tbody');
        this.global_caught_btn = document.getElementById('global-toggle-caught');
        this.global_donated_btn = document.getElementById('global-toggle-donated');
        this.global_unavailable_btn = document.getElementById('global-toggle-available');
        this.user_list = document.getElementById('user-list-wrapper');
        this.edit_users_form = new EditUsersForm(db, async () => {
            let users = await this.db.get_users();
            this.render_user_tabs(users);
        });
        this.start().then(() => {
            console.log('started!');
        }).catch(e => {
            console.error('error starting', e);
        });
    }

    updated_selected_user(id) {
        console.log('updating selected user to', id);
        this.selected_island = id;
        localStorage.setItem('selected_island', this.selected_island);
    }

    async start() {
        this.register_click_handlers();
        if (!this.selected_island) {
            const id = await this.db.get_default_user_id();
            this.updated_selected_user(id);
        }
        this.render_user_tabs();
        this.render_island_data();
        await this.timeTick();
    }

    async timeTick() {
        const current_time = App.get_current_time();
        if (current_time.hour != this.current_time.hour) {
            this.current_time = current_time;
            await this.render_island_data();
        }
        setTimeout(this.timeTick.bind(this), 60 * 1000);
    }

    register_click_handlers() {
        if (!!this.global_caught_btn) {
            this.global_caught_btn.addEventListener('click', async () => {
                this.show_caught = !this.show_caught;
                localStorage.setItem('show_caught', `${this.show_caught}`);
                this.handle_global_btn_classes(this.global_caught_btn, this.show_caught, 'Caught');
                this.render_island_data();
            });
            this.handle_global_btn_classes(this.global_caught_btn, this.show_caught, 'Caught');
        }
        if (!!this.global_donated_btn) {
            this.global_donated_btn.addEventListener('click', async () => {
                this.show_donated = !this.show_donated;
                localStorage.setItem('show_donated', `${this.show_donated}`);
                this.handle_global_btn_classes(this.global_donated_btn, this.show_donated, 'Donated');
                await this.render_island_data();
            });
            this.handle_global_btn_classes(this.global_donated_btn, this.show_donated, 'Donated');
        }
        if (!!this.global_unavailable_btn) {
            this.global_unavailable_btn.addEventListener('click', async() => {
                this.show_unavailable = !this.show_unavailable;
                localStorage.setItem('show_unavailable', `${this.show_unavailable}`);
                this.handle_global_btn_classes(this.global_unavailable_btn, this.show_unavailable, 'Unavailable');
                await this.render_island_data();
            });
            this.handle_global_btn_classes(this.global_unavailable_btn, this.show_unavailable, 'Unavailable');
        }
        if (!!this.fish_table_header) {
            this.handle_table_column_sorter(this.fish_table_header, this.sort_orders.fish);
        }
        if (!!this.bug_table_header) {
            this.handle_table_column_sorter(this.bug_table_header, this.sort_orders.bugs);
        }
        if (!!this.sea_creature_table_header) {
            this.handle_table_column_sorter(this.sea_creature_table_header, this.sort_orders.sea_creatures);
        }
    }

    handle_global_btn_classes(btn, flag, name) {
        if (flag) {
            btn.classList.add('is-error');
            btn.classList.remove('is-success');
            btn.innerText = `Hide ${name}`
        } else {
            btn.classList.add('is-success');
            btn.classList.remove('is-error');
            btn.innerText = `Show ${name}`;
        }
    }

    handle_table_column_sorter(row, sort_order) {
        let columns = row.querySelectorAll('th');
        for (let i = 0; i < columns.length; i++) {
            const column = columns[i];
            if (column.dataset.sort !== void 0) {
                column.addEventListener('click', async () => {
                    sort_order.key = column.dataset.sort;
                    sort_order.desc = !sort_order.desc;
                    await this.render_island_data()
                });
            }
        }
    }

    async render_user_tabs() {
        let users = await this.db.get_users();
        App.clear_table(this.user_list);
        for (const user of users) {
            this.user_list.appendChild(this.render_user_tab(user));
        }
        this.user_list.appendChild(this.render_edit_users_btn());
    }

    render_user_tab(user) {
        let btn = document.createElement('button');
        btn.dataset.islandId = user.id.toString();
        btn.classList.add('nes-btn');
        btn.classList.add('user-btn');
        if (user.id === this.selected_island) {
            btn.classList.add('is-success');
        } else {
            btn.classList.remove('is-success');
        }
        btn.innerText = user.name;
        btn.addEventListener('click',async ev => {
            let btn = ev.currentTarget;
            let container = btn.parentElement;
            if (!container) return;
            for (let i = 0; i < container.childElementCount; i++) {
                container.children[i].classList.remove('is-success');
            }
            btn.classList.add('is-success');
            if (user.id === this.selected_island) {
                return;
            }
            this.updated_selected_user(user.id);
            await this.render_island_data();
        });
        return btn;
    }

    render_edit_users_btn() {
        let btn = document.createElement('button');
        btn.classList.add('nes-btn');
        btn.innerText = '🖋';
        btn.addEventListener('click', () => {
            this.edit_users_form.show();
        });
        return btn;
    }

    async render_island_data() {
        let data;
        if (this.show_unavailable) {
            data = await this.db.get_all(this.selected_island || 0, this.show_caught,
                this.show_donated);
        } else {
            const {hour, month} = this.current_time = App.get_current_time();
            data = await this.db.get_all_for_time(
                this.selected_island || 0,
                hour,
                month,
                this.show_caught,
                this.show_donated
            );
        }
        this.render_tables(data);
    }

    render_tables({fish, bugs, sea_creatures}) {
        this.render_fish_table(fish);
        this.render_bugs_table(bugs);
        this.render_sea_creature_table(sea_creatures);
    }

    render_fish_table(fish) {
        this.order_collection(fish, this.sort_orders.fish.key, this.sort_orders.fish.desc);
        App.clear_table(this.fish_table_body);
        for (const f of fish) {
            this.fish_table_body.appendChild(this.render_fish_row(f));
        }
    }

    render_fish_row(f) {
        let tr = document.createElement('tr');
        tr.dataset.name = f.name;
        tr.dataset.location = f.location;
        tr.dataset.size = App.size_as_number(f.size.size).toString();
        tr.dataset.value = f.value.toString();
        tr.dataset.active = this.is_available(f).toString();
        tr.dataset.status = App.calculate_status(f.caught, f.donated).toString();
        let size_text = App.size_as_words(f.size.size);
        if (f.size.modifier) {
            size_text += ` ${f.size.modifier}`;
        }
        if (this.is_available(f)) {
            tr.classList.add('available');
        } else {
            tr.classList.add('unavailable');
            tr.title = `unavailable until ${this.next_available(f)}`;
        }
        tr.innerHTML = `
        <td class="cell-name">${f.name}</td>
        <td class="cell-image">
            <img src="${App.generate_image_src(f.name)}" class="thumbnail-image nes-avatar" />
        </td>
        <td class="cell-value">${f.value}</td>
        <td class="cell-location">${f.location}</td>
        <td class="cell-size">${size_text}</td>`;
        tr.appendChild(this.render_caught_cell(f, 'fish'));
        tr.appendChild(this.render_donated_cell(f, 'fish'));
        tr.appendChild(this.render_warning_cell(f));
        return tr;
    }

    render_bugs_table(bugs) {
        this.order_collection(bugs, this.sort_orders.bugs.key, this.sort_orders.bugs.desc);
        App.clear_table(this.bug_table_body);
        for (const bug of bugs) {
            this.bug_table_body.appendChild(this.render_bug_row(bug));
        }
    }

    render_bug_row(b) {
        let tr = document.createElement('tr');
        tr.dataset.name = b.name;
        tr.dataset.location = b.location;
        tr.dataset.value = b.value.toString();
        tr.dataset.active = this.is_available(b).toString();
        tr.dataset.status = App.calculate_status(b.caught, b.donated).toString();
        if (!this.is_available(b)) {
            tr.classList.add('unavailable');
            tr.title = `unavailable until ${this.next_available(b)}`;
        }
        tr.innerHTML = `
        <td class="cell-name">${b.name}</td>
        <td class="cell-image">
            <img src="${App.generate_image_src(b.name)}" class="thumbnail-image" />
        </td>
        <td class="cell-value">${b.value}</td>
        <td class="cell-location">${b.location}</td>
        `;
        tr.appendChild(this.render_caught_cell(b, 'bug'));
        tr.appendChild(this.render_donated_cell(b, 'bug'));
        tr.appendChild(this.render_warning_cell(b));
        return tr;
    }

    render_sea_creature_table(sea_creatures) {
        this.order_collection(sea_creatures, this.sort_orders.sea_creatures.key, this.sort_orders.sea_creatures.desc);
        App.clear_table(this.sea_creature_table_body);
        for (const creature of sea_creatures) {
            this.sea_creature_table_body.appendChild(this.render_sea_creature_row(creature));
        }
    }

    render_sea_creature_row(c) {
        let tr = document.createElement('tr');
        tr.dataset.name = c.name;
        tr.dataset.size = c.size;
        tr.dataset.value = `${c.value}`;
        tr.dataset.active = `${this.is_available(c)}`;
        tr.dataset.speed = c.speed;
        tr.dataset.status = `${App.calculate_status(c.caught, c.donated)}`;
        if (!this.is_available(c)) {
            tr.classList.add('unavailable');
            tr.title = `unavailable until ${this.next_available(c)}`;
        }
        tr.innerHTML = `
        <td class="cell-name">${c.name}</td>
        <td class="cell-image">
            <img src="${App.generate_image_src(c.name)}" class="thumbnail-image" />
        </td>
        <td class="cell-value">${c.value}</td>
        <td class="cell-speed">${App.speed_as_text(c.speed)}</td>
        <td class="cell-size">${App.size_as_words(c.size)}</td>`;
        tr.appendChild(this.render_caught_cell(c, 'sea_creature'));
        tr.appendChild(this.render_donated_cell(c, 'sea_creature'));
        tr.appendChild(this.render_warning_cell(c));
        return tr;
    }

    static size_as_number(size) {
        switch(size) {
            case 'Small': return 1;
            case 'Medium': return 2;
            case 'Large': return 3;
            case 'ExtraLarge': return 4;
            case 'Gargantuan': return 5;
            case 'Humongous': return 6;
            default: return 0;
        }
    }

    is_available(creature) {
        if (!creature.months_active[this.current_time.month]) {
            return false;
        }
        if (!creature.hours_active[this.current_time.hour]) {
            return false;
        }
        return true;
    }

    static calculate_status(...vals) {
        return vals.reduce((acc, v) => {
            if (v) {
                return acc + 1;
            }
            return acc;
        }, 0);
    }

    static generate_image_src(name) {
        let base = name.replace(/[-\s']/g, '').toLowerCase();
        return `${URL_PREFIX}/images/${base}.png`;
    }

    static speed_as_text(speed) {
        switch (speed) {
            case 'Stationary': return 'None';
            case 'VerySlow': return 'V. Slow';
            case 'Slow': return 'Slow';
            case 'Medium': return 'Medium';
            case 'Fast': return 'Fast';
            case 'VeryFast': return 'V. Fast';
        }
    }

    static speed_as_number(speed) {
        switch (speed) {
            case 'Stationary': return 1;
            case 'VerySlow': return 2;
            case 'Slow': return 3;
            case 'Medium': return 4;
            case 'Fast': return 5;
            case 'VeryFast': return 6;
            default: return 0
        }
    }

    static size_as_words(size) {
        switch(size) {
            case 'Small': return 'XS';
            case 'Medium': return 'S';
            case 'Large': return 'M';
            case 'ExtraLarge': return 'L';
            case 'Gargantuan': return 'XL';
            case 'Humongous': return 'XXL';
        }
    }

    static size_as_number(size) {
        if (!!size.size) {
            size = size.size;
        }
        switch(size) {
            case 'Small': return 1;
            case 'Medium': return 2;
            case 'Large': return 3;
            case 'ExtraLarge': return 4;
            case 'Gargantuan': return 5;
            case 'Humongous': return 6;
            default: return 0;
        }
    }

    static status_as_text(caught, donated, ty) {
        let ret = '';
        if (caught) {
            ret = `<span title="caught" />${App.caught_marker(ty)}</span>`;
        }
        if (donated) {
            ret += `🦉`;
        }
        return ret;
    }

    static caught_marker(ty) {
        switch (ty) {
            case 'fish': return '🎣';
            case 'bug': return '🥢';
            default: return '🤿';
        }
    }

    active_marker(creature) {
        let ret = '<label><input type="checkbox" class="nes-checkbox"';
        if (this.is_available(creature)) {
            ret += ' checked';
        }

        return ret + ' disabled /><span></span></label>';
    }

    render_caught_cell(creature, kind) {
        let td = App.render_checkbox_cell(creature.caught, 'cell-caught');
        td.querySelector('input').addEventListener('change', async () => {
            creature.caught = !creature.caught;
            await this.update_creature(kind, creature);
            await this.render_island_data();
        });
        return td;
    }
    render_donated_cell(creature, kind) {
        let td = App.render_checkbox_cell(creature.donated, 'cell-donated'); 
        td.querySelector('input').addEventListener('change', async () => {
            creature.donated = !creature.donated;
            await this.update_creature(kind, creature);
            await this.render_island_data();
        });
        return td;
    }

    static render_checkbox_cell(checked, cls) {
        let td = document.createElement('td');
        td.classList.add(cls);
        let label = document.createElement('label');
        td.appendChild(label);
        let input = document.createElement('input');
        input.type = 'checkbox';
        input.classList.add('nes-checkbox');
        if (checked) {
            input.setAttribute('checked', '');
        }
        label.appendChild(input);
        label.appendChild(document.createElement('span'));
        return td;
    }

    async update_creature(kind, creature) {
        switch (kind) {
            case 'fish': {
                await this.db.fish.update(creature.id, creature);
                break;
            }
            case 'bug': {
                console.log('creature', creature);
                await this.db.bugs.update(creature.id, creature);
                break;
            }
            case 'sea_creature': {
                await this.db.sea_creatures.update(creature.id, creature);
                break;
            }
        }
    }

    render_warning_cell(creature) {
        let td = document.createElement('td');
        td.classList.add('warning-cell');
        if (!this.is_available(creature)) {
            return td;
        }
        let hour = this.current_time.hour + 1;
        let month = this.current_time.month + 1;
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
        
        const clock_img = `⏰`;
        const cal_img = `🗓`;
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
        td.title = title;
        return td;
    }

    next_available(c) {
        if (c.months_active[this.current_time.month]) {
            for (let i = this.current_time.hour; i < c.hours_active.length; i++) {
                if (c.hours_active[i]) {
                    return `Today at ${App.hour_n_to_s(i)}`;
                }
            }
            for (let i = 0; i < this.current_time.hour; i++) {
                if (c.hours_active[i]) {
                    return `Tomorrow at ${App.hour_n_to_s(i)}`;
                }
            }
            return;
        }
        for (let i = this.current_time.month; i < c.months_active.length; i++) {
            if (c.months_active[i]) {
                return `The first of ${App.month_n_to_s(i)}`;
            }
        }
        for (let i = 0; i < this.current_time.month; i++) {
            if (c.months_active[i]) {
                return `The first of ${App.month_n_to_s(i)}`;
            }
        }
    }

    static hour_n_to_s(n) {
        if (n > 12) {
            return `${n - 12} PM`;
        }
        return `${n} AM`;
    }

    static month_n_to_s(n) {
        switch (n) {
            case 0: return 'January';
            case 1: return 'February';
            case 2: return 'March';
            case 3: return 'April';
            case 4: return 'May';
            case 5: return 'June';
            case 6: return 'July';
            case 7: return 'August';
            case 8: return 'September';
            case 9: return 'October';
            case 10: return 'November';
            default: return 'December';
        }
    }

    static clear_table(table) {
        while (!!table.lastChild) {
            table.removeChild(table.lastChild);
        }
    }

    order_collection(
        collection,
        key,
        desc
    ) {
        collection.sort((lhs, rhs) => {
            let lval, rval
            switch (key) {
                case 'active':
                    lval = +this.is_available(lhs);
                    rval = +this.is_available(rhs);
                    break;
                case 'speed':
                    lval = App.speed_as_number(lhs.speed);
                    rval = App.speed_as_number(rhs.speed);
                    break;
                case 'size':
                    lval = App.size_as_number(lhs.size);
                    rval = App.size_as_number(rhs.size);
                    break;
                case 'status':
                    lval = App.calculate_status(lhs.caught, lhs.donated);
                    rval = App.calculate_status(rhs.caught, rhs.donated);
                    break;
                default:
                    lval = lhs[key];
                    rval = rhs[key];
            } 
            const lty = typeof lval;
            const rty = typeof rval;
            if (lty !== rty) {
                return 0;
            }
            let l, r;
            if (desc) {
                l = lval;
                r = rval;
            } else {
                l = rval;
                r = lval;
            }
            switch (lty) {
                case 'string': return l.localeCompare(r);
                case 'number': return l  - r;
                default: return 0;
            }
        })
    }

    static get_current_time() {
        let now = new Date();
        return {
            hour: now.getHours(),
            month: now.getMonth(),
            timeout: now.getMinutes() * 60 * 1000,
        };
    }
}

class EditUsersForm {
    constructor(db, closed_cb) {
        this.db = db;
        this.el = document.getElementById('edit-users-list');
        this.list = null;
        document.getElementById('close-edit-users-btn').addEventListener('click', () => {
            this.hide();
            closed_cb();
        });
    }
    hide() {
        this.clear_list();
        this.el.classList.remove('show');
    }
    async show() {
        let users = await this.db.get_users();
        this.list = this.render_list(users);
        this.el.appendChild(this.list);
        this.el.classList.add('show');
    }

    render_list(users) {
        this.clear_list();
        let f = document.createElement('ul');
        for (const user of users) {
            f.appendChild(this.render_user_item(user))
        }
        f.appendChild(this.render_add_btn());
        return f;
    }
    clear_list() {
        if (this.list !== null && !!this.list.parentElement) {
            this.list.parentElement.removeChild(this.list);
        }
    }

    render_user_item(user) {
        let li = document.createElement('li');
        li.appendChild(this.render_user_name_input(user)); 
        li.appendChild(this.render_delete_button(user));
        return li;
    }

    render_user_name_input(user) {
        let el = document.createElement('input');
        el.type = 'text';
        el.value = user.name;
        el.addEventListener('change', async (ev) => {
            console.log('changed', ev);
            let input = ev.currentTarget;
            user.name = input.value;
            await this.db.islands.update(user.id, user);
        });
        return el;
    }

    render_delete_button(user) {
        let btn = document.createElement('button');
        btn.innerText = 'Delete';
        btn.classList.add('nes-btn', 'is-error');
        btn.addEventListener('click', async () => {
            if (confirm(`Are you sure you want to delete ${user.name} (${user.id})?`)) {
                await this.db.remove_user(user.id);
                await this.show();
            }
        });
        return btn;
    }

    render_add_btn() {
        let btn = document.createElement('button');
        btn.classList.add('nes-btn', 'add-user-btn');
        btn.innerText = 'Add User';
        btn.addEventListener('click', async () => {
            await this.db.setup_user('new user');
            this.show();
        });
        return btn;
    }
}

class Db extends Dexie {
    constructor(cb) {
        super("acnh_util");
        this.version(1).stores({
            islands: '++id, name',
            fish: '++id, table_id, island_id, name, value, location, size, months_active, hours_active, caught, donated',
            bugs: '++id, table_id, island_id, name, value, location, months_active, hours_active, caught, donated',
            sea_creatures: '++id, table_id, island_id, name, value, size, speed, months_active, hours_active, caught, donated',
        });
        this.islands = this.table('islands');
        this.fish = this.table('fish');
        this.bugs = this.table('bugs');
        this.sea_creatures = this.table('sea_creatures');
        
        this.islands.count().then(c => {
            console.log('island count: ', c);
            if (c < 1) {
                this.seed().then(() => {
                    cb(undefined, this)
                })
                .catch(cb)
            } else {
                cb(undefined, this);
            }
        }).catch(cb);
        window.__db = this;
    }

    static async initialize() {
        return new Promise((resolve, reject) => {
            new Db((e, db) => {
                if (e) return reject(e);
                return resolve(db);
            });
        })
    }

    async seed() {
        await this.setup_user('default');
    }

    async setup_user(island_name) {
        let island_id = await this.islands.add({name: island_name});
        const data = await (await fetch(`${URL_PREFIX}/initial_data.json`)).json();
        const island_info = {island_id, caught: false, donated: false};
        const mapper = (c, idx) => {
            let ret = Object.assign(c, island_info);
            if (ret.id !== void 0) {
                delete ret.id;
            }
            ret.table_id = idx;
            return ret;
        };
        const fish = data.fish.map(mapper);
        const bugs = data.bugs.map(mapper);
        const sea_creatures = data.sea_creatures.map(mapper);
        await this.fish.bulkAdd(fish).catch(e => {
            console.error('failed to add fish for ', island_name, island_id, fish);
            throw e;
        });
        await this.bugs.bulkAdd(bugs).catch(e => {
            console.error('failed to add bugs for ', island_name, island_id, bugs);
            throw e;
        });
        this.sea_creatures.bulkAdd(sea_creatures).catch(e => {
            console.error('failed to add sea creatures for ', island_name, island_id, sea_creatures);
            throw e;
        });
    }


    async remove_user(id) {
        await this.islands.delete(id);
        let fids = await this.fish.where('island_id').equals(id).primaryKeys();
        let bids = await this.bugs.where('island_id').equals(id).primaryKeys();
        let sids = await this.sea_creatures.where('island_id').equals(id).primaryKeys();
        await this.fish.bulkDelete(fids);
        await this.bugs.bulkDelete(bids);
        await this.sea_creatures.bulkDelete(sids);
    }

    async get_users() {
        return this.islands.toArray();
    }

    async get_default_user_id() {
        const user = await this.islands.toCollection().first();
        return user.id;
    }

    async get_user_id(name) {
        const island = await this.islands.filter(i => i.name === name).first();
        if (!island) throw new Error('no island named: ' + name);
        return island.id;
    }

    async get_all(island_id, show_caught, show_donated) {
        console.log('getting all for', island_id);
        let [fish, bugs, sea_creatures] = await Promise.all([
            this.fish.where('island_id').equals(island_id).filter(f => (show_caught || !f.caught) && (show_donated || !f.donated)).toArray(),
            this.bugs.where('island_id').equals(island_id).filter(f => (show_caught || !f.caught) && (show_donated || !f.donated)).toArray(),
            this.sea_creatures.where('island_id').equals(island_id).filter(f => (show_caught || !f.caught) && (show_donated || !f.donated)).toArray(),
        ]);
        return {
            fish,
            bugs,
            sea_creatures,
        };
    }

    async get_all_for_time(island_id, hour, month, include_caught, include_donated) {
        console.log('getting all for', island_id);
        let [fish, bugs, sea_creatures] = await Promise.all([
            this._get_all_for_time(this.fish, island_id, hour, month, include_caught, include_donated),
            this._get_all_for_time(this.bugs, island_id, hour, month, include_caught, include_donated),
            this._get_all_for_time(this.sea_creatures, island_id, hour, month, include_caught, include_donated),
        ]);
        return {
            fish,
            bugs,
            sea_creatures,
        };
    }

    async _get_all_for_time(
        table,
        island_id, hour, month, include_caught, include_donated
        ) {
        return table.filter(f => {
            return f.island_id == island_id
            && f.hours_active[hour] 
            && f.months_active[month]
            && (include_caught || !f.caught)
            && (include_donated || !f.donated)
        }).toArray();
    }

    async get_fish_by_name(name) {
        return this.fish.where('name').equals(name).first();
    }

    async catch_fish(id, caught) {
        if (caught === void 0) {
            caught = true;
        }
        this.catch_resource(this.fish, id, caught);
    }

    async catch_bug(id, caught) {
        if (caught === void 0) {
            caught = true;
        }
        this.catch_resource(this.bugs, id, caught);
    }
    
    async catch_sea_creature(id, caught) {
        if (caught === void 0) {
            caught = true;
        }
        this.catch_resource(this.sea_creatures, id, caught);
    }
    async donate_fish(id, donated) {
        if (donated === void 0) {
            donated = true;
        }
        this.donate_resource(this.fish, id, donated);
    }

    async donate_bug(id, donated) {
        if (donated === void 0) {
            donated = true;
        }
        this.donate_resource(this.bugs, id, donated);
    }

    async donate_sea_creature(id, donated) {
        if (donated === void 0) {
            donated = true;
        }
        this.donate_resource(this.sea_creatures, id, donated);
    }

    async catch_resource(table, id, caught) {
        let creature = await table.get(id);
        if (!creature) {
            throw new Error(`unable to find resource with id ${id}`);
        }
        creature.caught = caught;
        if (!caught) {
            creature.donated = false;
        }
        await table.update(creature.id, creature);
    }

    async donate_resource(table, id, donated) {
        let creature = await table.get(id);
        if (!creature) {
            throw new Error(`unable to find resource with island id ${id}`);
        }
        creature.donated = donated;
        await table.update(creature.id, creature);
    }

    
}