// ==ClosureCompiler==
// @compilation_level ADVANCED_OPTIMIZATIONS
// @output_file_name t.min.js
// @formatting pretty_print
// ==/ClosureCompiler==

/*  @preserve
 *  ==== Ampush EventTracker JS (v1.0) ====
 *  @version: 1.0
 *  @author: Sam Gammon <sam.gammon@ampush.com>
 */

/** @define {boolean} **/
var ENABLE_DEBUG = true;

/** @define {boolean} **/
var ENABLE_CODEC = false;

/** @define {boolean} **/
var ENABLE_LEGACY = false;

/** @define {string}  **/
var IDENTIFIER_KEY = '_amp';

/** @define {string} **/
var EL_CONFIG = 'amp-tracker';

/** @define {string} **/
var EL_DEFERRED = 'amp-deferred';

/** @define {string} **/
var LOG_PREFIX = '[Tracker]';

/** @define {string} **/
var BEACON_HOST = 'amp.sh';


/* === JSON === */
ENABLE_LEGACY ? (function () {
    if (!this.JSON) {

        /**
         * Trim both sides of an input string.
         * @param {string} str Input string to trim.
         * @return {{parse: function(string), stringify: function(Object)}} Trimmed string value.
         */
        this['JSON'] = (function() {
            var re = {
                obj: /^\{"[\w\W.]*\}$/,
                arr: /^\[[\w\W.]*\]$/,
                triml: /^\s+/,
                trimr: /\s+$/,
                quote: /^"[\w\W.]*"$/
            },

            /**
             * Trim both sides of an input string.
             * @param {string} str Input string to trim.
             * @return {string} Trimmed string value.
             */
            trim = function(str) {
                return str.replace(re.triml, '').replace(re.trimr, '');
            },

            /**
             * Convert a string value to a full JavaScript object.
             * @param {string} v Input value to convert.
             * @return {*} Converted native value.
             */
            getValue = function(v) {
                return (!isNaN(+v) ? +v : re.obj.test(v) || re.arr.test(v) ? parse(v) :
                    v == 'true' ? true : v == 'false' ? false : v == 'null' ? null : v == 'undefined' ? undefined :
                    re.quote.test(v) ? v.slice(1, -1) : v
            );
        },

        /**
         * Serialize an object into JSON.
         * @param {Object} obj Input object to serialize.
         * @return {?} Stringified JSON object.
         */
        stringify = function(obj) {
            var isObj, str, len, k, v;
                if (obj !== null && obj.toJSON && typeof obj.toJSON === 'function') return obj.toJSON();
                if (typeof obj === 'string') return '"' + obj.replace('"', '\"') + '"';
                if (!(typeof obj === 'object' && obj !== undefined || obj instanceof Array)) return '' + obj;
                isObj = typeof obj == 'object' && !(obj.length && obj.push && obj.slice);
                if (isObj) {
                    str = '{';
                    for (k in obj) {
                        v = obj[k];
                        if (v === obj) continue;
                        str += '"' + k + '":' + stringify(v) + ',';
                    }
                } else {
                    str = '[';
                    len = obj.length;
                    for (k = 0; k < len; k++) {
                        v = obj[k];
                        str += stringify(v) + ',';
                    }
                }
                str = str.slice(0, -1);
                return (str += isObj ? '}' : ']', str);
        },

        /**
         * Deserialize a JSON string into an object.
         * @param {string} str Input string to deserialize.
         * @return {Object} Deserialized object.
         */
        parse = function(str) {
            var tuples, isObj, obj, len, i, k, v, tuple;
                isObj = re.obj.test(str);
                obj = isObj ? {} : [];
                str = str.slice(1, -1);
                tuples = str.split(',');
                len = tuples.length;
                for (i = 0; i < len; i++) {
                    tuple = tuples[i];
                    if (isObj) {
                        tuple = tuple.split(':');
                        k = trim(tuple.shift()).slice(1, -1);
                        v = trim(tuple.shift());
                        if (re.quote.test(v)) v = v.slice(1, -1);
                            obj[k] = getValue(v);
                        } else {
                            v = trim(tuple);
                            obj.push(getValue(v));
                        }
                } return obj;
        };

        return /** @struct */ {
            parse: parse,
            stringify: stringify
        };
    })();
}}).call(this) : (function () { return null; }).call(this);


/* === BASE64 === */
ENABLE_LEGACY ? (function (context) {

    var cc = String.fromCharCode, Base64 = context['Base64'] = /** @struct */ {
        map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

        /**
         * Encode a string in Base64.
         * @param {string} z Input string to encode in Base64.
         * @return {string}
         */
        encode: function (z) {
            var o = "", i = 0, n = this.utf8.encode(z), m = this.map,
                i1, i2, i3, e1, e2, e3, e4;
                while (i < n.length) {
                    i1 = n.charCodeAt(i++), i2 = n.charCodeAt(i++), i3 = n.charCodeAt(i++);
                    e1 = (i1 >> 2), e2 = (((i1 & 3) << 4) | (i2 >> 4)), e3 = (isNaN(i2) ? 64 : ((i2 & 15) << 2) | (i3 >> 6));
                    e4 = (isNaN(i2) || isNaN(i3)) ? 64 : i3 & 63, o = o + m.charAt(e1) + m.charAt(e2) + m.charAt(e3) + m.charAt(e4);
                } return o;
        },

        /**
         * Decode a string from Base64.
         * @param {string} z Input string to decode from Base64.
         * @return {string}
         */
        decode: function (z) {
            var o = "", i = 0, n = z.replace(/[^A-Za-z0-9\+\/\=]/g, ""), m = this.map,
                e1, e2, e3, e4, c1, c2, c3;
                while (i < n.length) {
                    e1 = m.indexOf(n.charAt(i++)), e2 = m.indexOf(n.charAt(i++));
                    e3 = m.indexOf(n.charAt(i++)), e4 = m.indexOf(n.charAt(i++));
                    c1 = (e1 << 2) | (e2 >> 4), c2 = ((e2 & 15) << 4) | (e3 >> 2);
                    c3 = ((e3 & 3) << 6) | e4;
                    o += (cc(c1) + ((e3 != 64) ? cc(c2) : "")) + (((e4 != 64) ? cc(c3) : ""));
                } return this.utf8.decode(o);
        },

        utf8: /** @struct */ {

            /**
             * Encode a string as UTF-8.
             * @param {string} n Input string to encode as utf8.
             * @return {string}
             */
            encode: function (n) {
                var o = "", i = 0, c;
                    while (i < n.length) {
                        c = n.charCodeAt(i++);
                        o += ((c < 128) ? cc(c) : ((c > 127) && (c < 2048)) ?
                        cc((c >> 6) | 192) + cc((c & 63) | 128) : (cc((c >> 12) | 224) + cc(((c >> 6) & 63) | 128) + cc((c & 63) | 128)));
                    } return o;
            },

            /**
             * Decode a string from UTF-8.
             * @param {string} n Input string to decode as utf8.
             * @return {string}
             */
            decode: function (n) {
                var o = "", i = 0, c = 0;
                    while (i < n.length) {
                        c = n.charCodeAt(i);
                        o += ((c < 128) ? [cc(c), i++][0] : ((c > 191) && (c < 224)) ?
                        [cc(((c & 31) << 6) | (n.charCodeAt(i + 1) & 63)), (i += 2)][0] :
                        [cc(((c & 15) << 12) | ((n.charCodeAt(i + 1) & 63) << 6) | (n.charCodeAt(i + 2) & 63)), (i += 3)][0]);
                    } return o;
            }

        }

    }; return Base64;
})(this) : (function () { return null; }).call(this);


(0 || (function (context) {

    /**
     * Constructor for `EventTracker` JS.
     * @constructor
     * @struct
     * @param {Window|Object} context An object to export `EventTracker` to.
     * @param {?Array} async Async queue variable passed in from the page (usually `_amp`).
     */
    function EventTracker(context, async) {

        /**
         * Holds Tracker-local state.
         * @type {Object}
         */
        this.state = /** @struct */ {  // `state: {}`: Runtime State
            env: {},  // gathered details about the current browser environment
            fingerprint: {},  // persistent or cookie-based identifier
            beacon: {
                sent: [],  // sent tracking beacons
                pending: [],  // stack of historical beacons (for multiple)
                current: {},  // current beacon object
                host: BEACON_HOST  // hostname endpoint for beacons
            }
        };

        // gather environment and load configuration
        ENABLE_DEBUG ? this.log('Initializing `EventTracker`.', this.gather(context).load()) : this.gather(context).load() ;

    }

    /**
     * Cached DOM elements.
     * @type {Object}
     */
    EventTracker.prototype.el = /** @struct */ {
        config: EL_CONFIG,  // JSON configuration blob location (if DOM-provided)
        deferred: EL_DEFERRED  // ID for container for deffered script/img actions
    };

    /**
     * Materialized configuration.
     * @type {Object}
     */
    EventTracker.prototype.config = /** @struct */ {
        key: IDENTIFIER_KEY,  // name of cookie and `localStorage` pointer
        debug: ENABLE_DEBUG,  // boolean toggle for `debug` mode, which turns on logging
        serializer: [JSON.stringify, JSON.parse],  // object enserializer/deserializer pair
        storage: (window.localStorage || false),  // browser storage engine (for persistent fingerprinting)
        codec: {  // obfuscation encoder/decoder pair
            en: function (x) { return (ENABLE_CODEC ? window.btoa(x) : x); },
            de: function (x) { return (ENABLE_CODEC ? window.atob(x) : x); }
        }
    };

    /**
     * Echo a `log` message.
     * @param {...Object|string} args Objects to dump to the console.
     * @return {null}
     */
    EventTracker.prototype.log = (ENABLE_DEBUG ? function (args) { return console.log.apply(console, arguments); } : function (args) { return null; });

    /**
     * `Load` configuration and relevant DOM elements.
     *  @param {Object=} override Configuration object to overlay on top of in-page config, if any.
     *  @return {Object} Spec object with props `config` (materialized config), `deferred` (deferred el), `async` (queued beacons).
     */
    EventTracker.prototype.load = function (override) {
        return {
            // resolve config blob from DOM or hand back override
            config: (override ? (this.config = override) :
                (cfg = document.getElementById(this.el.config)) ?
                    (this.config = this.config.serializer[1]((this.el.config = document.getElementById(this.el.config)).textContent)) : {}),

            // grab deferred element, default to false if it can't be found
            deferred: (this.el.deferred = document.getElementById(this.el.deferred) || false),

            // look for asynchronously-invoked events
            async: (context._amp ? context._amp.async || [] : [])
        };
    };

    /**
     * `Gather` details about the JS environment, and any persistent/ephemeral session tokens present.
     * @param {Window|Object} context The context to read and fingerprint.
     * @return {EventTracker} The current `EventTracker` object.
     */
    EventTracker.prototype.gather = function (context) {

        var nav = context.navigator, scr = context.screen;

        /**
         * Environment state. Keeps track of browser and client environment.
         * @type {Object}
         */
        this.state.env = /** @struct */ {  // grab local environment details
            cookies: nav.cookieEnabled,  // whether cookies are enabled
            language: nav.language,  // current browser language
            vendor: nav.vendor,  // browser vendor
            ua: nav.userAgent,  // user-agent string
            platform: nav.platform,  // system architecture
            java: !!nav.javaEnabled(),  // support for Java
            socket: !!context.WebSocket || false,  // support for WebSockets
            worker: !!context.Worker || false,  // support for WebWorkers
            appcache: !!context.applicationCache || false,  // support for Appcaching
            dnt: (nav.doNotTrack ? !!nav.doNotTrack : false),  // whether the do-not-track header is enabled
            screen: scr ? {
                width: scr.width,  // try to detect screen width
                height: scr.height,  // try to detect screen height
                color_depth: scr.colorDepth,  // grab color depth
                pixel_density: context.devicePixelRatio  // grab pixel density (retina == 2, all else == 1)
            } : {}
        };

        /**
         * Fingerprint state. Keeps track of unique browser identification tokens.
         * @type {Object}
         */
        this.state.fingerprint = /** @struct */ {  // grab persistent (`localStorage`-based) or ephemeral (cookie-based) fingerprint, if any

            // storage-based fingerprinting: is the engine enabled, is our key there? (repectively)
            persistent: (this.config.storage ? (blob = this.config.storage.getItem(this.config.codec.en(this.config.key))) ?
                    this.config.serializer[1](this.config.codec.de(blob)) : null : false),
                    // ^  deserialize and decode if it's there, `null` for missing, `false` for not supported (respectively)

            // cookie-based fingerprinting: are cookies enabled, are there cookies, is ours there? (respectively)
            ephemeral: (navigator.cookieEnabled ? document.cookie.length > 0 ? (blob = document.cookie.match(this.config.key + '=.*;')) ?
                    this.config.codec.en(blob[0].substr(0, blob[0].length - 1).split('=')[1])  // drop ';', split cookie and decode
                : null : null : false)  // no amp cookie, no cookies, no support for cookies (respectively)

        }; return this;

    };

    /**
     * Collapse local environment and state into a serialized beacon.
     * @param {string} id Fingerprinted browser/user token.
     * @param {Object} env Environment to pass along to the tracker.
     * @return {Object} Returns the current `EventTracker`.
     */
    EventTracker.prototype.collapse = function (id, env) {

    };

    /**
     * Send collapsed beacon as an XHR or embedded image.
     * @param {string} endpoint Configuration object to overlay on top of in-page config, if any.
     * @param {Object} params Configuration object to overlay on top of in-page config, if any.
     * @return {XMLHttpRequest} Spec object with props `config` (materialized config), `deferred` (deferred el), `async` (queued beacons).
     */
     EventTracker.prototype.beacon = function (endpoint, params) {

     };

    return new (context['EventTracker'] = EventTracker)(context, (context._amp ? context._amp : []));
})(this));
