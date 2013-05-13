
/* === JSON === */
(function(){
  if (!this.JSON) {
    this.JSON = (function() {
      var re = {
        obj: /^\{"[\w\W.]*\}$/,
        arr: /^\[[\w\W.]*\]$/,
        triml: /^\s+/,
        trimr: /\s+$/,
        quote: /^"[\w\W.]*"$/
      }, 
      trim = function(str) {
        return str.replace(re.triml, '').replace(re.trimr, '');
      }, 
      getValue = function(v) {
        return (!isNaN(+v) ? +v : re.obj.test(v) || re.arr.test(v) ? parse(v) :
          v == 'true' ? true : v == 'false' ? false : v == 'null' ? null : v == 'undefined' ? undefined :
          re.quote.test(v) ? v.slice(1, -1) : v
        );
      },
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
          }
          else {
            v = trim(tuple);
            obj.push(getValue(v));
          }
        }
        return obj;
      },
      stringify = function(obj) {
        var isObj, str, len, k, v;
        if (obj != null && obj.toJSON && typeof obj.toJSON === 'function') return obj.toJSON();
        if (typeof obj === 'string') return '"' + obj.replace('"', '\"') + '"';
        if (!(typeof obj === 'object' && obj != undefined || typeof obj === 'array')) return '' + obj;
        isObj = typeof obj == 'object' && !(obj.length && obj.push && obj.slice);
        if (isObj) {
          str = '{'
          for (k in obj) {
            v = obj[k];
            if (v === obj) continue;
            str += '"' + k + '":' + stringify(v) + ',';
          }
        }
        else {
          str = '['
          len = obj.length;
          for (k = 0; k < len; k++) {
            v = obj[k];
            str += stringify(v) + ',';
          }
        }
        str = str.slice(0, -1);
        return (str += isObj ? '}' : ']', str);
      };
      return {
        parse: parse,
        stringify: stringify
      };
    })();
  }
}).call(this);
