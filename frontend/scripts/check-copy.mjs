import { readdirSync, readFileSync } from 'node:fs'
function scan(path){for(const e of readdirSync(path,{withFileTypes:true})){const p=path+'/'+e.name;if(e.isDirectory())scan(p);else if(/\.(tsx?|html)$/.test(p)&&readFileSync(p,'utf8').includes('\u2014'))throw new Error('Forbidden em dash: '+p)}}
scan('src'); console.log('UI copy check passed')
