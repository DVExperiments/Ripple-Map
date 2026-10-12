const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');
const E=require('../assets/engine.js');const data=JSON.parse(fs.readFileSync(path.join(__dirname,'../assets/content.json'),'utf8'));
assert.equal(data.scenarios.length,7);let nodeCount=0,edgeCount=0;
for(const s of data.scenarios){const ids=new Set(s.nodes.map(n=>n.id));assert.equal(ids.size,s.nodes.length);nodeCount+=s.nodes.length;edgeCount+=s.links.length;
 for(const l of s.links){assert(ids.has(l.source)&&ids.has(l.target));assert(['requires','influences','affects'].includes(l.kind));}
 for(const i of s.incidents){const result=E.impact(s,i.node);assert(result.ids.includes(i.node));assert.equal(result.depth[i.node],0);for(const x of result.ids)assert(ids.has(x));if(result.ids.length>1){const a=E.pathToRoot(result,result.ids.at(-1));assert.equal(a[0],i.node);}}
 const placed=E.positionNodes(s.nodes);assert.equal(placed.length,s.nodes.length);for(const n of placed){assert(n.x>0&&n.y>0)}
 const act={opened:{},lenses:{...E.DEFAULT_LENSES},critical:'',justification:'',incident:'',intervention:'',reflections:{}};
 assert(E.progress(s,act).score>=0);act.opened=Object.fromEntries(s.nodes.map(n=>[n.id,true]));act.lenses=Object.fromEntries(Object.keys(data.categories).map(c=>[c,true]));act.critical=s.nodes[1].id;act.justification='Important because this creates a dependency between systems.';act.incident=s.incidents[0].node;act.intervention='Try an alternative, but this may create costs and another dependency.';act.reflections=Object.fromEntries(['boundary','people','unexpected','next'].map(k=>[k,'Here is a substantial considered answer.']));assert.equal(E.progress(s,act).score,100);
}
assert(E.validateCustomNode('Water governance','governance'));assert(!E.validateCustomNode('x','governance'));assert.equal(E.impact({links:[{source:'a',target:'b',kind:'requires'},{source:'b',target:'c',kind:'requires'}]},'a').depth.c,2);
console.log(`PASS: ${data.scenarios.length} scenarios, ${nodeCount} elements, ${edgeCount} connections, ${data.scenarios.reduce((s,x)=>s+x.incidents.length,0)} stress tests, 100-point rubric`);
