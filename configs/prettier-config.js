module.exports = {
  // Configuración básica
  semi: true,
  trailingComma: "es5",
  singleQuote: true,
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,

  // Configuración de brackets
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: "avoid",

  // Configuración de JSX
  jsxSingleQuote: true,
  jsxBracketSameLine: false,

  // Configuración de archivos
  endOfLine: "lf",
  insertPragma: false,
  requirePragma: false,
  proseWrap: "preserve",

  // Configuración de HTML
  htmlWhitespaceSensitivity: "css",

  // Configuración de Markdown
  markdownGfm: true,

  // Configuración de plugins
  plugins: [
    "@trivago/prettier-plugin-sort-imports",
    "prettier-plugin-organize-attributes",
  ],

  // Configuración de orden de imports
  importOrder: ["^react$", "^next/(.*)$", "^@/(.*)$", "^[./]"],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,

  // Configuración de atributos
  attributeGroups: ["^class$", "^id$", "^data-", "^aria-", "^on[A-Z]", "^$"],

  // Configuración específica por tipo de archivo
  overrides: [
    {
      files: "*.json",
      options: {
        printWidth: 120,
        tabWidth: 2,
      },
    },
    {
      files: "*.md",
      options: {
        printWidth: 100,
        proseWrap: "always",
      },
    },
    {
      files: "*.yml",
      options: {
        tabWidth: 2,
        singleQuote: false,
      },
    },
    {
      files: "*.yaml",
      options: {
        tabWidth: 2,
        singleQuote: false,
      },
    },
    {
      files: "*.html",
      options: {
        printWidth: 120,
        htmlWhitespaceSensitivity: "ignore",
      },
    },
    {
      files: "*.css",
      options: {
        singleQuote: false,
      },
    },
    {
      files: "*.scss",
      options: {
        singleQuote: false,
      },
    },
    {
      files: "*.less",
      options: {
        singleQuote: false,
      },
    },
  ],
};
