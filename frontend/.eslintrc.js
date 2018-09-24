module.exports = {
  env: {
    es6: true,
    browser: true,
    jest: true,
  },

  globals: {
    fetch: true,
    FormData: true,
  },

  parser: 'babel-eslint',

  parserOptions: {
    ecmaVersion: 6,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
      generators: true,
      experimentalObjectRestSpread: true,
    },
  },

  extends: [
    'airbnb',
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:import/recommended',
    'plugin:flowtype/recommended',
    'prettier',
    'prettier/flowtype',
    'prettier/react',
  ],

  plugins: ['react', 'import', 'flowtype', 'babel', 'prettier'],

  settings: {
    'import/ignore': ['node_modules'],
    'import/extensions': ['.js'],
  },

  rules: {
    strict: 'off',

    'import/no-named-as-default': 'off',

    'import/no-unresolved': 'error',

    // Error if style doesn't match the prettier style
    'prettier/prettier': 'error',

    // Only warn on console use
    'no-console': 'warn',

    // Only warn if there are any unused variables
    'no-unused-vars': 'warn',

    // Don't error on empty code blocks
    'no-empty': 'off',

    // Don't require jsx extension
    'react/jsx-filename-extension': 'off',

    // Don't enforce destructuring props
    'react/destructuring-assignment': 'off',

    // Don't require that react components need PropType definitions
    'react/prop-types': 'off',

    // Only warn about deprecated string refs
    'react/no-string-refs': 'error',

    'react/display-name': 'off',

    // Ignore unescaped entities
    'react/no-unescaped-entities': 'off',

    'react/sort-comp': [
      2,
      {
        order: [
          'type-annotations',
          'static-methods',
          'lifecycle',
          'everything-else',
          'render',
        ],
      },
    ],
  },
};
