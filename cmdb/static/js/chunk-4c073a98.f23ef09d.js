(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4c073a98"],{"0d00":function(t,e,n){},a434:function(t,e,n){"use strict";var o=n("23e7"),i=n("23cb"),c=n("a691"),l=n("50c4"),s=n("7b0b"),a=n("65f0"),r=n("8418"),u=n("1dde"),d=n("ae40"),h=u("splice"),f=d("splice",{ACCESSORS:!0,0:0,1:2}),p=Math.max,v=Math.min,b=9007199254740991,w="Maximum allowed length exceeded";o({target:"Array",proto:!0,forced:!h||!f},{splice:function(t,e){var n,o,u,d,h,f,k=s(this),_=l(k.length),C=i(t,_),g=arguments.length;if(0===g?n=o=0:1===g?(n=0,o=_-C):(n=g-2,o=v(p(c(e),0),_-C)),_+n-o>b)throw TypeError(w);for(u=a(k,o),d=0;d<o;d++)h=C+d,h in k&&r(u,d,k[h]);if(u.length=o,n<o){for(d=C;d<_-o;d++)h=d+o,f=d+n,h in k?k[f]=k[h]:delete k[f];for(d=_;d>_-o+n;d--)delete k[d-1]}else if(n>o)for(d=_-o;d>C;d--)h=d+o-1,f=d+n-1,h in k?k[f]=k[h]:delete k[f];for(d=0;d<n;d++)k[d+C]=arguments[d+2];return k.length=_-o+n,u}})},c4cc:function(t,e,n){"use strict";n("0d00")},dbb3:function(t,e,n){"use strict";n.r(e);var o=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"container"},[n("el-row",{staticClass:"sections",staticStyle:{display:"flex"}},t._l(t.sections,(function(e,o){return n("el-col",{key:o,staticClass:"section",attrs:{span:24}},[n("el-card",{attrs:{shadow:"always"}},[n("div",{staticClass:"options"},t._l(e.options,(function(i){return n("a",{key:i.value,class:{active:e.currentOption===i.value},attrs:{href:"#"},on:{click:function(e){return t.handleRadioClick(i.value,o)}}},[t._v(t._s(i.label))])})),0),n("el-divider"),e.currentOption===e.contentOption?n("div",[t._v(t._s(e.content))]):t._e()],1),e.showButton&&o===t.sections.length-1?n("el-button",{on:{click:function(e){return t.handleAddButtonClick(o)}}},[t._v("新增")]):t._e()],1)})),1)],1)},i=[],c=(n("a434"),{data:function(){return{sections:[{contentOption:1,options:[{label:"选项1",value:1},{label:"选项2",value:2}],content:"选项1的文章内容",showButton:!0}]}},methods:{handleRadioClick:function(t,e){this.sections[e].contentOption=t},handleAddButtonClick:function(t){this.sections.length<3&&this.sections.splice(t+1,0,{contentOption:1,options:[{label:"选项1",value:1},{label:"选项2",value:2}],content:"选项1的文章内容",showButton:this.sections.length<2})}}}),l=c,s=(n("c4cc"),n("2877")),a=Object(s["a"])(l,o,i,!1,null,null,null);e["default"]=a.exports}}]);