import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  site: 'https://freereliableappliancepickup.com',
  trailingSlash: 'always',
  output: 'server',
  adapter: cloudflare()
});
