(window.webpackJsonp=window.webpackJsonp||[]).push([[9],{221:function(t,e,r){"use strict";var n=r(9),o=r(43),l=r(44),c=r(119),f=r(87),h=r(18),m=r(67).f,d=r(68).f,v=r(25).f,y=r(222).trim,w="Number",x=n.Number,_=x,C=x.prototype,I=l(r(88)(C))==w,N="trim"in String.prototype,O=function(t){var e=f(t,!1);if("string"==typeof e&&e.length>2){var r,n,o,l=(e=N?e.trim():y(e,3)).charCodeAt(0);if(43===l||45===l){if(88===(r=e.charCodeAt(2))||120===r)return NaN}else if(48===l){switch(e.charCodeAt(1)){case 66:case 98:n=2,o=49;break;case 79:case 111:n=8,o=55;break;default:return+e}for(var code,c=e.slice(2),i=0,h=c.length;i<h;i++)if((code=c.charCodeAt(i))<48||code>o)return NaN;return parseInt(c,n)}}return+e};if(!x(" 0o1")||!x("0b1")||x("+0x1")){x=function(t){var e=arguments.length<1?0:t,r=this;return r instanceof x&&(I?h((function(){C.valueOf.call(r)})):l(r)!=w)?c(new _(O(e)),r,x):O(e)};for(var k,A=r(16)?m(_):"MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,EPSILON,isFinite,isInteger,isNaN,isSafeInteger,MAX_SAFE_INTEGER,MIN_SAFE_INTEGER,parseFloat,parseInt,isInteger".split(","),E=0;A.length>E;E++)o(_,k=A[E])&&!o(x,k)&&v(x,k,d(_,k));x.prototype=C,C.constructor=x,r(29)(n,w,x)}},222:function(t,e,r){var n=r(6),o=r(48),l=r(18),c=r(223),f="["+c+"]",h=RegExp("^"+f+f+"*"),m=RegExp(f+f+"*$"),d=function(t,e,r){var o={},f=l((function(){return!!c[t]()||"​"!="​"[t]()})),h=o[t]=f?e(v):c[t];r&&(o[r]=h),n(n.P+n.F*f,"String",o)},v=d.trim=function(t,e){return t=String(o(t)),1&e&&(t=t.replace(h,"")),2&e&&(t=t.replace(m,"")),t};t.exports=d},223:function(t,e){t.exports="\t\n\v\f\r   ᠎             　\u2028\u2029\ufeff"},256:function(t,e,r){"use strict";r.r(e);r(14),r(8),r(15),r(20),r(21);var n=r(4),o=(r(221),r(33));function l(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(object);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,r)}return e}function c(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?l(Object(source),!0).forEach((function(e){Object(n.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):l(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var f={computed:c(c({},Object(o.b)(["settings","githubUrls"])),{},{menu:{get:function(){return this.$store.state.menu.open},set:function(t){this.$store.commit("menu/toggle",t)}},categories:function(){return this.$store.state.categories[this.$i18n.locale]}}),methods:{isCategoryActive:function(t){var e=this;return t.some((function(t){return t.to===e.$route.fullPath}))},isDocumentNew:function(t){if(t.version&&!(t.version<=0)){var e=localStorage.getItem("document-".concat(t.slug,"-version"));return t.version>Number(e)}}}},h=r(37),component=Object(h.a)(f,(function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("aside",{staticClass:"w-full lg:w-1/5 lg:block fixed lg:relative inset-0 mt-16 lg:mt-0 z-30 bg-white dark:bg-gray-900 lg:bg-transparent lg:dark:bg-transparent",class:{block:t.menu,hidden:!t.menu}},[r("div",{staticClass:"lg:sticky lg:top-16 overflow-y-auto h-full lg:h-auto lg:max-h-(screen-16)"},[r("ul",{staticClass:"p-4 lg:py-8 lg:pl-0 lg:pr-8"},[t.settings.algolia?t._e():r("li",{staticClass:"mb-4 lg:hidden"},[r("AppSearch")],1),t._v(" "),t._l(t.categories,(function(e,n,o){return r("li",{key:n,staticClass:"mb-4",class:{active:t.isCategoryActive(e),"lg:mb-0":o===Object.keys(t.categories).length-1}},[n?r("p",{staticClass:"mb-2 text-gray-500 uppercase tracking-wider font-bold text-sm lg:text-xs"},[t._v(t._s(n))]):t._e(),t._v(" "),r("ul",t._l(e,(function(e){return r("li",{key:e.slug,staticClass:"text-gray-700 dark:text-gray-300"},[r("NuxtLink",{staticClass:"px-2 rounded font-medium py-1 hover:text-primary-500 flex items-center justify-between",attrs:{to:t.localePath(e.to),"exact-active-class":"text-primary-500 bg-primary-100 hover:text-primary-500 dark:bg-primary-900"}},[t._v("\n              "+t._s(e.menuTitle||e.title)+"\n              "),r("client-only",[t.isDocumentNew(e)?r("span",{staticClass:"animate-pulse rounded-full bg-primary-500 opacity-75 h-2 w-2"}):t._e()])],1)],1)})),0)])})),t._v(" "),r("li",{staticClass:"lg:hidden space-x-2"},[r("p",{staticClass:"mb-2 text-gray-500 uppercase tracking-wider font-bold text-sm lg:text-xs"},[t._v("More")]),t._v(" "),r("div",{staticClass:"flex items-center space-x-4"},[t.settings.twitter?r("a",{staticClass:"inline-flex text-gray-700 dark:text-gray-300 hover:text-primary-500",attrs:{href:"https://twitter.com/"+t.settings.twitter,target:"_blank",rel:"noopener noreferrer",title:"Twitter",name:"Twitter"}},[r("IconTwitter",{staticClass:"w-5 h-5"})],1):t._e(),t._v(" "),t.settings.github?r("a",{staticClass:"inline-flex text-gray-700 dark:text-gray-300 hover:text-primary-500",attrs:{href:t.githubUrls.repo,target:"_blank",rel:"noopener noreferrer",title:"Github",name:"Github"}},[r("IconGithub",{staticClass:"w-5 h-5"})],1):t._e(),t._v(" "),r("AppLangSwitcher"),t._v(" "),r("AppColorSwitcher")],1)])],2)])])}),[],!1,null,null,null);e.default=component.exports;installComponents(component,{AppSearch:function(){return r.e(12).then(r.bind(null,266)).then((function(t){return t.default||t}))},IconTwitter:function(){return r.e(37).then(r.bind(null,289)).then((function(t){return t.default||t}))},IconGithub:function(){return r.e(30).then(r.bind(null,282)).then((function(t){return t.default||t}))},AppLangSwitcher:function(){return r.e(8).then(r.bind(null,263)).then((function(t){return t.default||t}))},AppColorSwitcher:function(){return r.e(4).then(r.bind(null,269)).then((function(t){return t.default||t}))}})}}]);