
/* === HERMES JS v1.0 (LEGACY, DEBUG) === */
var h=null,j=!1;
if(!this.JSON){var k=/^\{"[\w\W.]*\}$/,m=/^\[[\w\W.]*\]$/,n=/^\s+/,q=/\s+$/,r=/^"[\w\W.]*"$/,s=function(a){return a.replace(n,"").replace(q,"")},u=function(a){return!isNaN(+a)?+a:k.test(a)||m.test(a)?t(a):"true"==a?!0:"false"==a?j:"null"==a?h:"undefined"==a?void 0:r.test(a)?a.slice(1,-1):a},v=function(a){var d,b,c,e,g;if(a!==h&&a.toJSON&&"function"===typeof a.toJSON)return a.toJSON();if("string"===typeof a)return'"'+a.replace('"','"')+'"';if(!("object"===typeof a&&void 0!==a||a instanceof Array))return""+
a;if(d="object"==typeof a&&!(a.length&&a.push&&a.slice))for(e in b="{",a)g=a[e],g!==a&&(b+='"'+e+'":'+v(g)+",");else{b="[";c=a.length;for(e=0;e<c;e++)g=a[e],b+=v(g)+","}b=b.slice(0,-1);return b+=d?"}":"]",b},t=function(a){var d,b,c,e,g,f;b=(d=k.test(a))?{}:[];a=a.slice(1,-1);a=a.split(",");c=a.length;for(e=0;e<c;e++)f=a[e],d?(f=f.split(":"),g=s(f.shift()).slice(1,-1),f=s(f.shift()),r.test(f)&&(f=f.slice(1,-1)),b[g]=u(f)):(f=s(f),b.push(u(f)));return b};this.JSON={parse:t,stringify:v}}var w=String.fromCharCode;
this.Base64={map:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",h:function(a){var d="",b=0;a=this.k.h(a);for(var c=this.map,e,g,f,l,p;b<a.length;)e=a.charCodeAt(b++),g=a.charCodeAt(b++),f=a.charCodeAt(b++),l=e>>2,e=(e&3)<<4|g>>4,p=isNaN(g)?64:(g&15)<<2|f>>6,g=isNaN(g)||isNaN(f)?64:f&63,d=d+c.charAt(l)+c.charAt(e)+c.charAt(p)+c.charAt(g);return d},f:function(a){var d="",b=0;a=a.replace(/[^A-Za-z0-9\+\/\=]/g,"");for(var c=this.map,e,g,f,l,p;b<a.length;)e=c.indexOf(a.charAt(b++)),
g=c.indexOf(a.charAt(b++)),f=c.indexOf(a.charAt(b++)),l=c.indexOf(a.charAt(b++)),e=e<<2|g>>4,g=(g&15)<<4|f>>2,p=(f&3)<<6|l,d+=w(e)+(64!=f?w(g):"")+(64!=l?w(p):"");return this.k.f(d)},k:{h:function(a){for(var d="",b=0,c;b<a.length;)c=a.charCodeAt(b++),d+=128>c?w(c):127<c&&2048>c?w(c>>6|192)+w(c&63|128):w(c>>12|224)+w(c>>6&63|128)+w(c&63|128);return d},f:function(a){for(var d="",b=0,c=0;b<a.length;)c=a.charCodeAt(b),d+=128>c?[w(c),b++][0]:191<c&&224>c?[w((c&31)<<6|a.charCodeAt(b+1)&63),b+=2][0]:[w((c&
15)<<12|(a.charCodeAt(b+1)&63)<<6|a.charCodeAt(b+2)&63),b+=3][0];return d}}};var x=this;function y(a){this.state={n:h,o:h,t:{G:[],C:[],w:h,host:"amp.sh"}};this.log("Initializing `EventTracker`.",this.p(a).load())}y.prototype.b={a:"amp-tracker",e:"amp-deferred"};y.prototype.a={key:"_amp",debug:!0,i:[JSON.stringify,JSON.parse],j:window.localStorage||j,d:{g:function(a){return a},l:function(a){return a}}};y.prototype.log=function(a){return console.log.apply(console,arguments)};
y.prototype.load=function(a){return{a:a?this.a=a:(cfg=document.getElementById(this.b.a))?this.a=this.a.i[1]((this.b.a=document.getElementById(this.b.a)).textContent):{},e:this.b.e=document.getElementById(this.b.e)||j,async:x.c?x.c.async||[]:[]}};
y.prototype.p=function(a){var d=a.navigator;this.state.n={v:d.cookieEnabled,language:d.language,vendor:d.vendor,I:d.userAgent,platform:d.platform,B:!!d.javaEnabled(),H:!!a.q||j,J:!!a.r||j,s:!!a.applicationCache||j,z:d.m?!!d.m:j,screen:a.screen?{width:a.screen.width,height:a.screen.height,u:a.screen.colorDepth,F:a.devicePixelRatio}:{}};this.state.o={D:this.a.j?(blob=this.a.j.getItem(this.a.d.g(this.a.key)))?this.a.i[1](this.a.d.l(blob)):h:j,A:navigator.cookieEnabled?0<document.cookie.length?(blob=
document.cookie.match(this.a.key+"=.*;"))?this.a.d.g(blob[0].substr(0,blob[0].length-1).split("=")[1]):h:h:j};return this};new (x.EventTracker=y)(x,x.c?x.c:[]);