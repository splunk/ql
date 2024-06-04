/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(Object.prototype.hasOwnProperty.call(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		1: 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// script path function
/******/ 	function jsonpScriptSrc(chunkId) {
/******/ 		return __webpack_require__.p + "components/pages/" + ({}[chunkId]||chunkId) + ".js"
/******/ 	}
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/ 	// The chunk loading function for additional chunks
/******/ 	// Since all referenced chunks are already included
/******/ 	// in this file, this function is empty here.
/******/ 	__webpack_require__.e = function requireEnsure() {
/******/ 		return Promise.resolve();
/******/ 	};
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// on error function for async loading
/******/ 	__webpack_require__.oe = function(err) { console.error(err); throw err; };
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push(["./package/src/main/webapp/pages/logs/index.tsx",0]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./package/src/main/webapp/pages/logs/Logs.tsx":
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var __createBinding = this && this.__createBinding || (Object.create ? function (o, m, k, k2) {
  if (k2 === undefined) k2 = k;
  var desc = Object.getOwnPropertyDescriptor(m, k);
  if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
    desc = {
      enumerable: true,
      get: function get() {
        return m[k];
      }
    };
  }
  Object.defineProperty(o, k2, desc);
} : function (o, m, k, k2) {
  if (k2 === undefined) k2 = k;
  o[k2] = m[k];
});
var __setModuleDefault = this && this.__setModuleDefault || (Object.create ? function (o, v) {
  Object.defineProperty(o, "default", {
    enumerable: true,
    value: v
  });
} : function (o, v) {
  o["default"] = v;
});
var __importStar = this && this.__importStar || function (mod) {
  if (mod && mod.__esModule) return mod;
  var result = {};
  if (mod != null) for (var k in mod) {
    if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
  }
  __setModuleDefault(result, mod);
  return result;
};
var __importDefault = this && this.__importDefault || function (mod) {
  return mod && mod.__esModule ? mod : {
    "default": mod
  };
};
Object.defineProperty(exports, "__esModule", {
  value: true
});
var jsx_runtime_1 = __webpack_require__("./node_modules/react/jsx-runtime.js");
var react_1 = __webpack_require__("./node_modules/react/index.js");
// import { SWACollector } from "@splunk/dashboard-telemetry";
var withTokens_1 = __importDefault(__webpack_require__("./package/src/main/webapp/components/shared/hoc/withTokens.tsx"));
var Dashboard_1 = __importDefault(__webpack_require__("./package/src/main/webapp/components/shared/Dashboard.tsx"));
var actions_1 = __importDefault(__webpack_require__("./package/src/main/webapp/components/shared/actions.jsx"));
var TelemetryConstants_1 = __webpack_require__("./package/src/main/webapp/constants/TelemetryConstants.ts");
var telemetryUtils_1 = __webpack_require__("./package/src/main/webapp/util/utils/telemetryUtils.ts");
var definition = __importStar(__webpack_require__("./package/src/main/webapp/pages/logs/definition.json"));
var Logs = (0, withTokens_1["default"])(Dashboard_1["default"]);
var DashboardLogs = function DashboardLogs() {
  (0, react_1.useEffect)(function () {
    // Send telemetry event
    var payload = {
      page: TelemetryConstants_1.META_LOGS
    };
    (0, telemetryUtils_1.sendTelemetryEvent)(TelemetryConstants_1.EVENT_PAGE_VIEWS, payload);
  }, []);
  return (0, jsx_runtime_1.jsx)(Logs, {
    definition: definition,
    actionMenus: actions_1["default"]
  });
};
exports["default"] = DashboardLogs;

/***/ }),

