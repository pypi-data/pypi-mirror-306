"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[1914],{99478:function(e,n,r){r.d(n,{CY:function(){return P},N9:function(){return S}});var t=r(73235),o=r(52322),l=r(2784),s=r(7267),i=r(67126),a=r(59920),d=r(24207),p=r(36381),c=r(20958),u=r(78491),h=r(69737),x=r(53448),g=r(44900),m=r(75442),j=r(20171),f=r(39593),v=r(59923),y=r(92199);function b(){let e=(0,t._)(["\n  query PipelineExplorerRootQuery(\n    $snapshotPipelineSelector: PipelineSelector\n    $snapshotId: String\n    $rootHandleID: String!\n    $requestScopeHandleID: String\n  ) {\n    pipelineSnapshotOrError(\n      snapshotId: $snapshotId\n      activePipelineSelector: $snapshotPipelineSelector\n    ) {\n      ... on PipelineSnapshot {\n        id\n        name\n        metadataEntries {\n          ...MetadataEntryFragment\n        }\n        solidHandle(handleID: $rootHandleID) {\n          ...GraphExplorerSolidHandleFragment\n        }\n        solidHandles(parentHandleID: $requestScopeHandleID) {\n          handleID\n          solid {\n            name\n            definition {\n              assetNodes {\n                id\n                ...GraphExplorerAssetNodeFragment\n              }\n            }\n          }\n          ...GraphExplorerSolidHandleFragment\n        }\n        ...GraphExplorerFragment\n      }\n      ... on PipelineNotFoundError {\n        message\n      }\n      ... on PipelineSnapshotNotFoundError {\n        message\n      }\n      ...PythonErrorFragment\n    }\n  }\n\n  ","\n  ","\n  ","\n  ","\n  ","\n"]);return b=function(){return e},e}let P=()=>{(0,h.Px)();let e=(0,s.UO)(),n=(0,p.p3)(e["0"]),{pipelineName:r,snapshotId:t}=n,l=(0,s.k6)();return(0,j.j)("Snapshot: ".concat(r).concat(t?"@".concat(t.slice(0,8)):"")),(0,o.jsx)(S,{explorerPath:n,onChangeExplorerPath:(e,n)=>{l[n]("/snapshots/".concat((0,p.gY)(e)))},onNavigateToSourceAssetNode:(e,n)=>{let{assetKey:r}=n,t=(0,m.p)(r);e.metaKey?window.open(t,"_blank"):l.push((0,m.p)(r))}})},S=e=>{var n;let{explorerPath:r,repoAddress:t,onChangeExplorerPath:s,onNavigateToSourceAssetNode:p,isGraph:u=!1}=e,[h,m]=(0,l.useState)({explodeComposites:null!==(n=r.explodeComposites)&&void 0!==n&&n,preferAssetRendering:!0}),j=r.opNames.slice(0,r.opNames.length-1),f=(0,y._T)(t||null,r.pipelineName),b=(0,c.aM)(E,{variables:{snapshotPipelineSelector:r.snapshotId?void 0:f,snapshotId:r.snapshotId?r.snapshotId:void 0,rootHandleID:j.join("."),requestScopeHandleID:h.explodeComposites?void 0:j.join(".")}});return(0,o.jsx)(v.g,{queryResult:b,children:e=>{let{pipelineSnapshotOrError:n}=e;if("PipelineSnapshot"!==n.__typename)return(0,o.jsx)(d.Q,{isGraph:u,result:n,repoAddress:t});let l=n.solidHandle,c=h.explodeComposites?(0,i.i)(n.solidHandles):n.solidHandles,j=n.solidHandles.some(e=>e.solid.definition.assetNodes.length>0);return h.preferAssetRendering&&j?(0,o.jsx)(x.OK,{options:h,setOptions:m,fetchOptions:{pipelineSelector:f},explorerPath:r,onChangeExplorerPath:s,onNavigateToSourceAssetNode:p,viewType:g._4.JOB}):(0,o.jsx)(a.m0,{options:h,setOptions:m,explorerPath:r,onChangeExplorerPath:s,container:n,repoAddress:t,handles:c,parentHandle:l||void 0,isGraph:u,getInvocations:e=>c.filter(n=>n.solid.definition.name===e).map(e=>({handleID:e.handleID}))})}})},E=(0,c.Ps)(b(),f.i,a.Sm,a.Q,a.bg,u.B)},29664:function(e,n,r){r.d(n,{G:function(){return G}});var t=r(73235),o=r(52322),l=r(49853),s=r(49308),i=r(14934),a=r(37483),d=r(43212),p=r(89891),c=r(80122),u=r(2784),h=r(7267),x=r(36381),g=r(55255),m=r(88610),j=r(92199),f=r(10539);let v=e=>{let{repoAddress:n,anyFilter:r,jobName:t,jobPath:l}=e,s=(0,j.Ux)(n),d=(0,j.Hb)(s,t);return(0,o.jsx)(i.x,{padding:{vertical:64},children:(0,o.jsx)(a.t,{icon:"run",title:"No runs found",description:n?d?(0,o.jsxs)(i.x,{flex:{direction:"column",gap:12},children:[(0,o.jsx)("div",{children:r?"There are no matching runs for these filters.":"You have not materialized any assets with this job yet."}),(0,o.jsx)("div",{children:(0,o.jsx)(m.A,{icon:(0,o.jsx)(g.JO,{name:"materialization"}),to:(0,f.$U)(n,"/jobs/".concat(l)),children:"Materialize an asset"})})]}):(0,o.jsxs)(i.x,{flex:{direction:"column",gap:12},children:[(0,o.jsx)("div",{children:r?"There are no matching runs for these filters.":"You have not launched any runs for this job yet."}),(0,o.jsx)("div",{children:(0,o.jsx)(m.A,{icon:(0,o.jsx)(g.JO,{name:"add_circle"}),to:(0,f.$U)(n,"/jobs/".concat(l,"/playground")),children:"Launch a run"})})]}):(0,o.jsx)("div",{children:"You have not launched any runs for this job."})})})};var y=r(76016),b=r(16336),P=r(69737),S=r(43984),E=r(33182),I=r(49767),C=r(42884),H=r(69973),_=r(52338),R=r(17975),F=r(22563);let k=["status","tag","id","created_date_before","created_date_after"],N=e=>{(0,P.Px)();let{pipelinePath:n}=(0,h.UO)(),{repoAddress:r=null}=e,t=(0,x.p3)(n),{pipelineName:s,snapshotId:a}=t,c=(0,j.Ux)(r),g=(0,j.E8)(c,s);(0,y.b)(t,g);let[m,f]=(0,_.oD)(k),N=(0,u.useMemo)(()=>[g?{token:"job",value:s}:{token:"pipeline",value:s},a?{token:"snapshotId",value:a}:null].filter(Boolean),[g,s,a]),w=(0,C.fn)(),A=(0,u.useMemo)(()=>{let e=[...m,...N];if(r){let n={token:"tag",value:"".concat(S.H.RepositoryLabelTag,"=").concat((0,F.Wg)(r))};e.push(n)}return{...(0,_.VH)(e),pipelineName:s,snapshotId:a}},[m,N,s,r,a]),O=(0,u.useCallback)(e=>{let n=(0,l.HY)(e);m.some(e=>(0,l.HY)(e)===n)||f([...m,e])},[m,f]),{entries:$,paginationProps:T,queryResult:D}=(0,R.a)(A,"all",w.value),Y=(0,b.C4)(D,b.dT),{button:B,activeFiltersJsx:q}=(0,_.Vv)({enabledFilters:k,tokens:m,onChange:f,loading:D.loading}),U=(0,o.jsxs)(i.x,{flex:{direction:"row",gap:8,alignItems:"center"},style:{width:"100%"},padding:{right:16},children:[B,w.element,(0,o.jsx)("div",{style:{flex:1}}),(0,o.jsx)(b.xi,{refreshState:Y})]}),G=(0,o.jsxs)(i.x,{flex:{direction:"row",gap:4,alignItems:"center"},children:[N.map(e=>{let{token:n,value:r}=e;return(0,o.jsx)(d.V,{children:"".concat(n,":").concat(r)},n)}),q,q.length>0&&(0,o.jsx)(p.Z,{onClick:()=>f([]),children:"Clear all"})]});return(0,o.jsx)(E.Lw.Provider,{value:{refetch:Y.refetch},children:D.error?(0,o.jsx)(I.f,{error:D.error}):(0,o.jsx)("div",{style:{minHeight:0},children:(0,o.jsx)(H.F,{entries:$,loading:D.loading,onAddTag:O,refetch:Y.refetch,actionBarComponents:U,belowActionBarComponents:G,paginationProps:T,filter:A,emptyState:()=>(0,o.jsx)(v,{repoAddress:r,anyFilter:m.length>0,jobName:s,jobPath:n})})})})};var w=r(20958),A=r(49438),O=r(78491),$=r(71902),T=r(30916),D=r(15332),Y=r(59923),B=r(85062);function q(){let e=(0,t._)(["\n  query PipelineRunsRootQuery($limit: Int, $cursor: String, $filter: RunsFilter!) {\n    pipelineRunsOrError(limit: $limit, cursor: $cursor, filter: $filter) {\n      ... on Runs {\n        results {\n          id\n          ...RunTableRunFragment\n        }\n      }\n      ... on InvalidPipelineRunsFilterError {\n        message\n      }\n      ...PythonErrorFragment\n    }\n  }\n\n  ","\n  ","\n"]);return q=function(){return e},e}let U=["status","tag","id","created_date_before","created_date_after"],G=e=>{let{flagLegacyRunsPage:n}=(0,A.gV)();return n?(0,o.jsx)(V,{...e}):(0,o.jsx)(N,{...e})},V=e=>{(0,P.Px)();let{pipelinePath:n}=(0,h.UO)(),{repoAddress:r=null}=e,t=(0,x.p3)(n),{pipelineName:g,snapshotId:m}=t,f=(0,j.Ux)(r),I=(0,j.E8)(f,g);(0,y.b)(t,I);let[C,H]=(0,_.oD)(U),R=(0,u.useMemo)(()=>[I?{token:"job",value:g}:{token:"pipeline",value:g},m?{token:"snapshotId",value:m}:null].filter(Boolean),[I,g,m]),k=[...C,...R];if(r){let e={token:"tag",value:"".concat(S.H.RepositoryLabelTag,"=").concat((0,F.Wg)(r))};k.push(e)}let{queryResult:N,paginationProps:w}=(0,D.l)({query:M,pageSize:25,variables:{filter:{...(0,_.VH)(k),pipelineName:g,snapshotId:m}},nextCursorForResult:e=>{var n;if("Runs"===e.pipelineRunsOrError.__typename)return null===(n=e.pipelineRunsOrError.results[24])||void 0===n?void 0:n.id},getResultArray:e=>e&&"Runs"===e.pipelineRunsOrError.__typename?e.pipelineRunsOrError.results:[]}),A=(0,u.useCallback)(e=>{let n=(0,l.HY)(e);C.some(e=>(0,l.HY)(e)===n)||H([...C,e])},[C,H]),O=(0,b.C4)(N,b.dT),{button:T,activeFiltersJsx:q}=(0,_.Vv)({enabledFilters:U,tokens:C,onChange:H,loading:N.loading});return(0,o.jsx)(E.Lw.Provider,{value:{refetch:N.refetch},children:(0,o.jsx)(s.T,{children:(0,o.jsx)(Y.g,{queryResult:N,allowStaleData:!0,children:e=>{let{pipelineRunsOrError:t}=e;if("Runs"!==t.__typename)return(0,o.jsx)(i.x,{padding:{vertical:64},children:(0,o.jsx)(a.t,{icon:"error",title:"Query Error",description:t.message})});let l=t.results.slice(0,25),{hasNextCursor:s,hasPrevCursor:u}=w;return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(B.Y,{$top:0,children:(0,o.jsx)($.A,{runs:l,onAddTag:A,actionBarComponents:(0,o.jsxs)(i.x,{flex:{direction:"row",justifyContent:"space-between",grow:1,alignItems:"center",gap:4},margin:{right:8},children:[T,(0,o.jsx)(b.xi,{refreshState:O})]}),belowActionBarComponents:(0,o.jsxs)(o.Fragment,{children:[R.map(e=>{let{token:n,value:r}=e;return(0,o.jsx)(d.V,{children:"".concat(n,":").concat(r)},n)}),q.length?(0,o.jsxs)(o.Fragment,{children:[q,(0,o.jsx)(p.Z,{onClick:()=>{H([])},children:"Clear all"})]}):null]}),emptyState:()=>(0,o.jsx)(v,{repoAddress:r,anyFilter:C.length>0,jobName:g,jobPath:n})})}),s||u?(0,o.jsx)("div",{style:{marginTop:"20px"},children:(0,o.jsx)(c.pI,{...w})}):null]})}})})})},M=(0,w.Ps)(q(),T.Z,O.B)}}]);
//# sourceMappingURL=1914.d34fa0470bba9446.js.map