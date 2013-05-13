// ==ClosureCompiler==
// @compilation_level ADVANCED_OPTIMIZATIONS
// @output_file_name t.min.js
// @formatting pretty_print
// ==/ClosureCompiler==

var ENABLE_DEBUG, ENABLE_CODEC, IDENTIFIER_KEY, EL_CONFIG, EL_DEFERRED, LOG_PREFIX;

/** @define {boolean} **/
ENABLE_DEBUG = true;

/** @define {boolean} **/
ENABLE_CODEC = false;

/** @define {string}  **/
IDENTIFIER_KEY = '_amp';

/** @define {string} **/
EL_CONFIG = 'amp-tracker';

/** @define {string} **/
EL_DEFERRED = 'amp-deferred';

/** @define {string} **/
LOG_PREFIX = '[Tracker]';


/*  @preserve
 *  ==== Ampush EventTracker JS (v1.0) ====
 *  @version: 1.0
 *  @author: Sam Gammon <sam.gammon@ampush.com>
 */

(0 || (function (context) {

    /**
     * Constructor for `EventTracker` JS.
     * @constructor
     * @typedef {Object}
     * @param {Window|Object} context An object to export `EventTracker` to.
     * @param {?Object} async Async queue variable passed in from the page (usually `_amp`).
     * @struct
     */
    function EventTracker(context, async) {

        this.state = {  // `state: {}`: Runtime State
            env: null,  // gathered details about the current browser environment
            fingerprint: null,  // persistent or cookie-based identifier
            beacon: {
                sent: [],  // sent tracking beacons
                pending: [],  // stack of historical beacons (for multiple)
                current: null  // current beacon object
            }
        };

        // gather environment and load configuration
        ENABLE_DEBUG ? this.log('Initializing `EventTracker`.', async, this.gather().load()) : this.gather().load() ;

    }

    /**
     * Cached DOM elements.
     * @type {Object}
     * @struct
     */
    EventTracker.prototype.el = {
        config: EL_CONFIG,  // JSON configuration blob location (if DOM-provided)
        deferred: EL_DEFERRED  // ID for container for deffered script/img actions
    };

    /**
     * Materialized configuration.
     * @type {Object}
     * @struct
     */
    EventTracker.prototype.config = {
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
     * @param {string} msg String message to log directly after prefix.
     * @param {...string} var_args Objects or annotation data to stringify and dump.
     * @return {null}
     */
    EventTracker.prototype.log = (ENABLE_DEBUG ? function (msg) { ENABLE_DEBUG ? ((arguments.length > 1) ?  // only log in debug mode, only dump args if there's > 1
        console.log(LOG_PREFIX, msg, arguments) : console.log(LOG_PREFIX, msg)) : null } : null);

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
                    (this.config = this.serializer[1]((this.el.config = document.getElementById(this.el.config)).textContent)) : {}),

            // grab deferred element, default to false if it can't be found
            deferred: (this.el.deferred = document.getElementById(this.el.deferred) || false),

            // look for asynchronously-invoked events
            async: (context._amp ? context._amp.async || [] : [])
        };
    };

    /**
     *  `Gather` details about the JS environment, and any persistent/ephemeral session tokens present.
     *   @return {EventTracker} The current `EventTracker` object.
     */
    EventTracker.prototype.gather = function () {

        /**
         * Environment state. Keeps track of browser and client environment.
         * @type {Object}
         * @struct
         */
        this.state.env = {  // grab local environment details
            cookies: navigator.cookieEnabled,  // whether cookies are enabled
            language: navigator.language,  // current browser language
            vendor: navigator.vendor,  // browser vendor
            ua: navigator.userAgent,  // user-agent string
            platform: navigator.platform,  // system architecture
            dnt: !!navigator.doNotTrack,  // whether the do-not-track header is enabled
            java: !!navigator.javaEnabled(),  // support for Java
            socket: !!window.WebSocket || false,  // support for WebSockets
            worker: !!window.Worker || false,  // support for WebWorkers
            appcache: !!window.applicationCache || false,  // support for Appcaching
            screen: window.screen ? {
                width: window.screen.width,  // try to detect screen width
                height: window.screen.height,  // try to detect screen height
                color_depth: window.screen.colorDepth,  // grab color depth
                pixel_density: window.devicePixelRatio  // grab pixel density (retina == 2, all else == 1)
            } : {}
        };

        /**
         * Fingerprint state. Keeps track of unique browser identification tokens.
         * @type {Object}
         * @struct
         */
        this.state.fingerprint = {  // grab persistent (`localStorage`-based) or ephemeral (cookie-based) fingerprint, if any

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

    return new (context['EventTracker'] = EventTracker)(context, context._amp);
})(this));
