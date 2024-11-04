import '@testing-library/jest-dom';

import * as t from "./types";

type condition = () => boolean

global.SERVER_URL = "http://127.0.0.1:3000";
global.WAIT_TIMEOUT = 20000;

global.waitToMeet = async (page, fn: condition, ...args) => {
    const initTime: number = Date.now();
    while ((Date.now() - initTime) < global.WAIT_TIMEOUT) {
        if (await page.evaluate(fn, ...args)) return;
        await page.waitForTimeout(300);
    }

    let err = Error("Could not satisfy condition");
    throw err;
}

global.wait = {
    actionHandlerReady: async (page) => {
        await global.waitToMeet(page, () => (
            window.App.hasOwnProperty('URLContext') &&
            window.App.URLContext.hasOwnProperty('actionHandler') &&
            window.App.URLContext.actionHandler.ready));
    },
    parserReady: async (page) => {
        await global.wait.actionHandlerReady(page);
        await global.waitToMeet(page,
            () => window.App.URLContext.actionHandler.parser.ready);
    },
}

global.signIn = async (page) => {
    await global.wait.parserReady(page);
    await page.evaluate(() => window.App.onSignOutIn());
    await global.waitToMeet(page, (t): boolean => {
        let { URLContext } = window.App;
        let childContext: t.NavigationContext = Object.values(URLContext.children)[0];
        if (!URLContext.filled(childContext)) return false;
        if (!URLContext.filled(childContext.dataContext)) return false;
        if (!URLContext.filled(childContext.dataContext.mutableContext.data)) return false;
        return true;
    }, t);
    await page.evaluate((t) => {
        let context: t.NavigationContext = Object.values(window.App.URLContext.children)[0];
        Object.assign(context.dataContext.mutableContext.data, {
            username: 'robin', password: '1234'});
    }, t);
    await page.evaluate((t) => {
        (Object.values(window.App.URLContext.children)[0] as t.NavigationContext).dataContext.root.ok();
    }, t);
    await global.waitToMeet(page, (): boolean => {
        let {URLContext} = window.App;
        if (Object.values(URLContext.children).length) return false;
        if (!URLContext.filled(URLContext.APP.state.user_settings)) return false;
        if (!URLContext.filled(URLContext.APP.state.site_data)) return false;
        return URLContext.APP.state.user_settings.logged_in;
    });
    await global.wait.parserReady(page);
}

// page.on("console", message => console.log(message.text()));