/***/ "./package/src/main/webapp/pages/logs/definition.json":
/***/ (function(module) {

module.exports = JSON.parse("{\"visualizations\":{\"viz_chart_1\":{\"type\":\"splunk.area\",\"dataSources\":{\"primary\":\"ds_search_1\"},\"title\":\"Logs by severity (over time)\",\"options\":{\"yAxisAbbreviation\":\"off\",\"y2AxisAbbreviation\":\"off\",\"showRoundedY2AxisLabels\":false,\"legendTruncation\":\"ellipsisMiddle\",\"showY2MajorGridLines\":true,\"stackMode\":\"stacked\",\"legendLabels\":[\"DEBUG\",\"INFO\",\"WARNING\",\"ERROR\",\"CRITICAL\"],\"seriesColors\":[\"0xb2d16d\",\"0x6ab7c8\",\"0xfac61c\",\"0xf8912c\",\"0xd85d3d\"]},\"context\":{},\"eventHandlers\":[]},\"viz_table_1\":{\"type\":\"splunk.table\",\"options\":{\"wrap\":true,\"rowNumbers\":false,\"dataOverlayMode\":\"none\",\"drilldown\":\"cell\",\"count\":10},\"dataSources\":{\"primary\":\"ds_search_2\"},\"title\":\"Logs by severity\",\"eventHandlers\":[{\"type\":\"drilldown.customUrl\",\"options\":{\"url\":\"$ds_root_endpoint:result.value$/app/search/search?q=index=_internal (sourcetype=lookup_editor_rest_handler OR sourcetype=lookup_backups_rest_handler) | rex field=_raw \\\"(%3F<severity>(DEBUG)|(ERROR)|(WARNING)|(INFO)|(CRITICAL)) (%3F<message>.*)\\\" | search severity=$row.severity.value|u$\",\"newTab\":true}}]},\"viz_table_2\":{\"type\":\"splunk.table\",\"options\":{\"wrap\":true,\"rowNumbers\":false,\"dataOverlayMode\":\"none\",\"drilldown\":\"cell\",\"count\":10},\"dataSources\":{\"primary\":\"ds_search_3\"},\"eventHandlers\":[{\"type\":\"drilldown.customUrl\",\"options\":{\"url\":\"$ds_root_endpoint:result.value$/app/search/search?q=index=_internal (sourcetype=lookup_editor_rest_handler OR sourcetype=lookup_backups_rest_handler) $ds_tokens:result.severity_token$\",\"newTab\":true}}],\"title\":\"Latest logs\"}},\"dataSources\":{\"ds_search_1\":{\"type\":\"ds.search\",\"options\":{\"query\":\"index=_internal (sourcetype=lookup_editor_rest_handler OR sourcetype=lookup_backups_rest_handler) $ds_tokens:result.severity_token$ | rex field=_raw \\\"(?<severity>(DEBUG)|(ERROR)|(WARNING)|(INFO)|(CRITICAL)) (?<message>.*)\\\" | fillnull severity value=\\\"UNDEFINED\\\" | timechart count(severity) as count by severity\",\"queryParameters\":{\"earliest\":\"$field1.earliest$\",\"latest\":\"$field1.latest$\"}},\"name\":\"ds_search_1\"},\"ds_search_2\":{\"type\":\"ds.search\",\"options\":{\"query\":\"index=_internal (sourcetype=lookup_editor_rest_handler OR sourcetype=lookup_backups_rest_handler) | rex field=_raw \\\"(?<severity>(DEBUG)|(ERROR)|(WARNING)|(INFO)|(CRITICAL)) (?<message>.*)\\\" | fillnull value=\\\"undefined\\\" vendor_severity | stats sparkline count by severity | sort -count\",\"queryParameters\":{\"earliest\":\"$field1.earliest$\",\"latest\":\"$field1.latest$\"}},\"name\":\"ds_search_2\"},\"ds_search_3\":{\"type\":\"ds.search\",\"options\":{\"query\":\"index=_internal (sourcetype=lookup_editor_rest_handler OR sourcetype=lookup_backups_rest_handler) $ds_tokens:result.severity_token$\\n          | rex field=_raw \\\"(?<severity>(DEBUG)|(ERROR)|(WARNING)|(INFO)|(CRITICAL)) (?<message>.*)\\\"\\n          | sort -_time\\n          | eval time=_time\\n          | convert ctime(time)\\n          | table time severity message\",\"queryParameters\":{\"earliest\":\"$field1.earliest$\",\"latest\":\"$field1.latest$\"}},\"name\":\"ds_search_3\"},\"ds_tokens\":{\"type\":\"ds.search\",\"options\":{\"queryParameters\":{\"earliest\":\"$field1.earliest$\",\"latest\":\"$field1.latest$\"},\"query\":\"| makeresults count=1\\n| eval severity_input=\\\"$severity$\\\"\\n| eval list=split(severity_input,\\\",\\\")\\n| eval filterlist=mvfilter(!list IN (\\\"*\\\"))\\n| eval fields=\\\"\\\".mvjoin(mvmap(filterlist,\\\"\\\" . filterlist . \\\"\\\"), \\\" OR \\\").\\\"\\\"\\n| eval severity_token=case(severity_input==\\\"\\\",\\\"\\\", true(), fields)\",\"enableSmartSources\":true},\"name\":\"ds_tokens\"},\"ds_root_endpoint\":{\"type\":\"ds.search\",\"options\":{\"enableSmartSources\":true,\"query\":\"| rest /services/properties/web/settings/root_endpoint \\n|  fields value\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}},\"name\":\"ds_root_endpoint\"}},\"defaults\":{\"dataSources\":{\"ds.search\":{\"options\":{\"queryParameters\":{}}}}},\"inputs\":{\"input_1\":{\"type\":\"input.timerange\",\"title\":\"\",\"options\":{\"token\":\"field1\",\"defaultValue\":\"-24h@h,now\"}},\"input_2\":{\"options\":{\"items\":[{\"label\":\"All\",\"value\":\"DEBUG OR INFO OR WARNING OR ERROR OR CRITICAL\"},{\"label\":\"Debug\",\"value\":\"DEBUG\"},{\"label\":\"Informational\",\"value\":\"INFO\"},{\"label\":\"Warning\",\"value\":\"WARNING\"},{\"label\":\"Error\",\"value\":\"ERROR\"},{\"label\":\"Critical\",\"value\":\"CRITICAL\"}],\"defaultValue\":[\"DEBUG OR INFO OR WARNING OR ERROR OR CRITICAL\"],\"token\":\"severity\"},\"title\":\"Severity\",\"type\":\"input.multiselect\"}},\"layout\":{\"type\":\"grid\",\"options\":{\"submitButton\":true,\"height\":500},\"structure\":[{\"item\":\"viz_chart_1\",\"type\":\"block\",\"position\":{\"x\":0,\"y\":0,\"w\":600,\"h\":250}},{\"item\":\"viz_table_2\",\"type\":\"block\",\"position\":{\"x\":0,\"y\":250,\"w\":1200,\"h\":460}},{\"item\":\"viz_table_1\",\"type\":\"block\",\"position\":{\"x\":600,\"y\":0,\"w\":600,\"h\":250}}],\"globalInputs\":[\"input_1\",\"input_2\"]},\"description\":\"\",\"title\":\"Logs\"}");

/***/ }),

/***/ "./package/src/main/webapp/pages/logs/index.tsx":
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var __importDefault = this && this.__importDefault || function (mod) {
  return mod && mod.__esModule ? mod : {
    "default": mod
  };
};
Object.defineProperty(exports, "__esModule", {
  value: true
});
var pageLoader_1 = __importDefault(__webpack_require__("./package/src/main/webapp/util/pageLoader.tsx"));
var i18n_1 = __webpack_require__("./node_modules/@splunk/ui-utils/i18n.js");
var Logs_1 = __importDefault(__webpack_require__("./package/src/main/webapp/pages/logs/Logs.tsx"));
(0, pageLoader_1["default"])(Logs_1["default"], {
  pageTitle: (0, i18n_1._)('Logs'),
  showPageTitle: true,
  pageTitleBorder: true
});

/***/ })

/******/ });