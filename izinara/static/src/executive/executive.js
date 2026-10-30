/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const DOC_COLORS = { missing: "#ced4da", review: "#d39e00", verified: "#2e7d4f", rejected: "#c0392b" };
const LICENSE_COLORS = { valid: "#2e7d4f", expiring: "#d39e00", expired: "#c0392b", revoked: "#6c757d" };

export class IzinaraExecutive extends Component {
    static template = "izinara.Executive";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ data: null });
        this.today = luxon.DateTime.now().toFormat("dd LLL yyyy");
        onWillStart(async () => {
            this.state.data = await this.orm.call("izinara.dashboard", "get_executive_data", []);
        });
    }

    get ex() {
        return this.state.data.executive;
    }

    pct(part, total) {
        return total ? Math.round((100 * part) / total) : 0;
    }

    /** Segmen donut SVG: lingkaran keliling 100 sehingga dasharray = persen. */
    donut(rows, colors) {
        const total = rows.reduce((sum, r) => sum + r.count, 0);
        let offset = 25;
        return rows.filter((r) => r.count).map((r) => {
            const value = total ? (100 * r.count) / total : 0;
            const seg = { ...r, color: colors[r.state], dash: `${value} ${100 - value}`, offset, pct: Math.round(value) };
            offset -= value;
            return seg;
        });
    }

    get docSegments() {
        return this.donut(this.ex.docs, DOC_COLORS);
    }

    get licenseSegments() {
        return this.donut(this.ex.licenses, LICENSE_COLORS);
    }

    get verifiedCount() {
        const row = this.ex.docs.find((r) => r.state === "verified");
        return row ? row.count : 0;
    }

    get licenseTotal() {
        return this.ex.licenses.reduce((sum, r) => sum + r.count, 0);
    }

    get maxItems() {
        return Math.max(1, ...this.state.data.groups.map((g) => g.items));
    }

    get maxOpen() {
        return Math.max(1, ...this.state.data.parties.map((p) => p.open + p.done));
    }

    openDashboard() {
        this.action.doAction("izinara.action_permit_dashboard");
    }

    openGuide() {
        this.action.doAction("izinara.action_izinara_guide");
    }
}

registry.category("actions").add("izinara.executive", IzinaraExecutive);
