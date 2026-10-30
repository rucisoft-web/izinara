/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class PermitDashboard extends Component {
    static template = "izinara.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ data: null });
        onWillStart(() => this.load());
    }

    async load() {
        this.state.data = await this.orm.call("izinara.dashboard", "get_dashboard_data", []);
    }

    open(resModel, name, domain, views = [[false, "list"], [false, "form"]], context = {}) {
        this.action.doAction({ type: "ir.actions.act_window", name, res_model: resModel, domain, views, context });
    }

    openRecord(resModel, id) {
        this.action.doAction({ type: "ir.actions.act_window", res_model: resModel, res_id: id, views: [[false, "form"]] });
    }

    openKpi(key) {
        const today = luxon.DateTime.now().toISODate();
        const map = {
            shipments: ["izinara.shipment", "Pengapalan berjalan", [["state", "in", ["draft", "permits", "ready"]]]],
            apps_open: ["izinara.application", "Pengurusan berjalan", [["state", "in", ["draft", "progress", "submitted"]]]],
            apps_late: ["izinara.application", "Pengurusan terlambat", [["overdue", "=", true]]],
            steps_open: ["izinara.application.step", "Aktivitas belum selesai",
                [["done", "=", false], ["app_state", "in", ["progress", "submitted"]]]],
            steps_late: ["izinara.application.step", "Aktivitas terlambat",
                [["done", "=", false], ["app_state", "in", ["progress", "submitted"]], ["date_planned", "<", today]]],
            docs_review: ["izinara.document", "Dokumen menunggu verifikasi", [["state", "=", "review"]]],
            docs_rejected: ["izinara.document", "Dokumen ditolak", [["state", "=", "rejected"]]],
            memos_open: ["izinara.memo", "Memo menunggu jawaban", [["state", "=", "open"]]],
            memos_late: ["izinara.memo", "Memo lewat tenggat", [["overdue", "=", true]]],
            licenses_expiring: ["izinara.license", "Izin segera habis/kedaluwarsa",
                [["state", "in", ["valid", "expiring", "expired"]], ["date_expiry", "<=", luxon.DateTime.now().plus({ days: 90 }).toISODate()]]],
        };
        const [model, name, domain] = map[key];
        this.open(model, name, domain);
    }

    openParty(party, what) {
        const today = luxon.DateTime.now().toISODate();
        if (what === "late") {
            this.open("izinara.application.step", `Terlambat – ${party.name}`,
                [["party_id", "=", party.id], ["done", "=", false], ["app_state", "in", ["progress", "submitted"]], ["date_planned", "<", today]]);
        } else if (what === "open") {
            this.open("izinara.application.step", `Tugas – ${party.name}`,
                [["party_id", "=", party.id], ["done", "=", false], ["app_state", "in", ["progress", "submitted"]]]);
        } else if (what === "docs") {
            this.open("izinara.document", `Verifikasi – ${party.name}`,
                [["verifier_party_id", "=", party.id], ["state", "=", "review"]]);
        } else if (what === "memos") {
            this.open("izinara.memo", `Memo masuk – ${party.name}`,
                [["to_party_id", "=", party.id], ["state", "=", "open"]]);
        }
    }

    openType(type, state) {
        const domain = [["type_id", "=", type.id]];
        if (state) {
            domain.push(["state", "=", state]);
        }
        this.open("izinara.application", type.name, domain);
    }

    openGroup(group) {
        this.open("izinara.application", group.name, [["food_group", "=", group.code]],
            [[false, "list"], [false, "form"]]);
    }

    pct(type, state) {
        return type.total ? (100 * type[state]) / type.total : 0;
    }
}

registry.category("actions").add("izinara.dashboard", PermitDashboard);
