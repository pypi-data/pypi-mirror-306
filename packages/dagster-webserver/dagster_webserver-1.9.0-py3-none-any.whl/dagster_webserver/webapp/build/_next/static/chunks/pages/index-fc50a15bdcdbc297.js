(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[5405],{87314:function(e,t,r){(window.__NEXT_P=window.__NEXT_P||[]).push(["/",function(){return r(62564)}])},67328:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),function(e,t){for(var r in t)Object.defineProperty(e,r,{enumerable:!0,get:t[r]})}(t,{default:function(){return a},noSSR:function(){return o}});let l=r(43219);r(52322),r(2784);let n=l._(r(56800));function u(e){return{default:(null==e?void 0:e.default)||e}}function o(e,t){return delete t.webpack,delete t.modules,e(t)}function a(e,t){let r=n.default,l={loading:e=>{let{error:t,isLoading:r,pastDelay:l}=e;return null}};e instanceof Promise?l.loader=()=>e:"function"==typeof e?l.loader=e:"object"==typeof e&&(l={...l,...e});let a=(l={...l,...t}).loader;return(l.loadableGenerated&&(l={...l,...l.loadableGenerated},delete l.loadableGenerated),"boolean"!=typeof l.ssr||l.ssr)?r({...l,loader:()=>null!=a?a().then(u):Promise.resolve(u(()=>null))}):(delete l.webpack,delete l.modules,o(r,l))}("function"==typeof t.default||"object"==typeof t.default&&null!==t.default)&&void 0===t.default.__esModule&&(Object.defineProperty(t.default,"__esModule",{value:!0}),Object.assign(t.default,t),e.exports=t.default)},46085:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"LoadableContext",{enumerable:!0,get:function(){return l}});let l=r(43219)._(r(2784)).default.createContext(null)},56800:function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),Object.defineProperty(t,"default",{enumerable:!0,get:function(){return f}});let l=r(43219)._(r(2784)),n=r(46085),u=[],o=[],a=!1;function i(e){let t=e(),r={loading:!0,loaded:null,error:null};return r.promise=t.then(e=>(r.loading=!1,r.loaded=e,e)).catch(e=>{throw r.loading=!1,r.error=e,e}),r}class s{promise(){return this._res.promise}retry(){this._clearTimeouts(),this._res=this._loadFn(this._opts.loader),this._state={pastDelay:!1,timedOut:!1};let{_res:e,_opts:t}=this;e.loading&&("number"==typeof t.delay&&(0===t.delay?this._state.pastDelay=!0:this._delay=setTimeout(()=>{this._update({pastDelay:!0})},t.delay)),"number"==typeof t.timeout&&(this._timeout=setTimeout(()=>{this._update({timedOut:!0})},t.timeout))),this._res.promise.then(()=>{this._update({}),this._clearTimeouts()}).catch(e=>{this._update({}),this._clearTimeouts()}),this._update({})}_update(e){this._state={...this._state,error:this._res.error,loaded:this._res.loaded,loading:this._res.loading,...e},this._callbacks.forEach(e=>e())}_clearTimeouts(){clearTimeout(this._delay),clearTimeout(this._timeout)}getCurrentValue(){return this._state}subscribe(e){return this._callbacks.add(e),()=>{this._callbacks.delete(e)}}constructor(e,t){this._loadFn=e,this._opts=t,this._callbacks=new Set,this._delay=null,this._timeout=null,this.retry()}}function d(e){return function(e,t){let r=Object.assign({loader:null,loading:null,delay:200,timeout:null,webpack:null,modules:null},t),u=null;function i(){if(!u){let t=new s(e,r);u={getCurrentValue:t.getCurrentValue.bind(t),subscribe:t.subscribe.bind(t),retry:t.retry.bind(t),promise:t.promise.bind(t)}}return u.promise()}if(!a){let e=r.webpack?r.webpack():r.modules;e&&o.push(t=>{for(let r of e)if(t.includes(r))return i()})}function d(e,t){!function(){i();let e=l.default.useContext(n.LoadableContext);e&&Array.isArray(r.modules)&&r.modules.forEach(t=>{e(t)})}();let o=l.default.useSyncExternalStore(u.subscribe,u.getCurrentValue,u.getCurrentValue);return l.default.useImperativeHandle(t,()=>({retry:u.retry}),[]),l.default.useMemo(()=>{var t;return o.loading||o.error?l.default.createElement(r.loading,{isLoading:o.loading,pastDelay:o.pastDelay,timedOut:o.timedOut,error:o.error,retry:u.retry}):o.loaded?l.default.createElement((t=o.loaded)&&t.default?t.default:t,e):null},[e,o])}return d.preload=()=>i(),d.displayName="LoadableComponent",l.default.forwardRef(d)}(i,e)}function c(e,t){let r=[];for(;e.length;){let l=e.pop();r.push(l(t))}return Promise.all(r).then(()=>{if(e.length)return c(e,t)})}d.preloadAll=()=>new Promise((e,t)=>{c(u).then(e,t)}),d.preloadReady=e=>(void 0===e&&(e=[]),new Promise(t=>{let r=()=>(a=!0,t());c(o,e).then(r,r)})),window.__NEXT_PRELOADREADY=d.preloadReady;let f=d},62564:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return s}});var l=r(52322),n=r(25237),u=r.n(n),o=r(5632),a=r(2784);let i=u()(()=>Promise.all([r.e(9055),r.e(9937),r.e(5587),r.e(401),r.e(2816),r.e(6216),r.e(1659),r.e(1267),r.e(4363)]).then(r.bind(r,3172)),{loadableGenerated:{webpack:()=>[3172]},ssr:!1});function s(){let e=(0,o.useRouter)();return(0,a.useEffect)(()=>{e.beforePopState(()=>!1)},[e]),(0,l.jsx)("div",{id:"root",children:(0,l.jsx)(i,{})})}},25237:function(e,t,r){e.exports=r(67328)},5632:function(e,t,r){e.exports=r(69442)}},function(e){e.O(0,[2888,9774,179],function(){return e(e.s=87314)}),_N_E=e.O()}]);
//# sourceMappingURL=index-fc50a15bdcdbc297.js.map