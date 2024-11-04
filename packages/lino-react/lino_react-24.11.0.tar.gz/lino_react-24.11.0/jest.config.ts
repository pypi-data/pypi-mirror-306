import type { Config } from 'jest';

const config: Config = {
    moduleFileExtensions: ["js", "jsx", "ts", "tsx"],
    moduleNameMapper: {
        '^.+\\.(css|less)$': '<rootDir>/CSSStub.js'
    },
    preset: 'jest-puppeteer',
    // testRegex: "(/__tests__/.*|(\\.|/)(test|spec))\\.(jsx?|tsx?|js?|ts?)$",
    roots: ["<rootDir>/lino_react/react/components"],
    setupFilesAfterEnv: ["<rootDir>/lino_react/react/components/setupTests.ts"],
    testTimeout: 300000,
    transform: {
        '^.+\\.(ts|tsx)?$': 'ts-jest',
        '^.+\\.(js|jsx)$': 'babel-jest',
    },
    transformIgnorePatterns: [
        "node_modules/(?!(query-string|decode-uri-component|split-on-first|filter-obj)/)"
    ],
    verbose: true,
}

export default config;
