import { defineConfig } from '@rsbuild/core';

// Docs: https://rsbuild.rs/config/
export default defineConfig({
  output: {
    distPath: { root: 'docs' },
    assetPrefix: '/nuclear_data/',
  },
});
