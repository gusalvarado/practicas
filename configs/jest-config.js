module.exports = {
  // Configuración básica
  testEnvironment: "node",
  roots: ["<rootDir>/src", "<rootDir>/tests"],
  testMatch: [
    "**/__tests__/**/*.+(ts|tsx|js)",
    "**/*.(test|spec).+(ts|tsx|js)",
  ],
  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest",
  },
  collectCoverageFrom: [
    "src/**/*.{js,ts}",
    "!src/**/*.d.ts",
    "!src/**/*.test.{js,ts}",
    "!src/**/*.spec.{js,ts}",
    "!src/**/index.{js,ts}",
    "!src/**/types/**",
    "!src/**/constants/**",
  ],

  // Configuración de cobertura
  coverageDirectory: "coverage",
  coverageReporters: [
    "text",
    "text-summary",
    "html",
    "lcov",
    "json",
    "json-summary",
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  // Configuración de setup
  setupFilesAfterEnv: ["<rootDir>/tests/setup.ts"],
  testTimeout: 10000,
  clearMocks: true,
  restoreMocks: true,

  // Configuración de módulos
  moduleNameMapping: {
    "^@/(.*)$": "<rootDir>/src/$1",
    "^@tests/(.*)$": "<rootDir>/tests/$1",
    "^@config/(.*)$": "<rootDir>/config/$1",
  },

  // Configuración de transformación
  transformIgnorePatterns: [
    "node_modules/(?!(module-that-needs-to-be-transformed)/)",
  ],

  // Configuración de globals
  globals: {
    "ts-jest": {
      tsconfig: "tsconfig.json",
      isolatedModules: true,
    },
  },

  // Configuración de reporters
  reporters: [
    "default",
    [
      "jest-junit",
      {
        outputDirectory: "coverage",
        outputName: "junit.xml",
        classNameTemplate: "{classname}",
        titleTemplate: "{title}",
        ancestorSeparator: " › ",
        usePathForSuiteName: true,
      },
    ],
    [
      "jest-html-reporters",
      {
        publicPath: "./coverage/html-report",
        filename: "report.html",
        expand: true,
        hideIcon: false,
        pageTitle: "Test Report",
        logoImgPath: undefined,
        darkTheme: false,
      },
    ],
  ],

  // Configuración de watch
  watchPlugins: [
    "jest-watch-typeahead/filename",
    "jest-watch-typeahead/testname",
  ],

  // Configuración de verbose
  verbose: true,

  // Configuración de bail
  bail: false,

  // Configuración de maxWorkers
  maxWorkers: "50%",

  // Configuración de cache
  cache: true,
  cacheDirectory: "<rootDir>/.jest-cache",

  // Configuración de errorOnDeprecated
  errorOnDeprecated: true,

  // Configuración de forceExit
  forceExit: false,

  // Configuración de detectLeaks
  detectLeaks: true,
  detectOpenHandles: true,

  // Configuración de projects (para monorepos)
  projects: [
    {
      displayName: "unit",
      testMatch: ["<rootDir>/src/**/*.test.{js,ts}"],
      testEnvironment: "node",
    },
    {
      displayName: "integration",
      testMatch: ["<rootDir>/tests/integration/**/*.test.{js,ts}"],
      testEnvironment: "node",
    },
    {
      displayName: "e2e",
      testMatch: ["<rootDir>/tests/e2e/**/*.test.{js,ts}"],
      testEnvironment: "node",
    },
  ],

  // Configuración de collectCoverage
  collectCoverage: false,

  // Configuración de coveragePathIgnorePatterns
  coveragePathIgnorePatterns: [
    "/node_modules/",
    "/coverage/",
    "/dist/",
    "/build/",
    "/.next/",
    "/.nuxt/",
    "/.vuepress/",
    "/.serverless/",
    "/.fusebox/",
    "/.dynamodb/",
    "/.tern-port/",
  ],

  // Configuración de testPathIgnorePatterns
  testPathIgnorePatterns: [
    "/node_modules/",
    "/coverage/",
    "/dist/",
    "/build/",
    "/.next/",
    "/.nuxt/",
    "/.vuepress/",
    "/.serverless/",
    "/.fusebox/",
    "/.dynamodb/",
    "/.tern-port/",
  ],

  // Configuración de moduleFileExtensions
  moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json", "node"],

  // Configuración de resolver
  resolver: undefined,

  // Configuración de testEnvironmentOptions
  testEnvironmentOptions: {
    url: "http://localhost",
  },

  // Configuración de snapshotSerializers
  snapshotSerializers: [],

  // Configuración de testResultsProcessor
  testResultsProcessor: undefined,

  // Configuración de unmockedModulePathPatterns
  unmockedModulePathPatterns: ["node_modules/react/", "node_modules/enzyme/"],
};
