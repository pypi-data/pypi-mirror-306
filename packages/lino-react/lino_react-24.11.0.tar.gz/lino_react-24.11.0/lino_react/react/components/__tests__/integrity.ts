import puppeteer from "puppeteer";

import * as t from '../types';

describe("cloneUI.ts", () => {
    let browser, page;

    beforeAll(async () => {
        browser = await puppeteer.launch({headless: true});
        page = await browser.newPage();
    });

    it("load landing page", async () => {
        await page.goto(global.SERVER_URL);
    });

    it("sign in ok", async () => {
        await page.goto(global.SERVER_URL);
        await global.signIn(page);
        const logged_in = await page.evaluate(() => {
            return window.App.state.user_settings.logged_in;
        });
        expect(logged_in).toBe(true);
    });

    afterAll(() => browser.close());
});
