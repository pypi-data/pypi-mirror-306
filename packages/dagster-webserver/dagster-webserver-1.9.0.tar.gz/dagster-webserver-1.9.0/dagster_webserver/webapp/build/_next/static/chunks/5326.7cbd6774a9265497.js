"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[5326],{65326:function(e,t,o){o.r(t),o.d(t,{FallthroughRoot:function(){return g}});var n=o(52322),r=o(14934),i=o(79106),s=o(39013),l=o(2784),p=o(7267),a=o(17872),c=o(44900),u=o(17867),h=o(10539);let x=e=>e.repository.pipelines.filter(e=>!(0,c.pv)(e.name)),f=()=>{let{allRepos:e,loading:t,locationEntries:o}=(0,l.useContext)(u.C5);if(t)return(0,n.jsx)(r.x,{flex:{direction:"row",justifyContent:"center"},style:{paddingTop:"100px"},children:(0,n.jsxs)(r.x,{flex:{direction:"row",alignItems:"center",gap:16},children:[(0,n.jsx)(i.$,{purpose:"section"}),(0,n.jsx)("div",{style:{color:s.$()},children:"Loading definitions…"})]})});if(o.length&&0===e.length)return(0,n.jsx)(p.l_,{to:"/locations"});let a=e.filter(e=>x(e).length>0);if(0===a.length){let t=e.find(e=>e.repository.assetGroups.length);if(t)return(0,n.jsx)(p.l_,{to:(0,h.rO)(t.repository.name,t.repositoryLocation.name,"/asset-groups/".concat(t.repository.assetGroups[0].groupName))})}if(1===a.length){let e=a[0],t=x(e);if(1===t.length){let o=t[0];return(0,n.jsx)(p.l_,{to:(0,h.jT)({repoName:e.repository.name,repoLocation:e.repositoryLocation.name,pipelineName:o.name,isJob:o.isJob})})}}return a.length>0?(0,n.jsx)(p.l_,{to:"/overview"}):(0,n.jsx)(p.l_,{to:"/locations"})},g=()=>(0,n.jsx)(p.rs,{children:(0,n.jsx)(a.A,{path:"*",isNestingRoute:!0,children:(0,n.jsx)(f,{})})})}}]);
//# sourceMappingURL=5326.7cbd6774a9265497.js.map