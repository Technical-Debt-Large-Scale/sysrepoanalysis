!function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):"object"==typeof exports?exports.treemap=e():t.treemap=e()}(self,(function(){return(()=>{"use strict";var t={99:(t,e,n)=>{n.d(e,{Z:()=>s});var i=n(81),r=n.n(i),o=n(645),a=n.n(o)()(r());a.push([t.id,"@import url(https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap);"]),a.push([t.id,'*{user-select:none;padding:0;margin:0}.path{stroke-width:1.5;fill-opacity:1;stroke:#fff;stroke-opacity:1;opacity:1;cursor:pointer}.path:hover{stroke:#363636;stroke-width:2}.text{fill:#424242;fill-opacity:1;font-family:"Roboto",sans-serif;cursor:pointer;pointer-events:none}.text-scale{fill:#424242;fill-opacity:1;font-family:"Roboto",sans-serif}.tooltip{pointer-events:none}',""]);const s=a},645:t=>{t.exports=function(t){var e=[];return e.toString=function(){return this.map((function(e){var n="",i=void 0!==e[5];return e[4]&&(n+="@supports (".concat(e[4],") {")),e[2]&&(n+="@media ".concat(e[2]," {")),i&&(n+="@layer".concat(e[5].length>0?" ".concat(e[5]):""," {")),n+=t(e),i&&(n+="}"),e[2]&&(n+="}"),e[4]&&(n+="}"),n})).join("")},e.i=function(t,n,i,r,o){"string"==typeof t&&(t=[[null,t,void 0]]);var a={};if(i)for(var s=0;s<this.length;s++){var c=this[s][0];null!=c&&(a[c]=!0)}for(var l=0;l<t.length;l++){var d=[].concat(t[l]);i&&a[d[0]]||(void 0!==o&&(void 0===d[5]||(d[1]="@layer".concat(d[5].length>0?" ".concat(d[5]):""," {").concat(d[1],"}")),d[5]=o),n&&(d[2]?(d[1]="@media ".concat(d[2]," {").concat(d[1],"}"),d[2]=n):d[2]=n),r&&(d[4]?(d[1]="@supports (".concat(d[4],") {").concat(d[1],"}"),d[4]=r):d[4]="".concat(r)),e.push(d))}},e}},81:t=>{t.exports=function(t){return t[1]}},379:t=>{var e=[];function n(t){for(var n=-1,i=0;i<e.length;i++)if(e[i].identifier===t){n=i;break}return n}function i(t,i){for(var o={},a=[],s=0;s<t.length;s++){var c=t[s],l=i.base?c[0]+i.base:c[0],d=o[l]||0,h="".concat(l," ").concat(d);o[l]=d+1;var u=n(h),p={css:c[1],media:c[2],sourceMap:c[3],supports:c[4],layer:c[5]};if(-1!==u)e[u].references++,e[u].updater(p);else{var f=r(p,i);i.byIndex=s,e.splice(s,0,{identifier:h,updater:f,references:1})}a.push(h)}return a}function r(t,e){var n=e.domAPI(e);return n.update(t),function(e){if(e){if(e.css===t.css&&e.media===t.media&&e.sourceMap===t.sourceMap&&e.supports===t.supports&&e.layer===t.layer)return;n.update(t=e)}else n.remove()}}t.exports=function(t,r){var o=i(t=t||[],r=r||{});return function(t){t=t||[];for(var a=0;a<o.length;a++){var s=n(o[a]);e[s].references--}for(var c=i(t,r),l=0;l<o.length;l++){var d=n(o[l]);0===e[d].references&&(e[d].updater(),e.splice(d,1))}o=c}}},569:t=>{var e={};t.exports=function(t,n){var i=function(t){if(void 0===e[t]){var n=document.querySelector(t);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(t){n=null}e[t]=n}return e[t]}(t);if(!i)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");i.appendChild(n)}},216:t=>{t.exports=function(t){var e=document.createElement("style");return t.setAttributes(e,t.attributes),t.insert(e,t.options),e}},565:(t,e,n)=>{t.exports=function(t){var e=n.nc;e&&t.setAttribute("nonce",e)}},795:t=>{t.exports=function(t){var e=t.insertStyleElement(t);return{update:function(n){!function(t,e,n){var i="";n.supports&&(i+="@supports (".concat(n.supports,") {")),n.media&&(i+="@media ".concat(n.media," {"));var r=void 0!==n.layer;r&&(i+="@layer".concat(n.layer.length>0?" ".concat(n.layer):""," {")),i+=n.css,r&&(i+="}"),n.media&&(i+="}"),n.supports&&(i+="}");var o=n.sourceMap;o&&"undefined"!=typeof btoa&&(i+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(o))))," */")),e.styleTagTransform(i,t,e.options)}(e,t,n)},remove:function(){!function(t){if(null===t.parentNode)return!1;t.parentNode.removeChild(t)}(e)}}}},589:t=>{t.exports=function(t,e){if(e.styleSheet)e.styleSheet.cssText=t;else{for(;e.firstChild;)e.removeChild(e.firstChild);e.appendChild(document.createTextNode(t))}}}},e={};function n(i){var r=e[i];if(void 0!==r)return r.exports;var o=e[i]={id:i,exports:{}};return t[i](o,o.exports,n),o.exports}n.n=t=>{var e=t&&t.__esModule?()=>t.default:()=>t;return n.d(e,{a:e}),e},n.d=(t,e)=>{for(var i in e)n.o(e,i)&&!n.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})},n.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),n.r=t=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})};var i={};return(()=>{function t(t){return document.createElementNS("http://www.w3.org/2000/svg",t)}function e(t){return document.getElementById(t)}n.r(i),n.d(i,{default:()=>B,render:()=>z});var r=n(379),o=n.n(r),a=n(795),s=n.n(a),c=n(569),l=n.n(c),d=n(565),h=n.n(d),u=n(216),p=n.n(u),f=n(589),m=n.n(f),g=n(99),y={};y.styleTagTransform=m(),y.setAttributes=h(),y.insert=l().bind(null,"head"),y.domAPI=s(),y.insertStyleElement=p(),o()(g.Z,y),g.Z&&g.Z.locals&&g.Z.locals;const v=14,x={ROOT_CHANGE:new Event("root-change")},w=[];let b={data:[]};var $,C,A=null;function L(e,n,i={}){const{x:r,y:o,width:a,height:s}=i,c=t("path");return c.classList.add(e),c.setAttribute("style",`fill: ${n}`),c.setAttribute("d",`M${r},${o} L${a+r},${o} L${a+r},${s+o} L${r},${s+o} Z`),c}function E(t){const e=("canvas",document.createElement("canvas")).getContext("2d");return e.font="14px Roboto",e.measureText(t).width}function M(e,n,i,r=!0){const{coords:o,name:a}=n,s=t("text");s.classList.add(e),s.setAttribute("x",0),s.setAttribute("y",0),s.textContent=a;const c=E(a)+5;let l=o.width/c;(l>1&&v>o.height||l<1&&l*v>o.height)&&(l=0);const d=l>1?`translate(${o.x+5}, ${o.y+v})`:`translate(${o.x}, ${o.y+l*v})scale(${l})`;return s.setAttribute("style",`font-size: 14px; fill: ${i}; fill-opacity: ${l<.3?0:1}; white-space: pre;`),s.setAttribute("transform",d),r&&(n.topOffset=l>1?22:l*v+5),s}function O(){document.querySelectorAll(".tooltip").forEach((t=>t.remove()))}function T(t,e){A++,t.children.sort(((t,e)=>e.weight-t.weight)),t.children.forEach((t=>{const n={id:A,name:t.name,parent:e.id,weight:t.weight,topOffset:0,type:t.type,heatmap:t.heatmap,children:[],scaledWeight:0};e?.children?.push(n),T(t,n)}))}function S(t){return w.filter((e=>e.id==t.id)).length>0}function R(t,e){if(e?.id==t)return e;if(e.children.length>0)for(let n=0;n<e.children.length;n++){let i=R(t,e.children[n]);if(null!=i)return i}return null}function k(e,n,i={}){const{x:r,y:o,width:a,height:s}=i;i.width=i.width-30-60;const c=t("svg");c.setAttribute("id","treemap"),c.setAttribute("viewBox",`${r} ${o} ${a} ${s}`),c.appendChild(function(e,n={}){const{x:i,y:r,width:o,height:a}=n,s=t("g"),c=t("g"),l=t("defs"),d=t("linearGradient"),h=t("text");d.setAttribute("id","Gradient"),d.setAttribute("x1","0"),d.setAttribute("x2","0"),d.setAttribute("y1","0"),d.setAttribute("y1","1");const u=[5,20,30,40,50,60,70,80,90];u.forEach(((e,n)=>{let i=t("stop");i.setAttribute("offset",`${e}%`),i.setAttribute("stop-color",`hsl(240,100%,${u[u.length-n-1]}%)`),d.appendChild(i)})),l.appendChild(d),s.appendChild(l);const p={y:r+34+30,x:o+i+15,width:30,height:a-110};h.classList.add("text-scale"),h.setAttribute("x",p.x+20),h.setAttribute("y",p.y-20),h.setAttribute("text-anchor","middle"),h.setAttribute("style","font-size: 11px; fill: rgb(0,0,0); fill-opacity: 1; white-space: pre;"),h.textContent=e.title,s.appendChild(h);const f=L("scale","url('#Gradient')",p);s.appendChild(f);const m=e.values.max-e.values.min;return[e.values.min,Math.round(m/4),Math.round(m/2),Math.round(m/2+m/4),e.values.max].forEach((n=>{const i=(n-e.values.min)/(e.values.max-e.values.min);let r=t("text");r.classList.add("text-scale"),r.setAttribute("x",0),r.setAttribute("y",0),r.textContent=n;const o=(1-i)*p.height;r.setAttribute("style","font-size: 11px; fill: rgb(0,0,0); fill-opacity: 1; white-space: pre;"),r.setAttribute("transform",`translate(${p.x+p.width+5}, ${0==o?p.y+5:o+p.y})`),c.appendChild(r)})),s.appendChild(c),s}(n,i)),c.appendChild(function(e={}){const{x:n,y:i,width:r}=e,o=t("g"),a=L("path","hsl(240, 100%, 92%)",{y:i,x:n,width:r,height:34});a.addEventListener("click",(()=>function(){if(0==w.length)return;w.pop();const t=w[w.length-1];C=R(t?t.id:$.id,$),window.dispatchEvent(x.ROOT_CHANGE)}())),o.appendChild(a);const s=M("text",{name:$.name+": "+$.weight,coords:{y:i+10,width:r,x:n}},"rgb(0,0,0)",!1);return s.setAttribute("id","collapse-button-text"),o.appendChild(s),o}(i));const l=t("g");return l.classList.add("treemap-rects"),c.appendChild(l),e.appendChild(c),l}function j(t){for(;t.firstChild;)t.removeChild(t.firstChild)}function N(){return b.height>b.width?{value:b.width,vertical:!1}:{value:b.height,vertical:!0}}function I(n,i,r,o,a){if(0===n.length)return;const s=n.map((t=>t.scaledWeight)).reduce(((t,e)=>t+e),0)/i;n.forEach((n=>{const i=n.scaledWeight/s;let c={x:b.x,y:b.y};r?(c={...c,width:s,height:i},b.y+=i):(c={...c,width:i,height:s},b.x+=i),n.coords=c,function(t={}){const{y:e,x:n,width:i,height:r}=t;return e<r+e&&n<i+n}(c)&&o.appendChild(function(n,i){const{fill:r,color:o}=function(t,e){const n=e.max-e.min;let i=95;return n>0&&(i*=1-(t-e.min)/n),{fill:`hsl(240, 100%, ${i}%)`,color:i>50?"rgb(0,0,0)":"rgb(255,255,255)"}}(n.heatmap,i.values),a=t("g");return"DIR"===n.type&&a.addEventListener("click",(()=>function(t){null==t.parent||S(t)||(C=R(t.id,$),w.push(...function(t){const e=[];let n=C.parent;for(;null!=n;){let t=R(n,$);if(S(t))break;e.push({id:t.id,name:t.name,weight:t.weight}),n=t.parent}return e.pop(),e.reverse(),e.push({id:t.id,name:t.name,weight:t.weight}),e}(t)),window.dispatchEvent(x.ROOT_CHANGE))}(n))),a.addEventListener("mouseover",(()=>function(n,i,r,o){const{coords:a,name:s,weight:c,type:l}=n;let d,h,u,p,f=null;const m=["label="+s,"weight="+c,"type="+l?.toLowerCase(),o+"="+Math.round(n.heatmap)],g=C.coords.width+C.coords.x,y=C.coords.height,x=Math.max(...m.map((t=>E(t)))),w=t("g"),b=t("path");b.setAttribute("style",`fill: ${i};  fill-opacity: 1; stroke: rgb(54, 54, 54); stroke-width: 2;`),w.classList.add("tooltip"),w.appendChild(b);const $={width:10,top:0,bottom:0,left:0,right:0,middle:h>y?a.height-7:a.y+7};d=$.middle-m.length*v/2-5,h=$.middle+m.length*v/2+5,p=a.width+a.x,u=p+x,d=h>y?$.middle-m.length*v-5:d,h=h>y?$.middle+5:h,f=d+(h-d)/2<a.y?.82*(h-d):(h-d)/2,$.top=d+(h-d)/2<a.y?h-15:d+.8*f,$.bottom=d+(h-d)/2<a.y?h-8:h-.8*f,u>g?(u=a.width+a.x-$.width,p=u-x-$.width,$.right=u+$.width,b.setAttribute("d",`M${p},${d} L${u},${d} L${u},${$.top} L${$.right},${d+f} L${u},${$.bottom} L${u},${h} L${p},${h} L${p},${d}Z`)):($.left=p-$.width,b.setAttribute("d",`M${p},${d} L${u},${d} L${u},${h} L${p},${h} L${p},${$.bottom} L${$.left},${d+f} L${p},${$.top} L${p},${d}Z`)),m.forEach(((e,n)=>{let i=t("text");i.setAttribute("x",0),i.setAttribute("y",0),i.classList.add("tooltip-text"),i.setAttribute("style",`font-size: 14px; fill: ${r}; white-space: pre;`),i.setAttribute("transform",`translate(${p+5}, ${d+(n+1)*v})`),i.textContent=e,w.appendChild(i)})),e("treemap").appendChild(w)}(n,r,o,i.title))),a.addEventListener("mouseout",(()=>O())),a.appendChild(L("path",r,n.coords)),a.appendChild(M("text",n,o)),a}(n,a))})),r?(b.x+=s,b.y-=i,b.width-=s):(b.x-=i,b.y+=s,b.height-=s)}function Z(t,e){const n=t.map((t=>t.scaledWeight)),i=n.reduce(((t,e)=>t+e),0),r=Math.max(...n),o=Math.min(...n);return Math.max(e**2*r/i**2,i**2/(e**2*o))}function P(t,e,n,i,r){if(0===t.length)return;if(1===t.length)return function(t,e,n,i,r){const{vertical:o}=N();I(t,n,o,i,r),I(e,n,o,i,r)}(e,t,n,i,r);const o=[...e,t[0]];return 0===e.length||Z(e,n)>=Z(o,n)?(t.shift(),P(t,o,n,i,r)):(I(e,n,N().vertical,i,r),P(t,[],N().value,i,r))}function W(t,e,n){const i=t.id===C.id,r=t.children.map((t=>t.weight)).reduce(((t,e)=>t+e),0),o=i?t.coords.width:t.coords.width-10,a=i?t.coords.height-34:t.coords.height-t.topOffset-5;t.children.forEach((t=>{t.scaledWeight=t.weight*o*a/r}));const s=[...t.children];b={...b,x:i?t.coords.x:t.coords.x+5,y:i?t.coords.y+34:t.coords.y+t.topOffset,width:o,height:a},P(s,[],N().value,e,n),t.children.forEach((t=>{W(t,e,n)}))}function _(t,e,n){j(t),C.coords=e,W(C,t,n)}function G(){const t={min:0,max:0},e=n=>{n?.heatmap&&(n.heatmap>t.max?t.max=n.heatmap:n.heatmap<t.min&&(t.min=n.heatmap)),n.children.length>0&&n.children.forEach((t=>{e(t)}))};return e(C),t}function H(t){A=0;const e=(n=t,JSON.parse(n||"{}"));var n;const i=function(t){return{id:A||0,name:t.hasOwnProperty("name")?t.name:null,parent:t.parent||null,weight:t.weight||0,children:t.children||[],topOffset:0,type:t.type||null,heatmap:t.heatmap||null,coords:t.coords||{},scaledWeight:0}}({id:A,name:e.name,weight:e.weight,children:[],type:e.type,heatmap:e.heatmap,topOffset:0,parent:null,scaledWeight:0});return T(e,i),i}function z(t,n,i){const r=H(t);C=r,$=r,n.innerHTML="";const o={values:G(),title:i},a=n.getBoundingClientRect(),s=k(n,o,a);window.addEventListener("root-change",(()=>{O(),_(s,a,o),function(){const t=e("collapse-button-text"),n=w.map((t=>t.name));n.unshift($.name);const i=1==n.length?$.weight:w[w.length-1].weight;t.textContent=n.join(" / ")+": "+i}()})),window.addEventListener("resize",(()=>{!function(t,e){j(t);const n=t.getBoundingClientRect();_(k(t,e,n),n,e)}(n,o)})),_(s,a,o)}const B={render:z}})(),i})()}));