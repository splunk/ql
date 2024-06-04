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
/******/ 		6: 0
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
/******/ 	deferredModules.push(["./package/src/main/webapp/pages/status/index.tsx",0]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./package/src/main/webapp/pages/status/Status.tsx":
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
var definition = __importStar(__webpack_require__("./package/src/main/webapp/pages/status/definition.json"));
var TelemetryConstants_1 = __webpack_require__("./package/src/main/webapp/constants/TelemetryConstants.ts");
var telemetryUtils_1 = __webpack_require__("./package/src/main/webapp/util/utils/telemetryUtils.ts");
var Status = (0, withTokens_1["default"])(Dashboard_1["default"]);
var DashboardStatus = function DashboardStatus() {
  (0, react_1.useEffect)(function () {
    // Send telemetry event
    var payload = {
      page: TelemetryConstants_1.META_STATUS
    };
    (0, telemetryUtils_1.sendTelemetryEvent)(TelemetryConstants_1.EVENT_PAGE_VIEWS, payload);
  }, []);
  return (0, jsx_runtime_1.jsx)(Status, {
    definition: definition,
    actionMenus: actions_1["default"]
  });
};
exports["default"] = DashboardStatus;

/***/ }),

/***/ "./package/src/main/webapp/pages/status/definition.json":
/***/ (function(module) {

module.exports = JSON.parse("{\"visualizations\":{\"viz_single_1\":{\"type\":\"splunk.singlevalue\",\"options\":{\"colorMode\":\"none\",\"drilldown\":\"none\",\"numberPrecision\":0,\"sparklineDisplay\":\"below\",\"trendDisplay\":\"absolute\",\"trellis.enabled\":0,\"trellis.scales.shared\":1,\"trellis.size\":\"medium\",\"underLabel\":\"Splunk app for lookup file editing REST handler\",\"unitPosition\":\"after\",\"shouldUseThousandSeparators\":true,\"majorColor\":\"#53a051\"},\"dataSources\":{\"primary\":\"ds_search_1\"}},\"viz_single_2\":{\"type\":\"splunk.singlevalue\",\"options\":{\"colorMode\":\"none\",\"drilldown\":\"none\",\"numberPrecision\":0,\"sparklineDisplay\":\"below\",\"trendDisplay\":\"absolute\",\"trellis.enabled\":0,\"trellis.scales.shared\":1,\"trellis.size\":\"medium\",\"underLabel\":\"Lookup backups REST handler\",\"unitPosition\":\"after\",\"shouldUseThousandSeparators\":true,\"backgroundColor\":\"> majorValue | rangeValue(backgroundColorEditorConfig)\",\"majorColor\":\"#53a051\",\"trendColor\":\"#000000\"},\"dataSources\":{\"primary\":\"ds_search_2\"},\"context\":{\"backgroundColorEditorConfig\":[{\"to\":20,\"value\":\"#D41F1F\"},{\"from\":20,\"to\":40,\"value\":\"#D94E17\"},{\"from\":40,\"to\":60,\"value\":\"#CBA700\"},{\"from\":60,\"to\":80,\"value\":\"#669922\"},{\"from\":80,\"value\":\"#118832\"}]}},\"viz_chart_1\":{\"type\":\"splunk.area\",\"dataSources\":{\"primary\":\"ds_search_3\"},\"title\":\"Splunk app for lookup file editing REST handler activity\",\"options\":{\"yAxisAbbreviation\":\"auto\",\"y2AxisAbbreviation\":\"auto\",\"showRoundedY2AxisLabels\":false,\"legendTruncation\":\"ellipsisMiddle\",\"showY2MajorGridLines\":true,\"xAxisLabelRotation\":0,\"xAxisTitleVisibility\":\"show\",\"yAxisTitleVisibility\":\"show\",\"y2AxisTitleVisibility\":\"show\",\"yAxisScale\":\"linear\",\"showOverlayY2Axis\":false,\"nullValueDisplay\":\"gaps\",\"dataValuesDisplay\":\"off\",\"stackMode\":\"auto\",\"showSplitSeries\":false,\"showIndependentYRanges\":false,\"legendMode\":\"standard\",\"legendDisplay\":\"right\",\"lineWidth\":2},\"context\":{}},\"viz_chart_2\":{\"type\":\"splunk.area\",\"dataSources\":{\"primary\":\"ds_search_4\"},\"title\":\"Lookup backups REST handler activity\",\"options\":{\"yAxisAbbreviation\":\"auto\",\"y2AxisAbbreviation\":\"auto\",\"showRoundedY2AxisLabels\":false,\"legendTruncation\":\"ellipsisMiddle\",\"showY2MajorGridLines\":true,\"xAxisLabelRotation\":0,\"xAxisTitleVisibility\":\"show\",\"yAxisTitleVisibility\":\"show\",\"y2AxisTitleVisibility\":\"show\",\"yAxisScale\":\"linear\",\"showOverlayY2Axis\":false,\"nullValueDisplay\":\"gaps\",\"dataValuesDisplay\":\"off\",\"stackMode\":\"auto\",\"showSplitSeries\":false,\"showIndependentYRanges\":false,\"legendMode\":\"standard\",\"legendDisplay\":\"right\",\"lineWidth\":2},\"context\":{}}},\"dataSources\":{\"ds_search_1\":{\"type\":\"ds.search\",\"options\":{\"query\":\"| stats count as value | eval value=\\\"Offline\\\" | append [rest /services/data/lookup_edit/ping | fields value] | stats last(value) as status | eval range=if(status==\\\"Offline\\\", \\\"severe\\\", \\\"low\\\")\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}}},\"ds_search_2\":{\"type\":\"ds.search\",\"options\":{\"query\":\"| stats count as value | eval value=\\\"Offline\\\" | append [rest /services/data/lookup_backup/ping | fields value] | stats last(value) as status | eval range=if(status==\\\"Offline\\\", \\\"severe\\\", \\\"low\\\")\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}}},\"ds_search_3\":{\"type\":\"ds.search\",\"options\":{\"query\":\"index=_internal sourcetype=lookup_editor_rest_handler | timechart count\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}}},\"ds_search_4\":{\"type\":\"ds.search\",\"options\":{\"query\":\"index=_internal sourcetype=lookup_backups_rest_handler | timechart count\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}}}},\"defaults\":{\"dataSources\":{\"ds.search\":{\"options\":{\"queryParameters\":{}}}}},\"inputs\":{},\"layout\":{\"type\":\"grid\",\"options\":{\"height\":500},\"structure\":[{\"item\":\"viz_single_1\",\"type\":\"block\",\"position\":{\"x\":0,\"y\":0,\"w\":600,\"h\":166}},{\"item\":\"viz_chart_1\",\"type\":\"block\",\"position\":{\"x\":0,\"y\":166,\"w\":600,\"h\":334}},{\"item\":\"viz_single_2\",\"type\":\"block\",\"position\":{\"x\":600,\"y\":0,\"w\":600,\"h\":166}},{\"item\":\"viz_chart_2\",\"type\":\"block\",\"position\":{\"x\":600,\"y\":166,\"w\":600,\"h\":334}}],\"globalInputs\":[]},\"description\":\"View the current status of the Splunk app for lookup file editing. The application will not work correctly if any REST handlers are offline. See Splunk documentation for troubleshooting steps.\",\"title\":\"Status\"}");

/***/ }),

/***/ "./package/src/main/webapp/pages/status/index.tsx":
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
var Status_1 = __importDefault(__webpack_require__("./package/src/main/webapp/pages/status/Status.tsx"));
(0, pageLoader_1["default"])(Status_1["default"], {
  pageTitle: (0, i18n_1._)('Status'),
  showPageTitle: true,
  pageTitleBorder: true
});

/***/ })

/******/ });