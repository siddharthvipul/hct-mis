// ***********************************************************
// This plugins/index.js can be used to load plugins
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)

// https://gist.github.com/csuzw/845b589549b61d3a5fe18e49592e166f

const cucumber = require('cypress-cucumber-preprocessor').default;
const browserify = require('@cypress/browserify-preprocessor');

module.exports = (on) => {
  const options = browserify.defaultOptions;

  options.browserifyOptions.plugin.unshift([
    'tsify',
    { project: 'cypress/tsconfig.json' },
  ]);

  on('file:preprocessor', cucumber(options));
};
