/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class IzinaraPermitGuide extends Component {
    static template = "izinara.PermitGuide";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ data: null, selected: null, search: "" });
        onWillStart(async () => {
            this.state.data = await this.orm.call("izinara.dashboard", "get_permit_guide_data", []);
            this.state.selected = this.state.data.types.length ? this.state.data.types[0].id : null;
        });
    }

    get current() {
        return this.state.data.types.find((t) => t.id === this.state.selected);
    }

    typesOf(scope) {
        const q = this.state.search.trim().toLowerCase();
        return this.state.data.types.filter((t) => t.scope === scope &&
            (!q || t.name.toLowerCase().includes(q) || t.code.toLowerCase().includes(q) ||
             t.authority.toLowerCase().includes(q)));
    }

    /** Keterangan dipecah per paragraf; baris "Kapan diperlukan: ..." ditampilkan sebagai butir berjudul. */
    get paragraphs() {
        return this.current.description.split(/\n+/).filter((p) => p.trim()).map((p) => {
            const m = p.match(/^(Kapan diperlukan|Hasil|Perhatian):\s*(.*)$/);
            return m ? { label: m[1], text: m[2] } : { label: "", text: p };
        });
    }

    get totalDays() {
        return this.current.steps.reduce((sum, s) => sum + s.days, 0);
    }

    select(id) {
        this.state.selected = id;
        const body = document.querySelector(".o_izinara_pg_detail");
        if (body) {
            body.scrollTop = 0;
        }
    }

    openType() {
        this.action.doAction({ type: "ir.actions.act_window", res_model: "izinara.type",
            res_id: this.state.selected, views: [[false, "form"]] });
    }
}

registry.category("actions").add("izinara.permit_guide", IzinaraPermitGuide);
