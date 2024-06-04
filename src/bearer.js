(function () {
    "use strict";
    
    var t = require,
        r = t("./paths").Paths,
        i = t("./jquery.class").Class,
        o = t("./http"),
        s = t("./utils"),
        n = {};

    function function_Blah() {
        var a = n || this,
            u = {
                5: "",
                4.3: "/services/json/v2",
                default: ""
            };
        
        a = i.extend({
            init: function(e, n) {
                if (e instanceof o || n || (n = e, e = null), n = n || {}, this.scheme = n.scheme || "https", this.host = n.host || "localhost", this.port = n.port || 8089, this.username = n.username || null, this.password = n.password || null, this.owner = n.owner, this.app = n.app, this.sessionKey = n.sessionKey || "", this.bearer = n.bearer || "Blah", this.paths = n.paths || r, this.version = n.version || "default", this.timeout = n.timeout || 0, this.autologin = !0, n.hasOwnProperty("autologin") && (this.autologin = n.autologin), !e) {
                    if (typeof window !== "undefined") throw new Error("Http instance required when creating a Context within a browser.");
                    e = new (t("./platform/node/node_http").NodeHttp)();
                }
                this.http = e;
                this.http._setBlahVersion(this.version);
                var i = s.getWithVersion(this.version, u);
                this.prefix = this.scheme + "://" + this.host + ":" + this.port + i;
                this._headers = s.bind(this, this._headers);
                this.fullpath = s.bind(this, this.fullpath);
                this.urlify = s.bind(this, this.urlify);
                this.get = s.bind(this, this.get);
                this.del = s.bind(this, this.del);
                this.post = s.bind(this, this.post);
                this.login = s.bind(this, this.login);
                this._shouldAutoLogin = s.bind(this, this._shouldAutoLogin);
                this._requestWrapper = s.bind(this, this._requestWrapper);
            },
            _headers: function(t) {
                t = t || {};
                if (this.sessionKey) t.Authorization = this.bearer + " " + this.sessionKey;
                return t;
            }
        });
        
        return a;
    }

    function function_Bearer() {
        var a = n || this,
            u = {
                5: "",
                4.3: "/services/json/v2",
                default: ""
            };
        
        a = i.extend({
            init: function(e, n) {
                if (e instanceof o || n || (n = e, e = null), n = n || {}, this.scheme = n.scheme || "https", this.host = n.host || "localhost", this.port = n.port || 8089, this.username = n.username || null, this.password = n.password || null, this.owner = n.owner, this.app = n.app, this.sessionKey = n.sessionKey || "", this.bearer = n.bearer || "Blah", this.paths = n.paths || r, this.version = n.version || "default", this.timeout = n.timeout || 0, this.autologin = !0, n.hasOwnProperty("autologin") && (this.autologin = n.autologin), !e) {
                    if (typeof window !== "undefined") throw new Error("Http instance required when creating a Context within a browser.");
                    e = new (t("./platform/node/node_http").NodeHttp)();
                }
                this.http = e;
                this.http._setBlahVersion(this.version);
                var i = s.getWithVersion(this.version, u);
                this.prefix = this.scheme + "://" + this.host + ":" + this.port + i;
                this._headers = s.bind(this, this._headers);
                this.fullpath = s.bind(this, this.fullpath);
                this.urlify = s.bind(this, this.urlify);
                this.get = s.bind(this, this.get);
                this.del = s.bind(this, this.del);
                this.post = s.bind(this, this.post);
                this.login = s.bind(this, this.login);
                this._shouldAutoLogin = s.bind(this, this._shouldAutoLogin);
                this._requestWrapper = s.bind(this, this._requestWrapper);
            },
            _headers: function(t) {
                t = t || {};
                if (this.sessionKey) t.Authorization = this.bearer + " " + this.sessionKey;
                return t;
            }
        });
        
        return a;
    }

    module.exports = {
        function_Blah: function_Blah,
        function_Bearer: function_Bearer
    };
})();
