"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[832],{60832:function(e,t,n){n.r(t),n.d(t,{CodeLocationsPage:function(){return Q},CodeLocationsPageContent:function(){return X},default:function(){return Y}});var o=n(52322),i=n(14934),r=n(74159),l=n(35292),s=n(74580),a=n(2784),c=n(9108),d=n(77265),x=n(53476);let u=(e,t)=>{let n=[],o=t.reduce((e,t)=>(e[t.name]=t,e),{});for(let t of e){var i,r;let e;let l=o[t.name];e="LOADING"===t.loadStatus?"Updating":(null==l?void 0:l.versionKey)!==t.versionKey?"Loading":(null==l?void 0:null===(i=l.locationOrLoadError)||void 0===i?void 0:i.__typename)==="PythonError"?"Failed":"Loaded",(null==l?void 0:null===(r=l.locationOrLoadError)||void 0===r?void 0:r.__typename)==="RepositoryLocation"?l.locationOrLoadError.repositories.forEach(o=>{n.push({type:"repository",locationStatus:t,locationEntry:l,repository:o,status:e})}):n.push({type:"location",locationStatus:t,locationEntry:l||null,status:e})}return n},h=(e,t,n)=>{let o=t.toLocaleLowerCase();return e.filter(e=>{var t;return(null===(t=n.status)||void 0===t||!t.length||!!n.status.includes(e.status))&&("repository"!==e.type?e.locationStatus.name.toLocaleLowerCase().includes(o):e.locationStatus.name.toLocaleLowerCase().includes(o)||e.repository.name.toLocaleLowerCase().includes(o))})},j=function(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"",o=arguments.length>3&&void 0!==arguments[3]?arguments[3]:{status:[]},i=u(e,t),r=h(i,n,o);return{flattened:i,filtered:r}};var p=n(4378),m=n(90483),g=n(5343),y=n(97211),f=n(74548),v=n(17867);let w=()=>{let{loading:e,locationEntries:t}=(0,a.useContext)(v.C5),n=(0,x.sJ)(g.n),[i,r]=(0,a.useState)(""),l=(0,a.useCallback)(e=>{r(e.target.value)},[]),s=i.toLocaleLowerCase(),[c,d]=(0,p.q)({encode:e=>{let{status:t}=e;return{status:Array.isArray(t)?t:void 0}},decode:e=>({status:Array.isArray(null==e?void 0:e.status)?e.status:[]})}),{flattened:u,filtered:h}=(0,a.useMemo)(()=>{var e;return j((null==n?void 0:null===(e=n.locationStatusesOrError)||void 0===e?void 0:e.__typename)==="WorkspaceLocationStatusEntries"?n.locationStatusesOrError.entries:[],t,s,c)},[t,s,c,n]),w=(0,f.im)({name:"Status",icon:"tag",allValues:(0,a.useMemo)(()=>["Failed","Loaded","Updating","Loading"].map(e=>({key:e,value:e,match:[e]})),[]),menuWidth:"300px",renderLabel:e=>{let{value:t}=e;return(0,o.jsx)(m.rd,{text:t})},getStringValue:e=>e,state:c.status,onStateChanged:e=>{d({status:Array.from(e)})},matchType:"all-of",canSelectAll:!1,allowMultipleSelections:!0}),{button:C,activeFiltersJsx:L}=(0,y.m)({filters:[w]});return{button:C,activeFiltersJsx:L,onChangeSearch:l,loading:e,flattened:u,filtered:h,searchValue:i}};var C=n(69737),L=n(20171),b=n(72447),E=n(79106),S=n(37483),N=n(18259),O=n(88510),k=n(53664),_=n(38491),V=n(47933),I=n(35505),z=n(14277),$=n(12576),U=n(35002),F=n(43212),M=n(10539),A=n(44900);let D=e=>{let{repo:t,repoAddress:n}=e,r=t.assetGroups.length,l=t.pipelines.filter(e=>{let{name:t}=e;return!(0,A.pv)(t)}).length,s=t.schedules.length,a=t.sensors.length;return(0,o.jsxs)(i.x,{flex:{direction:"row",gap:8,alignItems:"center"},children:[(0,o.jsx)(U.u,{content:1===r?"1 asset group":"".concat(r," asset groups"),placement:"top",children:(0,o.jsx)(P,{to:(0,M.$U)(n,"/assets"),children:(0,o.jsx)(F.V,{interactive:!0,icon:"asset_group",children:r})})}),(0,o.jsx)(U.u,{content:1===l?"1 job":"".concat(l," jobs"),placement:"top",children:(0,o.jsx)(P,{to:(0,M.$U)(n,"/jobs"),children:(0,o.jsx)(F.V,{interactive:!0,icon:"job",children:l})})}),(0,o.jsx)(U.u,{content:1===s?"1 schedule":"".concat(s," schedules"),placement:"top",children:(0,o.jsx)(P,{to:(0,M.$U)(n,"/schedules"),children:(0,o.jsx)(F.V,{interactive:!0,icon:"schedule",children:s})})}),(0,o.jsx)(U.u,{content:1===a?"1 sensor":"".concat(a," sensors"),placement:"top",children:(0,o.jsx)(P,{to:(0,M.$U)(n,"/sensors"),children:(0,o.jsx)(F.V,{interactive:!0,icon:"sensors",children:a})})})]})},P=(0,I.ZP)(V.rU).withConfig({componentId:"sc-97d114c1-0"})([":hover,:active{outline:none;text-decoration:none;}"]);var q=n(65822),T=n(22563),W=n(35599),R=n(17008);let J="3fr 1fr 1fr 160px",Z=a.forwardRef((e,t)=>{let{locationEntry:n,locationStatus:r,index:l}=e,{name:s}=r,a=(0,q.kQ)(q.Js,s);return(0,o.jsx)("div",{ref:t,"data-index":l,children:(0,o.jsxs)(H,{border:"bottom",children:[(0,o.jsx)(R.E5,{children:(0,o.jsx)(i.x,{flex:{direction:"column",gap:4},children:(0,o.jsx)("div",{style:{fontWeight:500},children:(0,o.jsx)(V.rU,{to:(0,M.$U)(a),children:(0,o.jsx)(k.g,{text:s})})})})}),(0,o.jsx)(R.E5,{children:(0,o.jsx)("div",{children:(0,o.jsx)($._y,{locationStatus:r,locationOrError:n})})}),(0,o.jsx)(R.E5,{children:(0,o.jsx)("div",{style:{whiteSpace:"nowrap"},children:(0,o.jsx)(W.C,{unixTimestamp:r.updateTimestamp})})}),(0,o.jsx)(R.E5,{children:(0,o.jsxs)(_.zH,{children:[(0,o.jsx)($.hN,{location:s}),n?(0,o.jsx)(z.c5,{locationNode:n}):null]})})]})})}),B=a.forwardRef((e,t)=>{let{locationEntry:n,locationStatus:r,repository:l,index:s}=e,a=(0,q.kQ)(l.name,l.location.name),c=[...n.displayMetadata,...l.displayMetadata];return(0,o.jsx)("div",{ref:t,"data-index":s,children:(0,o.jsxs)(H,{border:"bottom",children:[(0,o.jsx)(R.E5,{children:(0,o.jsxs)(i.x,{flex:{direction:"column",gap:4},children:[(0,o.jsx)("div",{style:{fontWeight:500},children:(0,o.jsx)(V.rU,{to:(0,M.$U)(a),children:(0,o.jsx)(k.g,{text:(0,T.Uz)(a)})})}),(0,o.jsx)($.OM,{metadata:c}),(0,o.jsx)($.F8,{metadata:c}),(0,o.jsx)(D,{repo:l,repoAddress:a})]})}),(0,o.jsx)(R.E5,{children:(0,o.jsx)("div",{children:(0,o.jsx)($._y,{locationStatus:r,locationOrError:n})})}),(0,o.jsx)(R.E5,{children:(0,o.jsx)("div",{style:{whiteSpace:"nowrap"},children:(0,o.jsx)(W.C,{unixTimestamp:r.updateTimestamp})})}),(0,o.jsx)(R.E5,{style:{alignItems:"flex-end"},children:(0,o.jsxs)(_.zH,{children:[(0,o.jsx)($.hN,{location:r.name}),(0,o.jsx)(z.c5,{locationNode:n})]})})]})})}),G=()=>(0,o.jsxs)(R.VJ,{templateColumns:J,sticky:!0,children:[(0,o.jsx)(R.qN,{children:"Name"}),(0,o.jsx)(R.qN,{children:"Status"}),(0,o.jsx)(R.qN,{children:"Updated"}),(0,o.jsx)(R.qN,{style:{textAlign:"right"},children:"Actions"})]}),H=(0,I.ZP)(i.x).withConfig({componentId:"sc-23cbebdb-0"})(["display:grid;grid-template-columns:",";"],J),K=e=>{let{loading:t,codeLocations:n,searchValue:r,isFilteredView:l}=e,s=(0,a.useRef)(null),c=(0,O.MG)({count:n.length,getScrollElement:()=>s.current,estimateSize:()=>64,overscan:10}),d=c.getTotalSize(),x=c.getVirtualItems();return t&&!n.length?(0,o.jsxs)(i.x,{flex:{gap:8,alignItems:"center"},padding:{horizontal:24},children:[(0,o.jsx)(E.$,{purpose:"body-text"}),(0,o.jsx)("div",{children:"Loading…"})]}):n.length?(0,o.jsxs)(R.W2,{ref:s,children:[(0,o.jsx)(G,{}),(0,o.jsx)(R.Nh,{$totalHeight:d,children:x.map(e=>{let{index:t,key:i,size:r,start:l}=e,s=n[t];return"location"===s.type?(0,o.jsx)(N.X2,{$height:r,$start:l,children:(0,o.jsx)(Z,{index:t,locationEntry:s.locationEntry,locationStatus:s.locationStatus,ref:c.measureElement})},i):(0,o.jsx)(N.X2,{$height:r,$start:l,children:(0,o.jsx)(B,{index:t,locationStatus:s.locationStatus,locationEntry:s.locationEntry,repository:s.repository,ref:c.measureElement})},i)})})]}):r?(0,o.jsx)(i.x,{padding:{vertical:32},children:(0,o.jsx)(S.t,{icon:"folder",title:"No matching code locations",description:(0,o.jsxs)("div",{children:["No code locations were found for search query ",(0,o.jsx)("strong",{children:r}),"."]})})}):l?(0,o.jsx)(i.x,{padding:{vertical:32},children:(0,o.jsx)(S.t,{icon:"folder",title:"No matching code locations",description:(0,o.jsx)("div",{children:"No code locations were found for these filter settings."})})}):(0,o.jsx)(i.x,{padding:{vertical:32},children:(0,o.jsx)(S.t,{icon:"folder",title:"No code locations",description:"When you add a code location, your definitions will appear here."})})},X=()=>{(0,C.Px)(),(0,L.j)("Code locations");let{activeFiltersJsx:e,flattened:t,button:n,loading:s,filtered:a,onChangeSearch:c,searchValue:d}=w(),x=t.length,u=x>10;return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsxs)(i.x,{padding:{vertical:16,horizontal:24},flex:{direction:"row",justifyContent:"space-between",alignItems:"center"},style:{height:"64px"},children:[(0,o.jsxs)(i.x,{flex:{direction:"row",gap:8,alignItems:"center"},children:[n,u?(0,o.jsx)(r.oi,{icon:"search",value:d,onChange:c,placeholder:"Filter code locations by name…",style:{width:"400px"}}):(0,o.jsx)(l.pm,{id:"repository-locations",children:s||!x?"Code locations":1===x?"1 code location":"".concat(x," code locations")})]}),(0,o.jsxs)(i.x,{flex:{direction:"row",gap:12,alignItems:"center"},children:[u?(0,o.jsx)("div",{children:"".concat(x," code locations")}):null,(0,o.jsx)(b.i,{})]})]}),e.length?(0,o.jsx)(i.x,{flex:{direction:"row",alignItems:"center",gap:4},padding:{horizontal:24},children:e}):null,(0,o.jsx)(K,{loading:s,codeLocations:a,isFilteredView:!!e.length,searchValue:d})]})},Q=()=>{let{pageTitle:e}=a.useContext(c.N);return(0,o.jsxs)(i.x,{flex:{direction:"column"},style:{height:"100%",overflow:"hidden"},children:[(0,o.jsx)(s.m,{title:(0,o.jsx)(l.X6,{children:e}),tabs:(0,o.jsx)(d.Z,{tab:"locations"})}),(0,o.jsx)(X,{})]})};var Y=Q},14277:function(e,t,n){n.d(t,{c5:function(){return h}});var o=n(52322),i=n(60603),r=n(55010),l=n(38491),s=n(55255),a=n(92506),c=n(1747),d=n(20156),x=n(2784),u=n(45984);let h=e=>{var t;let{locationNode:n}=e,[a,c]=(0,x.useState)(!1),[d,u]=(0,x.useState)(!1),h=null,m=null;return(null===(t=n.locationOrLoadError)||void 0===t?void 0:t.__typename)==="RepositoryLocation"&&null!==n.locationOrLoadError.dagsterLibraryVersions&&(h=(0,o.jsx)(i.sN,{icon:"info",text:"View Dagster libraries",onClick:()=>u(!0)}),m=(0,o.jsx)(p,{libraries:n.locationOrLoadError.dagsterLibraryVersions,isOpen:d,setIsOpen:u})),(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(r.J,{position:"bottom-left",content:(0,o.jsxs)(i.v2,{children:[(0,o.jsx)(i.sN,{icon:"info",text:"View configuration",onClick:()=>c(!0)}),h]}),children:(0,o.jsx)(l.zx,{icon:(0,o.jsx)(s.JO,{name:"expand_more"})})}),(0,o.jsx)(j,{metadata:n.displayMetadata,isOpen:a,setIsOpen:c}),m]})},j=e=>{let{isOpen:t,setIsOpen:n,metadata:i}=e;return(0,o.jsxs)(a.Vq,{title:"Code location configuration",icon:"info",isOpen:t,onClose:()=>n(!1),style:{width:"600px"},children:[(0,o.jsx)(m,{displayMetadata:i}),(0,o.jsx)(a.cN,{topBorder:!0,children:(0,o.jsx)(l.zx,{onClick:()=>n(!1),intent:"primary",children:"Done"})})]})},p=e=>{let{isOpen:t,setIsOpen:n,libraries:i}=e;return(0,o.jsxs)(a.Vq,{title:"Dagster library versions",icon:"info",isOpen:t,onClose:()=>n(!1),style:{width:"600px"},children:[(0,o.jsxs)(c.i,{children:[(0,o.jsx)("thead",{children:(0,o.jsxs)("tr",{children:[(0,o.jsx)("th",{children:"Library"}),(0,o.jsx)("th",{children:"Version"})]})}),(0,o.jsx)("tbody",{children:i.map(e=>(0,o.jsxs)("tr",{children:[(0,o.jsx)("td",{children:e.name}),(0,o.jsx)("td",{children:e.version})]},e.name))})]}),(0,o.jsx)(a.cN,{topBorder:!0,children:(0,o.jsx)(l.zx,{onClick:()=>n(!1),intent:"primary",children:"Done"})})]})},m=e=>{let{displayMetadata:t}=e,n=(0,x.useMemo)(()=>{let e=t.reduce((e,t)=>(e[t.key]=t.value,e),{});return u.Pz(e)},[t]);return(0,o.jsx)(d.u,{value:n,options:{readOnly:!0,lineNumbers:!0,mode:"yaml"},theme:["config-editor"]})}},12576:function(e,t,n){n.d(t,{F8:function(){return L},OM:function(){return w},_y:function(){return b},hN:function(){return E}});var o=n(52322),i=n(35002),r=n(83373),l=n(53664),s=n(14934),a=n(39013),c=n(43212),d=n(89891),x=n(38491),u=n(55255),h=n(74188),j=n(2784),p=n(35505),m=n(81306),g=n(50309),y=n(85227),f=n(22203),v=n(68954);let w=e=>{let{metadata:t}=e,n=(0,y.m)(),s=t.find(e=>{let{key:t}=e;return"image"===t}),a=(null==s?void 0:s.value)||"",c=(0,j.useCallback)(async()=>{n(a),await (0,g.B7)({intent:"success",icon:"done",message:"Image string copied!"})},[n,a]);return s?(0,o.jsxs)(C,{flex:{direction:"row",gap:4},children:[(0,o.jsx)("span",{style:{fontWeight:500},children:"image:"}),(0,o.jsx)(i.u,{content:"Click to copy",placement:"top",display:"block",children:(0,o.jsx)(r.k,{onClick:c,style:S,children:(0,o.jsx)(l.g,{text:s.value})})})]}):null},C=(0,p.ZP)(s.x).withConfig({componentId:"sc-5a4acf7-0"})(["width:100%;color:",";font-size:12px;.bp5-popover-target{overflow:hidden;}"],a.$()),L=e=>{let{metadata:t}=e,n=t.find(e=>{let{key:t}=e;return"module_name"===t||"package_name"===t||"python_file"===t});return n?(0,o.jsxs)(s.x,{flex:{direction:"row",gap:4},style:{width:"100%",color:a.$(),fontSize:12},children:[(0,o.jsxs)("span",{style:{fontWeight:500},children:[n.key,":"]}),(0,o.jsx)("div",{style:S,children:(0,o.jsx)(l.g,{text:n.value})})]}):null},b=e=>{var t;let{locationStatus:n,locationOrError:i}=e,[r,l]=(0,j.useState)(!1),a=(0,j.useMemo)(()=>(0,v.je)((null==n?void 0:n.name)||""),[null==n?void 0:n.name]),{reloading:x,tryReload:u}=(0,v.Dc)({scope:"location",reloadFn:a});return(null==n?void 0:n.loadStatus)==="LOADING"?(0,o.jsx)(c.V,{minimal:!0,intent:"primary",children:"Updating…"}):(null==i?void 0:i.versionKey)!==(null==n?void 0:n.versionKey)?(0,o.jsx)(c.V,{minimal:!0,intent:"primary",children:"Loading…"}):n&&(null==i?void 0:null===(t=i.locationOrLoadError)||void 0===t?void 0:t.__typename)==="PythonError"?(0,o.jsxs)(o.Fragment,{children:[(0,o.jsxs)(s.x,{flex:{alignItems:"center",gap:12},children:[(0,o.jsx)(c.V,{minimal:!0,intent:"danger",children:"Failed"}),(0,o.jsx)(d.Z,{onClick:()=>l(!0),children:(0,o.jsx)("span",{style:{fontSize:"12px"},children:"View error"})})]}),(0,o.jsx)(m.p,{location:n.name,isOpen:r,error:i.locationOrLoadError,reloading:x,onDismiss:()=>l(!1),onTryReload:()=>u()})]}):(0,o.jsx)(c.V,{minimal:!0,intent:"success",children:"Loaded"})},E=e=>{let{location:t}=e;return(0,o.jsx)(f.s,{location:t,ChildComponent:e=>{let{reloading:t,tryReload:n,hasReloadPermission:r}=e;return(0,o.jsx)(s.x,{flex:{direction:"row",alignItems:"center",gap:4},children:(0,o.jsx)(i.u,{content:r?"":f.H,canShow:!r,useDisabledButtonTooltipFix:!0,children:(0,o.jsx)(x.zx,{icon:(0,o.jsx)(u.JO,{name:"code_location_reload"}),disabled:!r,loading:t,onClick:()=>n(),children:"Reload"})})})}})},S={width:"100%",display:"block",fontFamily:h.b.monospace,fontSize:"12px",color:a.$()}}}]);
//# sourceMappingURL=832.6e7ffc6b2ba66574.js.map