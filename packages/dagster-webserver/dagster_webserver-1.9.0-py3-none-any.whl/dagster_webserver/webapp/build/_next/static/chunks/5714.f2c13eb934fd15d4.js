"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[5714],{75714:function(e,t,n){n.r(t),n.d(t,{MergedAutomationRoot:function(){return eY},default:function(){return eF}});var s=n(52322),r=n(14934),o=n(45774),i=n(37483),a=n(35292),l=n(55255),c=n(39013),d=n(74580),u=n(74159),h=n(35002),p=n(2784),m=n(55010),x=n(60603),g=n(38491),j=n(15358),f=n(34147),S=n(92506),y=n(20958),v=n(71406);let w={step:"initial",completion:{completed:0,errors:{}}},b=(e,t)=>{switch(t.type){case"reset":return w;case"start":return{...e,step:"updating"};case"update-success":{let{completion:t}=e;return{step:"updating",completion:{...t,completed:t.completed+1}}}case"update-error":{let{completion:n}=e;return{step:"updating",completion:{...n,completed:n.completed+1,errors:{...n.errors,[t.name]:t.error}}}}case"complete":return{...e,step:"completed"}}},N=()=>(0,p.useReducer)(b,w);var E=n(94062),C=n(99417),T=n(89398);let k=e=>{let{openWithIntent:t,onClose:n,onComplete:r,automations:o}=e,i=o.length,[a,d]=N();(0,p.useEffect)(()=>{"not-open"===t&&d({type:"reset"})},[t,d]);let[u]=(0,y.Db)(T.VE),[h]=(0,y.Db)(T.Xu),[m]=(0,y.Db)(C.Wz),[x]=(0,y.Db)(C.d0),w=async e=>{let{repoAddress:t,name:n,type:s}=e,r={repositoryLocationName:t.location,repositoryName:t.name};switch(s){case"sensor":{let{data:e}=await u({variables:{sensorSelector:{...r,sensorName:n}}});switch(null==e?void 0:e.startSensor.__typename){case"Sensor":d({type:"update-success"});return;case"SensorNotFoundError":case"UnauthorizedError":case"PythonError":d({type:"update-error",name:n,error:e.startSensor.message})}break}case"schedule":{let{data:e}=await m({variables:{scheduleSelector:{...r,scheduleName:n}}});switch(null==e?void 0:e.startSchedule.__typename){case"ScheduleStateResult":d({type:"update-success"});return;case"UnauthorizedError":case"PythonError":d({type:"update-error",name:n,error:e.startSchedule.message})}break}default:(0,v.UT)(s)}},b=async e=>{let{name:t,type:n,instigationState:s}=e,r={id:s.id};switch(n){case"sensor":{let{data:e}=await h({variables:r});switch(null==e?void 0:e.stopSensor.__typename){case"StopSensorMutationResult":d({type:"update-success"});return;case"UnauthorizedError":case"PythonError":d({type:"update-error",name:t,error:e.stopSensor.message})}break}case"schedule":{let{data:e}=await x({variables:r});switch(null==e?void 0:e.stopRunningSchedule.__typename){case"ScheduleStateResult":d({type:"update-success"});return;case"UnauthorizedError":case"PythonError":d({type:"update-error",name:t,error:e.stopRunningSchedule.message})}break}default:(0,v.UT)(n)}},k=async()=>{if("not-open"!==t){for(let e of(d({type:"start"}),o))"start"===t?await w(e):await b(e);d({type:"complete"}),r()}},A="updating"!==a.step;return(0,s.jsxs)(S.Vq,{isOpen:"not-open"!==t,title:"start"===t?"Start automations":"Stop automations",canEscapeKeyClose:A,canOutsideClickClose:A,onClose:n,children:[(0,s.jsx)(S.a7,{children:(0,s.jsxs)(f.Z,{direction:"column",spacing:24,children:[(()=>{if("not-open"===t)return null;switch(a.step){case"initial":if("stop"===t)return(0,s.jsx)("div",{children:"".concat(1===i?"1 automation":"".concat(i," automations")," will be stopped. Do you want to continue?")});return(0,s.jsx)("div",{children:"".concat(1===i?"1 automation":"".concat(i," automations")," will be started. Do you want to continue?")});case"updating":case"completed":let e=i>0?a.completion.completed/i:1;return(0,s.jsxs)(f.Z,{direction:"column",spacing:8,children:[(0,s.jsx)(j.k,{intent:"primary",value:Math.max(.1,e),animate:e<1}),"updating"===a.step?(0,s.jsx)(E.c,{message:"Automations are being updated, please do not navigate away yet."}):null]});default:return null}})(),(()=>{if("not-open"===t||"initial"===a.step)return null;if("updating"===a.step)return(0,s.jsx)("div",{children:"Please do not close the window or navigate away while automations are being updated."});let e=a.completion.errors,n=Object.keys(e).length,r=a.completion.completed-n;return(0,s.jsxs)(f.Z,{direction:"column",spacing:8,children:[r?(0,s.jsxs)(f.Z,{direction:"row",spacing:8,alignItems:"flex-start",children:[(0,s.jsx)(l.JO,{name:"check_circle",color:c.fA()}),(0,s.jsx)("div",{children:"start"===t?"Successfully started ".concat(1===r?"1 automation":"".concat(r," automations"),"."):"Successfully stopped ".concat(1===r?"1 automation":"".concat(r," automations"),".")})]}):null,n?(0,s.jsxs)(f.Z,{direction:"column",spacing:8,children:[(0,s.jsxs)(f.Z,{direction:"row",spacing:8,alignItems:"flex-start",children:[(0,s.jsx)(l.JO,{name:"warning",color:c.qr()}),(0,s.jsx)("div",{children:"start"===t?"Could not start ".concat(1===n?"1 automation":"".concat(n," automations"),":"):"Could not stop ".concat(1===n?"1 automation":"".concat(n," automations"),":")})]}),(0,s.jsx)("ul",{style:{margin:"8px 0"},children:Object.keys(e).map(t=>(0,s.jsx)("li",{children:(0,s.jsxs)(f.Z,{direction:"row",spacing:8,children:[(0,s.jsxs)("strong",{children:[t,":"]}),e[t]?(0,s.jsx)("div",{children:e[t]}):null]})},t))})]}):null]})})()]})}),(0,s.jsx)(S.cN,{children:(()=>{if("not-open"===t)return null;switch(a.step){case"initial":return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(g.zx,{onClick:n,children:"Cancel"}),(0,s.jsx)(g.zx,{intent:"primary",onClick:k,children:"start"===t?"Start ".concat(1===i?"1 automation":"".concat(i," automations")):"Stop ".concat(1===i?"1 automation":"".concat(i," automations"))})]});case"updating":return(0,s.jsx)(g.zx,{intent:"primary",disabled:!0,children:"start"===t?"Starting ".concat(1===i?"1 automation":"".concat(i," automations")):"Stopping ".concat(1===i?"1 automation":"".concat(i," automations"))});case"completed":return(0,s.jsx)(g.zx,{intent:"primary",onClick:n,children:"Done"})}})()})]})};var A=n(88257);let _=e=>{let t=!1,n=!1;for(let s of e){let{status:e}=s;if(e===A.ynu.RUNNING?n=!0:e===A.ynu.STOPPED&&(t=!0),n&&t)break}return{anyOff:t,anyOn:n}},z=e=>{let{automations:t,onDone:n}=e,r=t.length,[o,i]=(0,p.useState)("not-open"),{anyOff:a,anyOn:c}=(0,p.useMemo)(()=>_(t.map(e=>{let{instigationState:t}=e;return t})),[t]);return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(m.J,{content:(0,s.jsxs)(x.v2,{children:[(0,s.jsx)(x.sN,{text:"Start ".concat(1===r?"1 automation":"".concat(r," automations")),disabled:!a,"aria-disabled":!a,icon:"toggle_on",onClick:()=>{i("start")}}),(0,s.jsx)(x.sN,{text:"Stop ".concat(1===r?"1 automation":"".concat(r," automations")),disabled:!c,"aria-disabled":!c,icon:"toggle_off",onClick:()=>{i("stop")}})]}),placement:"bottom-end",children:(0,s.jsx)(g.zx,{disabled:!r,intent:"primary",rightIcon:(0,s.jsx)(l.JO,{name:"expand_more"}),children:"Actions"})}),(0,s.jsx)(k,{openWithIntent:o,automations:t,onClose:()=>i("not-open"),onComplete:()=>{n()}})]})};var R=n(18259),O=n(43212),U=n(88510),M=n(35505),P=n(17008);let I="60px minmax(400px, 1.5fr) 240px 1fr 200px 200px",L=e=>{let{checkbox:t}=e;return(0,s.jsxs)(P.VJ,{templateColumns:I,sticky:!0,children:[(0,s.jsx)(P.qN,{children:(0,s.jsx)("div",{style:{position:"relative",top:"-1px"},children:t})}),(0,s.jsx)(P.qN,{children:"Name"}),(0,s.jsx)(P.qN,{children:"Type"}),(0,s.jsx)(P.qN,{children:"Target"}),(0,s.jsx)(P.qN,{children:"Last tick"}),(0,s.jsx)(P.qN,{children:"Last run"})]})},q=(0,M.ZP)(r.x).withConfig({componentId:"sc-40d0a0cf-0"})(["display:grid;grid-template-columns:",";height:100%;"],I);var D=n(37504),Y=n(53664),F=n(47933),$=n(24427),Z=n(16336),V=n(60648),G=n(89516);let K=e=>{let{cronSchedule:t,executionTimezone:n}=e,r=(0,G.A)(t,n||"UTC");return(0,s.jsx)(X,{children:(0,s.jsx)(h.u,{content:t,placement:"top",children:(0,s.jsx)(O.V,{icon:"schedule",children:r})})})},X=M.ZP.div.withConfig({componentId:"sc-907f4215-0"})([".bp5-popover-target{max-width:100%;:focus{outline:none;}}"]);var H=n(6750),J=n(4219);let W=(e,t)=>{if(e===A.ynu.STOPPED&&0===t||e===A.ynu.RUNNING&&1===t)return null;let n=[];return e===A.ynu.RUNNING&&0===t?n.push("Schedule is set to be running, but either the scheduler is not configured or the scheduler is not running the schedule"):e===A.ynu.STOPPED&&t>0&&n.push("Schedule is set to be stopped, but the scheduler is still running the schedule"),t>0&&n.push("Duplicate cron job for schedule found."),(0,s.jsx)(m.J,{interactionKind:"hover",popoverClassName:"bp5-popover-content-sizing",position:"right",content:(0,s.jsxs)(r.x,{flex:{direction:"column",gap:8},padding:12,children:[(0,s.jsx)("strong",{children:"There are errors with this schedule."}),(0,s.jsx)("div",{children:"Errors:"}),(0,s.jsx)("ul",{children:n.map((e,t)=>(0,s.jsx)("li",{children:e},t))})]}),children:(0,s.jsx)(O.V,{fill:!0,interactive:!0,intent:"danger",children:"Error"})})};var B=n(86269),Q=n(58905),ee=n(73235),et=n(83738);n(92199);var en=n(10539),es=n(77837),er=n(33182);function eo(){let e=(0,ee._)(["\n  query SingleScheduleQuery($selector: ScheduleSelector!) {\n    scheduleOrError(scheduleSelector: $selector) {\n      ... on Schedule {\n        id\n        name\n        pipelineName\n        description\n        scheduleState {\n          id\n          runningCount\n          hasStartPermission\n          hasStopPermission\n          ticks(limit: 1) {\n            id\n            ...TickTagFragment\n          }\n          runs(limit: 1) {\n            id\n            ...RunTimeFragment\n          }\n          nextTick {\n            timestamp\n          }\n        }\n        partitionSet {\n          id\n          name\n        }\n        ...ScheduleSwitchFragment\n      }\n    }\n  }\n\n  ","\n  ","\n  ","\n"]);return eo=function(){return e},e}n(43);let ei="1.2fr 1fr 1fr 76px 148px 210px 92px",ea="60px ".concat(ei);(0,M.ZP)(r.x).withConfig({componentId:"sc-ff7847b9-0"})(["display:grid;grid-template-columns:",";height:100%;"],e=>{let{$showCheckboxColumn:t}=e;return t?ea:ei});let el=(0,y.Ps)(eo(),es.dY,er.$X,J.J),ec=(0,p.forwardRef)((e,t)=>{var n;let{index:o,name:i,repoAddress:l,checked:c,onToggleChecked:d}=e,[u,m]=(0,y.td)(el,{variables:{selector:{repositoryName:l.name,repositoryLocationName:l.location,scheduleName:i}},notifyOnNetworkStatusChange:!0}),[x,g]=(0,y.td)(H.d,{variables:{scheduleSelector:{repositoryName:l.name,repositoryLocationName:l.location,scheduleName:i}}});(0,et.v5)((0,p.useCallback)(()=>{u(),x()},[u,x])),(0,Z.C4)(m,Z.dT),(0,Z.C4)(g,Z.dT);let{data:j}=m,f=(0,p.useMemo)(()=>(null==j?void 0:j.scheduleOrError.__typename)!=="Schedule"?null:j.scheduleOrError,[j]),S=null==f?void 0:f.scheduleState,v=(0,p.useMemo)(()=>{if(!S)return{disabled:!0};let{hasStartPermission:e,hasStopPermission:t,status:n}=S;return n!==A.ynu.RUNNING||t?n!==A.ynu.STOPPED||e?{disabled:!1}:{disabled:!0,message:"You do not have permission to start this schedule"}:{disabled:!0,message:"You do not have permission to stop this schedule"}},[S]),w=null==f?void 0:f.scheduleState.ticks[0],b=(null==f?void 0:f.pipelineName)?[{pipelineName:f.pipelineName}]:null,N=(null===(n=g.data)||void 0===n?void 0:n.scheduleOrError.__typename)==="Schedule"?g.data.scheduleOrError.assetSelection:null;return(0,s.jsx)("div",{ref:t,"data-index":o,children:(0,s.jsxs)(q,{border:"bottom",children:[(0,s.jsx)(P.E5,{children:(0,s.jsx)(h.u,{canShow:v.disabled,content:v.message||"",placement:"top",children:(0,s.jsx)(D.X,{disabled:v.disabled,checked:c,onChange:e=>{if(d&&e.target instanceof HTMLInputElement){let{checked:t}=e.target;d({checked:t,shiftKey:e.nativeEvent instanceof MouseEvent&&e.nativeEvent.getModifierState("Shift")})}}})})}),(0,s.jsx)(P.E5,{children:(0,s.jsxs)(r.x,{flex:{direction:"row",gap:8,alignItems:"flex-start"},children:[f?(0,s.jsxs)(r.x,{flex:{direction:"column",gap:4},children:[(0,s.jsx)(J.M,{repoAddress:l,schedule:f},i),W(f.scheduleState.status,f.scheduleState.runningCount)]}):(0,s.jsx)("div",{style:{width:30}}),(0,s.jsx)(F.rU,{to:(0,en.$U)(l,"/schedules/".concat(i)),children:(0,s.jsx)(Y.g,{text:i})})]})}),(0,s.jsx)(P.E5,{children:f?(0,s.jsxs)(r.x,{flex:{direction:"column",gap:4},children:[(0,s.jsx)(K,{cronSchedule:f.cronSchedule,executionTimezone:f.executionTimezone}),f.scheduleState.nextTick&&f.scheduleState.status===A.ynu.RUNNING?(0,s.jsx)(a.YS,{children:(0,s.jsxs)("div",{style:{overflow:"hidden",whiteSpace:"nowrap",maxWidth:"100%",textOverflow:"ellipsis"},children:["Next tick:\xa0",(0,s.jsx)(B.v,{timestamp:f.scheduleState.nextTick.timestamp,timezone:f.executionTimezone,timeFormat:{showSeconds:!1,showTimezone:!0}})]})}):null]}):(0,s.jsx)(et.mq,{queryResult:m})}),(0,s.jsx)(P.E5,{children:(0,s.jsx)("div",{children:(0,s.jsx)($.p,{repoAddress:l,automationType:"schedule",targets:b,assetSelection:N})})}),(0,s.jsx)(P.E5,{children:w?(0,s.jsx)("div",{children:(0,s.jsx)(Q.a,{tick:w,tickResultType:"runs"})}):(0,s.jsx)(et.mq,{queryResult:m})}),(0,s.jsx)(P.E5,{children:(null==f?void 0:f.scheduleState)&&(null==f?void 0:f.scheduleState.runs[0])?(0,s.jsx)(V.Z,{run:f.scheduleState.runs[0],name:i,showButton:!1,showHover:!0,showSummary:!1}):(0,s.jsx)(et.mq,{queryResult:m})})]})})});var ed=n(68856),eu=n(60918);function eh(){let e=(0,ee._)(["\n  query SingleSensorQuery($selector: SensorSelector!) {\n    sensorOrError(sensorSelector: $selector) {\n      ... on Sensor {\n        id\n        description\n        name\n        targets {\n          pipelineName\n        }\n        metadata {\n          assetKeys {\n            path\n          }\n        }\n        minIntervalSeconds\n        description\n        sensorState {\n          id\n          runningCount\n          hasStartPermission\n          hasStopPermission\n          ticks(limit: 1) {\n            id\n            ...TickTagFragment\n          }\n          runs(limit: 1) {\n            id\n            ...RunTimeFragment\n          }\n          nextTick {\n            timestamp\n          }\n        }\n        ...SensorSwitchFragment\n      }\n    }\n  }\n\n  ","\n  ","\n  ","\n"]);return eh=function(){return e},e}n(55546);let ep="1.5fr 180px 1fr 76px 120px 148px 180px",em="60px ".concat(ep);(0,M.ZP)(r.x).withConfig({componentId:"sc-452e670b-0"})(["display:grid;grid-template-columns:",";height:100%;"],e=>{let{$showCheckboxColumn:t}=e;return t?em:ep});let ex={[A.dEY.ASSET]:{name:"Asset sensor",icon:"sensors",description:"Asset sensors instigate runs when a materialization occurs"},[A.dEY.AUTO_MATERIALIZE]:{name:"Automation condition sensor",icon:"automation_condition",description:"Automation condition sensors trigger runs based on conditions defined on assets or checks."},[A.dEY.AUTOMATION]:{name:"Automation condition sensor",icon:"automation_condition",description:"Automation condition sensors trigger runs based on conditions defined on assets or checks."},[A.dEY.FRESHNESS_POLICY]:{name:"Freshness policy sensor",icon:"sensors",description:"Freshness sensors check the freshness of assets on each tick, then perform an action in response to that status"},[A.dEY.MULTI_ASSET]:{name:"Multi-asset sensor",icon:"sensors",description:"Multi asset sensors trigger job executions based on multiple asset materialization event streams"},[A.dEY.RUN_STATUS]:{name:"Run status sensor",icon:"sensors",description:"Run status sensors react to run status"},[A.dEY.STANDARD]:{name:"Standard sensor",icon:"sensors",description:null},[A.dEY.UNKNOWN]:{name:"Standard sensor",icon:"sensors",description:null}},eg=(0,y.Ps)(eh(),es.dY,er.$X,eu.U),ej=(0,p.forwardRef)((e,t)=>{var n;let{index:o,name:i,repoAddress:a,checked:l,onToggleChecked:c}=e,[d,u]=(0,y.td)(eg,{variables:{selector:{repositoryName:a.name,repositoryLocationName:a.location,sensorName:i}}}),[m,x]=(0,y.td)(ed.Z,{variables:{sensorSelector:{repositoryName:a.name,repositoryLocationName:a.location,sensorName:i}}});(0,et.v5)((0,p.useCallback)(()=>{d(),m()},[d,m])),(0,Z.C4)(u,Z.dT),(0,Z.C4)(x,Z.dT);let{data:g}=u,j=(0,p.useMemo)(()=>(null==g?void 0:g.sensorOrError.__typename)!=="Sensor"?null:g.sensorOrError,[g]),f=null==j?void 0:j.sensorState,S=(0,p.useMemo)(()=>{if(!f)return{disabled:!0};let{hasStartPermission:e,hasStopPermission:t,status:n}=f;return n!==A.ynu.RUNNING||t?n!==A.ynu.STOPPED||e?{disabled:!1}:{disabled:!0,message:"You do not have permission to start this sensor"}:{disabled:!0,message:"You do not have permission to stop this sensor"}},[f]),v=null==j?void 0:j.sensorState.ticks[0],w=null==j?void 0:j.sensorType,b=w?ex[w]:null,N=(null===(n=x.data)||void 0===n?void 0:n.sensorOrError.__typename)==="Sensor"?x.data.sensorOrError.assetSelection:null;return(0,s.jsx)("div",{ref:t,"data-index":o,children:(0,s.jsxs)(q,{border:"bottom",children:[(0,s.jsx)(P.E5,{children:(0,s.jsx)(h.u,{canShow:S.disabled,content:S.message||"",placement:"top",children:(0,s.jsx)(D.X,{disabled:S.disabled,checked:l,onChange:e=>{if(c&&e.target instanceof HTMLInputElement){let{checked:t}=e.target;c({checked:t,shiftKey:e.nativeEvent instanceof MouseEvent&&e.nativeEvent.getModifierState("Shift")})}}})})}),(0,s.jsx)(P.E5,{children:(0,s.jsxs)(r.x,{flex:{direction:"row",gap:8,alignItems:"flex-start"},children:[j?(0,s.jsx)(eu.c,{repoAddress:a,sensor:j},i):(0,s.jsx)("div",{style:{width:30}}),(0,s.jsx)(F.rU,{to:(0,en.$U)(a,"/sensors/".concat(i)),children:(0,s.jsx)(Y.g,{text:i})})]})}),(0,s.jsx)(P.E5,{children:(0,s.jsx)("div",{children:b?b.description?(0,s.jsx)(h.u,{content:(0,s.jsx)("div",{style:{maxWidth:"300px"},children:b.description}),placement:"top",children:(0,s.jsx)(O.V,{icon:b.icon,children:b.name})}):(0,s.jsx)(O.V,{icon:b.icon,children:b.name}):null})}),(0,s.jsx)(P.E5,{children:j?(0,s.jsx)("div",{children:(0,s.jsx)($.p,{targets:j.targets||null,repoAddress:a,assetSelection:N,automationType:j.sensorType})}):(0,s.jsx)(et.mq,{queryResult:x})}),(0,s.jsx)(P.E5,{children:v?(0,s.jsx)("div",{children:(0,s.jsx)(Q.a,{tick:v,tickResultType:"runs"})}):(0,s.jsx)(et.mq,{queryResult:u})}),(0,s.jsx)(P.E5,{children:(null==j?void 0:j.sensorState)&&(null==j?void 0:j.sensorState.runs[0])?(0,s.jsx)(V.Z,{run:j.sensorState.runs[0],name:i,showButton:!1,showHover:!0,showSummary:!1}):(0,s.jsx)(et.mq,{queryResult:u})})]})})});var ef=n(22921),eS=n(22563);let ey=(e,t)=>"".concat((0,eS.Uz)(e),"-").concat(t);var ev=n(98956),ew=n(50646);let eb=e=>{let{repos:t,headerCheckbox:n,checkedKeys:o,onToggleCheckFactory:i}=e,a=p.useRef(null),l=p.useMemo(()=>t.map(e=>{let{repoAddress:t}=e;return(0,eS.Uz)(t)}),[t]),{expandedKeys:c,onToggle:d,onToggleAll:u}=(0,ew.N)(ef.y,l),m=p.useMemo(()=>{let e=[];return t.forEach(t=>{let{repoAddress:n,schedules:s,sensors:r}=t;e.push({type:"header",repoAddress:n,scheduleCount:s.length,sensorCount:r.length});let o=(0,eS.Uz)(n);if(c.includes(o)){let t=new Set(r),o=new Set(s);[...r,...s].sort((e,t)=>v.Bl.compare(e,t)).forEach(s=>{t.has(s)?e.push({type:"sensor",repoAddress:n,sensor:s}):o.has(s)&&e.push({type:"schedule",repoAddress:n,schedule:s})})}}),e},[t,c]),x=(0,ev.w)(t.map(e=>{let{repoAddress:t}=e;return t.name})),g=(0,U.MG)({count:m.length,getScrollElement:()=>a.current,estimateSize:e=>{let t=m[e];return(null==t?void 0:t.type)==="header"?32:64},overscan:15}),j=g.getTotalSize(),f=g.getVirtualItems();return(0,s.jsx)("div",{style:{overflow:"hidden"},children:(0,s.jsxs)(P.W2,{ref:a,children:[(0,s.jsx)(L,{checkbox:n}),(0,s.jsx)(P.Nh,{$totalHeight:j,children:f.map(e=>{let{index:t,key:n,size:a,start:l}=e,p=m[t],j=p.type;if("header"===j)return(0,s.jsx)(R.X2,{$height:a,$start:l,children:(0,s.jsx)(et._$,{repoAddress:p.repoAddress,ref:g.measureElement,index:t,onToggle:d,onToggleAll:u,expanded:c.includes((0,eS.Uz)(p.repoAddress)),showLocation:x.has(p.repoAddress.name),rightElement:(0,s.jsxs)(r.x,{flex:{direction:"row",gap:4},children:[(0,s.jsx)(h.u,{content:1===p.sensorCount?"1 sensor":"".concat(p.sensorCount," sensors"),placement:"top",children:(0,s.jsx)(O.V,{icon:"sensors",children:p.sensorCount})}),(0,s.jsx)(h.u,{content:1===p.scheduleCount?"1 schedule":"".concat(p.scheduleCount," schedules"),placement:"top",children:(0,s.jsx)(O.V,{icon:"schedule",children:p.scheduleCount})})]})},n)},n);if("sensor"===j){let e=ey(p.repoAddress,p.sensor);return(0,s.jsx)(R.X2,{$height:a,$start:l,children:(0,s.jsx)(ej,{index:t,ref:g.measureElement,name:p.sensor,checked:o.has(e),onToggleChecked:i(e),repoAddress:p.repoAddress},n)},n)}if("schedule"===j){let e=ey(p.repoAddress,p.schedule);return(0,s.jsx)(R.X2,{$height:a,$start:l,children:(0,s.jsx)(ec,{index:t,ref:g.measureElement,name:p.schedule,checked:o.has(e),onToggleChecked:i(e),repoAddress:p.repoAddress},n)},n)}return(0,s.jsx)("div",{},n)})})]})})};var eN=n(69737),eE=n(20171),eC=n(4378),eT=n(52154);let ek=e=>e.hasStartPermission&&e.status===A.ynu.STOPPED||e.hasStopPermission&&e.status===A.ynu.RUNNING;var eA=n(907),e_=n(49455),ez=n(97211),eR=n(74548),eO=n(2389),eU=n(50027),eM=n(59030);let eP=()=>{let[e,t]=(0,eC.q)({encode:e=>({instigationStatus:e.size?Array.from(e).join(","):void 0}),decode:e=>{var t;return new Set((null===(t=e.instigationStatus)||void 0===t?void 0:t.split(","))||[])}});return(0,eR.im)({name:"Running state",icon:"toggle_off",allValues:[{value:A.ynu.RUNNING,match:["on","running"]},{value:A.ynu.STOPPED,match:["off","stopped"]}],getKey:e=>e,renderLabel:e=>{let{value:t}=e;return(0,s.jsx)("span",{children:t===A.ynu.RUNNING?"Running":"Stopped"})},state:e,onStateChanged:t,getStringValue:e=>e})};var eI=n(17867),eL=n(65822);let eq={schedules:{label:"Schedules",value:{type:"schedules",label:"Schedules"},match:["schedules"]},sensors:{label:"Sensors",value:{type:"sensors",label:"Sensors"},match:["sensors"]}},eD=Object.values(eq),eY=()=>{(0,eN.Px)(),(0,eE.j)("Automation");let{allRepos:e,visibleRepos:t,loading:n,data:m,refetch:x}=(0,p.useContext)(eI.C5),[g,j]=(0,eC.q)({queryKey:"search",defaults:{search:""}}),[f,S]=(0,eC.q)({encode:e=>({automationType:e.size?Array.from(e).join(","):void 0}),decode:e=>{var t;return new Set((null===(t=e.automationType)||void 0===t?void 0:t.split(","))||[])}}),y=(0,p.useMemo)(()=>new Set(Array.from(f).map(e=>eq[e].value)),[f]),v=(0,eU.A)(),w=eP(),b=(0,eR.im)({name:"Automation type",allValues:eD,icon:"automation_condition",getStringValue:e=>e.label,state:y,renderLabel:e=>{let{value:t}=e;return(0,s.jsx)("span",{children:t.label})},onStateChanged:e=>{S(new Set(Array.from(e).map(e=>e.type)))}}),N=(0,p.useMemo)(()=>{let e=Object.values(m).filter(e=>"WorkspaceLocationEntry"===e.__typename),n=(0,e_.S)(t);return e$(e).filter(e=>{let{repoAddress:t}=e;return n.has((0,eS.Uz)(t))})},[m,t]),E=(0,eM.in)({allTags:(0,eM.gP)(N,(0,p.useCallback)(e=>[...e.schedules.flatMap(e=>e.tags),...e.sensors.flatMap(e=>e.tags)],[]))}),{state:C}=E,T=(0,p.useMemo)(()=>[v,w,b,E],[v,w,b,E]),{button:k,activeFiltersJsx:A}=(0,ez.m)({filters:T}),{state:_}=w,R=(0,p.useMemo)(()=>N.map(e=>{let{sensors:t,schedules:n,...s}=e;return{...s,sensors:t.filter(e=>{let{sensorState:t,tags:n}=e;return(!C.size||!!(0,eM.wH)(Array.from(C),n))&&(!_.size||!!_.has(t.status))&&(!f.size||!!f.has("sensors"))}),schedules:n.filter(e=>{let{scheduleState:t,tags:n}=e;return(!C.size||!!(0,eM.wH)(Array.from(C),n))&&(!_.size||!!_.has(t.status))&&(!f.size||!!f.has("schedules"))})}}),[N,C,_,f]),O=g.trim().toLocaleLowerCase(),U=O.length>0,M=(0,p.useMemo)(()=>{let e=O.toLocaleLowerCase();return R.map(t=>{let{repoAddress:n,schedules:s,sensors:r}=t;return{repoAddress:n,schedules:s.filter(t=>{let{name:n}=t;return n.toLocaleLowerCase().includes(e)}).map(e=>{let{name:t}=e;return t}),sensors:r.filter(t=>{let{name:n}=t;return n.toLocaleLowerCase().includes(e)}).map(e=>{let{name:t}=e;return t})}}).filter(e=>{let{sensors:t,schedules:n}=e;return t.length>0||n.length>0})},[R,O]),P=(0,p.useMemo)(()=>R.map(e=>{let{repoAddress:t,schedules:n,sensors:s}=e;return[...s.filter(e=>{let{sensorState:t}=e;return ek(t)}).map(e=>{let{name:n,sensorState:s}=e;return{repoAddress:t,name:n,type:"sensor",instigationState:s}}),...n.filter(e=>{let{scheduleState:t}=e;return ek(t)}).map(e=>{let{name:n,scheduleState:s}=e;return{repoAddress:t,name:n,type:"schedule",instigationState:s}})]}).flat(),[R]),I=(0,p.useMemo)(()=>P.map(e=>{let{repoAddress:t,name:n}=e;return ey(t,n)}),[P]),[{checkedIds:L},{onToggleFactory:q,onToggleAll:D}]=(0,eT.a)(I),Y=(0,p.useMemo)(()=>{let e=new Set(M.map(e=>{let{repoAddress:t,schedules:n,sensors:s}=e;return[...n,...s].map(e=>ey(t,e))}).flat());return I.filter(t=>e.has(t))},[I,M]),F=(0,p.useMemo)(()=>{let e=new Set(Y.filter(e=>L.has(e)));return P.filter(t=>{let{repoAddress:n,name:s}=t;return e.has(ey(n,s))})},[Y,P,L]),$=I.length>0,Z=F.length,V=Y.length>0;return(0,s.jsxs)(r.x,{flex:{direction:"column"},style:{height:"100%",overflow:"hidden"},children:[(0,s.jsx)(d.m,{title:(0,s.jsx)(a.X6,{children:"Automation"})}),(0,s.jsxs)(r.x,{padding:{horizontal:24,vertical:12},flex:{direction:"row",alignItems:"center",justifyContent:"space-between",gap:12,grow:0},children:[(0,s.jsxs)(r.x,{flex:{direction:"row",gap:12},children:[k,(0,s.jsx)(u.oi,{icon:"search",value:g,onChange:e=>j(e.target.value),placeholder:"Filter by name…",style:{width:"340px"}})]}),(0,s.jsx)(h.u,{content:"You do not have permission to start or stop these schedules",canShow:V&&!$,placement:"top-end",useDisabledButtonTooltipFix:!0,children:(0,s.jsx)(z,{automations:F,onDone:()=>x()})})]}),A.length?(0,s.jsx)(r.x,{padding:{vertical:8,horizontal:24},border:"top-and-bottom",flex:{direction:"row",gap:8},children:A}):null,(()=>{if(n)return(0,s.jsx)(r.x,{flex:{direction:"row",justifyContent:"center"},padding:{top:64},children:(0,s.jsx)(o.f,{label:"Loading automations…"})});let d=e.length>t.length;return M.length?(0,s.jsx)(eb,{headerCheckbox:$?(0,s.jsx)(eO.W,{checkedCount:Z,totalCount:Y.length,onToggleAll:D}):void 0,repos:M,checkedKeys:L,onToggleCheckFactory:q}):U?(0,s.jsx)(r.x,{padding:{top:20},children:(0,s.jsx)(i.t,{icon:"search",title:"No matching automations",description:d?(0,s.jsxs)("div",{children:["No automations matching ",(0,s.jsx)("strong",{children:g})," were found in the selected code locations"]}):(0,s.jsxs)("div",{children:["No automations matching ",(0,s.jsx)("strong",{children:g})," were found in your definitions"]})})}):(0,s.jsx)(r.x,{padding:{top:20},children:(0,s.jsx)(i.t,{icon:"search",title:"No automations",description:d?"No automations were found in the selected code locations":(0,s.jsxs)(a.pN,{children:["There are no automations in this deployment."," ",(0,s.jsx)("a",{href:"https://docs.dagster.io/concepts/automation",target:"_blank",rel:"noreferrer",children:(0,s.jsxs)(r.x,{flex:{direction:"row",gap:4,alignItems:"center"},children:["Learn more about automations",(0,s.jsx)(l.JO,{name:"open_in_new",color:c.Es()})]})})]})})})})()]})};var eF=eY;let e$=e=>{let t=e.map(e=>e.locationOrLoadError),n=[];for(let e of t)if((null==e?void 0:e.__typename)==="RepositoryLocation")for(let t of e.repositories){let{name:s,schedules:r,sensors:o}=t,i=(0,eL.kQ)(s,e.name);(o.length>0||r.length>0)&&n.push({repoAddress:i,schedules:r,sensors:o})}return(0,eA.S)(n)}},907:function(e,t,n){n.d(t,{S:function(){return r}});var s=n(22563);let r=e=>[...e].sort((e,t)=>{let n=(0,s.Uz)(e.repoAddress),r=(0,s.Uz)(t.repoAddress);return n.localeCompare(r)})},49455:function(e,t,n){n.d(t,{S:function(){return o}});var s=n(65822),r=n(22563);let o=e=>new Set(e.map(e=>(0,r.Uz)((0,s.kQ)(e.repository.name,e.repositoryLocation.name))))}}]);
//# sourceMappingURL=5714.f2c13eb934fd15d4.js.map