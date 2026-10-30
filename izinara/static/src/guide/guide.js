/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const TABS = [
    ["summary", "Ringkasan fungsi"],
    ["purchasing", "Purchasing"],
    ["pangan", "Makanan Luar (BPOM)"],
    ["halal", "Sertifikasi Halal"],
    ["perizinan", "Perizinan"],
    ["impor", "Impor & Kepabeanan"],
    ["manager", "Manajer"],
];

export class IzinaraGuide extends Component {
    static template = "izinara.Guide";
    static props = ["*"];

    setup() {
        this.action = useService("action");
        this.tabs = TABS;
        this.state = useState({ tab: "summary" });
    }

    open(xmlid) {
        this.action.doAction(xmlid);
    }
}

registry.category("actions").add("izinara.guide", IzinaraGuide);
