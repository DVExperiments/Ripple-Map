/* Ripple Map deterministic educational engine. No libraries or network requests. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;root.RippleEngine=api;})(typeof window!=='undefined'?window:globalThis,function(){
 'use strict';
 const CATS=['infrastructure','technology','data','people','governance','ecology'];
 const DEFAULT_LENSES={infrastructure:true,technology:true,data:false,people:false,governance:false,ecology:false};
 const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
 function positionNodes(nodes,adjustments={}){
  const groups={infrastructure:[[168,166],[183,337],[171,515],[174,697],[312,806]],technology:[[415,149],[425,326],[412,515],[428,708],[525,808]],data:[[675,110],[686,247],[682,656],[687,801]],people:[[1190,151],[1180,323],[1193,495],[1185,675],[1195,814]],governance:[[927,126],[953,277],[953,438],[985,562]],ecology:[[928,662],[937,781],[1071,833]]};
  const counts={};return nodes.map(n=>{
   const idx=counts[n.category]||0;counts[n.category]=idx+1;
   let pos=n.category==='core'?[686,444]:((groups[n.category]||[[685,520]])[idx]||[245+(idx%5)*210,180+(Math.floor(idx/5))*120]);
   const offset=adjustments[n.id]; if(offset)pos=[offset.x,offset.y];
   return {...n,x:clamp(pos[0],90,1270),y:clamp(pos[1],60,824)};
  });
 }
 function impact(scenario,failedId,customNodes=[],customLinks=[]){
  const links=[...scenario.links,...customLinks];const queue=[failedId],depth={[failedId]:0},parent={},reasons={};
  while(queue.length){const current=queue.shift();for(const e of links){if(e.kind!=='requires'||e.source!==current||depth[e.target]!==undefined)continue;depth[e.target]=depth[current]+1;parent[e.target]=current;reasons[e.target]=e.why;queue.push(e.target);}}
  return {ids:Object.keys(depth),depth,parent,reasons,primary:Object.keys(depth).filter(id=>depth[id]===1),downstream:Object.keys(depth).filter(id=>depth[id]>1)};
 }
 function neighbourhood(scenario,id,customLinks=[]){const links=[...scenario.links,...customLinks];return {inbound:links.filter(l=>l.target===id),outbound:links.filter(l=>l.source===id)};}
 function pathToRoot(result,target){if(result.depth[target]===undefined)return [];const path=[target];while(result.parent[path[0]])path.unshift(result.parent[path[0]]);return path;}
 function progress(scenario,activity){let total=0;const detail=[];
  const observed=Object.values(activity.opened||{}).filter(Boolean).length;let n=Math.min(20,Math.round(observed/Math.min(10,scenario.nodes.length)*20));total+=n;detail.push({label:'Investigate system elements',points:n,max:20});
  const categories=Object.values(activity.lenses||{}).filter(Boolean).length;n=Math.round(categories/6*15);total+=n;detail.push({label:'Reveal different systems',points:n,max:15});
  n=activity.critical&&scenario.nodes.some(x=>x.id===activity.critical)?10:0;total+=n;detail.push({label:'Name a critical dependency',points:n,max:10});
  n=activity.justification&&activity.justification.trim().length>=35?15:activity.justification&&activity.justification.trim().length>=12?7:0;total+=n;detail.push({label:'Explain your reasoning',points:n,max:15});
  n=activity.incident?10:0;total+=n;detail.push({label:'Stress-test a failure',points:n,max:10});
  n=activity.intervention&&activity.intervention.trim().length>=30?10:activity.intervention&&activity.intervention.trim().length>=10?5:0;total+=n;detail.push({label:'Suggest a response and trade-off',points:n,max:10});
  const refl=activity.reflections||{};n=['boundary','people','unexpected','next'].reduce((s,k)=>s+(String(refl[k]||'').trim().length>=20?5:0),0);total+=n;detail.push({label:'Reflect on the wider system',points:n,max:20});
  return {score:total,detail};
 }
 function tidy(s){return String(s??'').trim().replace(/\s+/g,' ')};
 function validateCustomNode(label,cat){return tidy(label).length>=3&&tidy(label).length<=62&&CATS.includes(cat);}
 return {CATS,DEFAULT_LENSES,positionNodes,impact,neighbourhood,pathToRoot,progress,tidy,validateCustomNode};
});
