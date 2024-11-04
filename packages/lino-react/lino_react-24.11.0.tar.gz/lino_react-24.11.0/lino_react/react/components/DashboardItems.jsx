export const name = "DashboardItems";

import React from "react";
import PropTypes from "prop-types";
import { RegisterImportPool, Component } from "./Base";

import { DataProvider } from "./DataProvider";

let ex; const exModulePromises = ex = {
    prButton: import(/* webpackChunkName: "prButton_DashboardItems" */"primereact/button"),
    lm: import(/* webpackChunkName: "LoadingMask_DashboardItems" */"./LoadingMask"),
}
RegisterImportPool(ex);


export class DashboardItems extends Component {
    static requiredModules = ["prButton", "lm"];
    static iPool = ex;
    static propTypes = {
        // dashboard_items: PropTypes.number.
        user: PropTypes.string
    };
    static defaultProps = {
        P: 0
    };

    constructor() {
        super();
        this.state = {
            ...this.state,
            stamp: Date(),
            unloaded: true,
        };
        // this.method = this.method.bind(this);
        this.reloadData = this.reload;
        this.onDataGet = this.onDataGet.bind(this)
    }

    // method() {return this.props.}

    reload() {
        // this.setState({ // Set new stamp forcing reloading of each DP
        //     stamp:Date()
        // });
        Object.keys(window.App.rps).filter(k => k.includes("dashboard")).forEach(d => {
            window.App.rps[d].reload();
        })
    }

    onDataGet(d) {
        this.setState({
            unloaded: false
        })
    }

    renderDashboard(showReloadButton, rp) {
        return (data) => {
            if (data.version_mismatch && rp === "dashboard-0") {
                window.App.reload();
                return
            }
            if (data.html) {
                return <div>
                    {showReloadButton && <this.ex.prButton.Button icon={"pi pi-refresh"} style={{float:"right"}} onClick={() => {
                        let dp = window.App.rps[rp];
                        dp && dp.reload();
                    }
                    }/>}
                    <div dangerouslySetInnerHTML={{__html: data.html}}></div>
                </div>
            }
        }
    }

    render() {
        if (!this.state.ready) return null;
        const S = this.state;
        const P = this.props;
        let len = P.dashboard_items;
        if (len === undefined) {
            len = 0
        }
        // const Comp = "Table";
        // return loaded ? this.props.render(data, Comp) : <p>{placeholder}</p>;
        return <this.ex.lm.LoadingMask mask={S.unloaded} fillHeight={true} backgroundColor={""}>
            <DataProvider
                ref={(el) => {
                    window.App.setRpRef(el, `dashboard-main`)
                }}
                key={`${P.user}-${S.stamp}`}
                endpoint={"api/main_html"}
                useEverLoaded={true}
                hideLoading={true}
                post_data={this.onDataGet}
                render={this.renderDashboard(false, `dashboard-main`)}
            />
            {[...Array(len).keys()].map(i =>
                <DataProvider
                    key={`${P.user}-${i}-${S.stamp}`}
                    ref={(el) => {
                        window.App.setRpRef(el, `dashboard-${i}`)
                    }}
                    endpoint={`dashboard/${i}`}
                    post_data={this.onDataGet}
                    hideLoading={true}
                    render={this.renderDashboard(true, `dashboard-${i}`)}
                />)
            }
        </this.ex.lm.LoadingMask>
    }
}
