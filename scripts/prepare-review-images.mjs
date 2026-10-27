// Run after: npm install --no-save @imagemagick/magick-wasm@0.0.30
import {copyFile} from 'node:fs/promises';
const source=new URL('magick.wasm',import.meta.resolve('@imagemagick/magick-wasm'));
await copyFile(source,new URL('../supabase/functions/reviews/magick.wasm',import.meta.url));
console.log('Prepared pinned WASM asset for Supabase deployment.');
