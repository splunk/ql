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
/******/ 		5: 0
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
/******/ 	deferredModules.push(["./package/src/main/webapp/pages/overview/index.tsx",0]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./package/src/main/webapp/pages/overview/Overview.tsx":
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
var withTokens_1 = __importDefault(__webpack_require__("./package/src/main/webapp/components/shared/hoc/withTokens.tsx"));
var Dashboard_1 = __importDefault(__webpack_require__("./package/src/main/webapp/components/shared/Dashboard.tsx"));
var actions_1 = __importDefault(__webpack_require__("./package/src/main/webapp/components/shared/actions.jsx"));
var definition = __importStar(__webpack_require__("./package/src/main/webapp/pages/overview/definition.json"));
var TelemetryConstants_1 = __webpack_require__("./package/src/main/webapp/constants/TelemetryConstants.ts");
var telemetryUtils_1 = __webpack_require__("./package/src/main/webapp/util/utils/telemetryUtils.ts");
var Overview = (0, withTokens_1["default"])(Dashboard_1["default"]);
var DashboardOverview = function DashboardOverview() {
  (0, react_1.useEffect)(function () {
    // Send telemetry event
    var payload = {
      page: TelemetryConstants_1.META_OVERVIEW
    };
    (0, telemetryUtils_1.sendTelemetryEvent)(TelemetryConstants_1.EVENT_PAGE_VIEWS, payload);
  }, []);
  return (0, jsx_runtime_1.jsx)(Overview, {
    definition: definition,
    actionMenus: actions_1["default"]
  });
};
exports["default"] = DashboardOverview;

/***/ }),

/***/ "./package/src/main/webapp/pages/overview/definition.json":
/***/ (function(module) {

module.exports = JSON.parse("{\"visualizations\":{\"viz_singleview_1\":{\"type\":\"splunk.singlevalue\",\"title\":\"Lookup files\",\"description\":\"Total lookup files available with monthly trend\",\"dataSources\":{\"primary\":\"ds_total_lookups\"},\"options\":{\"majorColor\":\"#000000\",\"trendColor\":\"#dc4e41\",\"sparklineDisplay\":\"off\"},\"showProgressBar\":true},\"viz_singleview_2\":{\"type\":\"splunk.singlevalue\",\"title\":\"CSV lookup files\",\"description\":\"Total CSV lookup files available with monthly trend\",\"dataSources\":{\"primary\":\"ds_count_csv_lookups\"},\"options\":{\"sparklineDisplay\":\"off\",\"majorColor\":\"#000000\",\"trendColor\":\"#dc4e41\"},\"showProgressBar\":true},\"viz_singleview_3\":{\"type\":\"splunk.singlevalue\",\"title\":\"KV Store lookup files\",\"description\":\"Total KV store lookup files available with monthly trend\",\"dataSources\":{\"primary\":\"ds_count_kv_lookups\"},\"options\":{\"sparklineDisplay\":\"off\",\"majorColor\":\"#000000\",\"trendColor\":\"#dc4e41\"},\"showProgressBar\":true},\"viz_singleview_4\":{\"type\":\"splunk.singlevalue\",\"title\":\"CSV lookup backups\",\"description\":\"Count of CSV lookups that have at least one backup\",\"dataSources\":{\"primary\":\"ds_csv_backup_count\"},\"options\":{\"sparklineDisplay\":\"off\",\"trendColor\":\"> trendValue | rangeValue(trendColorEditorConfig)\"},\"context\":{\"trendColorEditorConfig\":[{\"value\":\"#1c6b2d\",\"to\":0},{\"value\":\"#333022\",\"from\":0,\"to\":0.99},{\"value\":\"#d41f1f\",\"from\":0.99}]},\"showProgressBar\":true},\"viz_singleview_5\":{\"type\":\"splunk.singlevalue\",\"title\":\"CSV lookup file size\",\"description\":\"Total lookup files size with daily trend\",\"dataSources\":{\"primary\":\"ds_total_csv_size\"},\"options\":{\"unit\":\"$unit_token$\",\"numberPrecision\":3,\"trendColor\":\"> trendValue | rangeValue(trendColorEditorConfig)\",\"sparklineDisplay\":\"off\",\"majorValue\":\"> sparklineValues | lastPoint()\",\"trendValue\":\"> sparklineValues | delta(-2)\",\"sparklineValues\":\"> primary | seriesByName('total_size')\"},\"context\":{\"trendColorEditorConfig\":[{\"value\":\"#1c6b2d\",\"to\":0},{\"value\":\"#333022\",\"from\":0,\"to\":0.01},{\"value\":\"#d41f1f\",\"from\":0.01}]},\"showProgressBar\":true},\"viz_singleview_6\":{\"type\":\"splunk.singlevalue\",\"title\":\"Backup size\",\"description\":\"Total CSV lookup file backup size with daily trend\",\"dataSources\":{\"primary\":\"ds_backup_daily_trend\"},\"options\":{\"sparklineDisplay\":\"off\",\"unit\":\"$unit_token$\",\"numberPrecision\":3,\"trendColor\":\"> trendValue | rangeValue(trendColorEditorConfig)\"},\"context\":{\"trendColorEditorConfig\":[{\"value\":\"#1c6b2d\",\"to\":0},{\"value\":\"#333022\",\"from\":0,\"to\":0.01},{\"value\":\"#d41f1f\",\"from\":0.01}]},\"showProgressBar\":true},\"viz_table_1\":{\"type\":\"splunk.table\",\"title\":\"Large CSV lookups by size\",\"description\":\"(Top 20)\",\"dataSources\":{\"primary\":\"ds_large_csv_lookups\"},\"options\":{\"columnFormat\":{\"evaldate\":{\"data\":\"> table | seriesByName(\\\"evaldate\\\") | formatByType(evaldateColumnFormatEditorConfig)\"},\"date\":{\"data\":\"> table | seriesByName(\\\"date\\\") | formatByType(dateColumnFormatEditorConfig)\"},\"Created Date\":{\"data\":\"> table | seriesByName(\\\"Created Date\\\") | formatByType(Created_DateColumnFormatEditorConfig)\"},\"Created date\":{\"data\":\"> table | seriesByName(\\\"Created date\\\") | formatByType(Created_dateColumnFormatEditorConfig)\"}},\"tableFormat\":{\"rowBackgroundColors\":\"> table | seriesByIndex(0) | pick(tableAltRowBackgroundColorsByTheme)\"},\"showInternalFields\":false},\"context\":{\"evaldateColumnFormatEditorConfig\":{\"time\":{\"format\":\"YYYY-MM-DD\"}},\"dateColumnFormatEditorConfig\":{\"time\":{\"format\":\"YYYY-MM-DD\"}},\"Created_DateColumnFormatEditorConfig\":{\"time\":{\"format\":\"MM-DD-YYYY\"}},\"Created_dateColumnFormatEditorConfig\":{\"time\":{\"format\":\"YYYY-DD-MM\"}}},\"eventHandlers\":[{\"type\":\"drilldown.customUrl\",\"options\":{\"url\":\"$ds_root_endpoint:result.value$/app/lookup_editor/lookup_edit?owner=$row.Owner.value|u$&namespace=$row.App.value|u$&lookup=$row.Lookup name.value|u$&type=csv&transform=\",\"newTab\":true}}],\"showProgressBar\":true},\"viz_table_2\":{\"type\":\"splunk.table\",\"title\":\"Large CSV backups by size\",\"description\":\"(Top 20)\",\"dataSources\":{\"primary\":\"ds_large_csv_backups\"},\"options\":{\"columnFormat\":{\"backup_date\":{\"data\":\"> table | seriesByName(\\\"backup_date\\\") | formatByType(backup_dateColumnFormatEditorConfig)\"},\"Backup Date\":{\"data\":\"> table | seriesByName(\\\"Backup Date\\\") | formatByType(Backup_DateColumnFormatEditorConfig)\"},\"Backup date\":{\"data\":\"> table | seriesByName(\\\"Backup date\\\") | formatByType(Backup_dateColumnFormatEditorConfig)\"}}},\"context\":{\"backup_dateColumnFormatEditorConfig\":{\"time\":{\"format\":\"YYYY-MM-DD\"}},\"Backup_DateColumnFormatEditorConfig\":{\"time\":{\"format\":\"MM-DD-YYYY\"}},\"Backup_dateColumnFormatEditorConfig\":{\"time\":{\"format\":\"YYYY-DD-MM\"}}},\"eventHandlers\":[{\"type\":\"drilldown.customUrl\",\"options\":{\"url\":\"$ds_root_endpoint:result.value$/app/lookup_editor/lookup_edit?owner=$row.Owner.value|u$&namespace=$row.App.value|u$&lookup=$row.Lookup name.value|u$&type=csv&transform=\",\"newTab\":true}}],\"showProgressBar\":true}},\"dataSources\":{\"ds_count_kv_lookups\":{\"type\":\"ds.search\",\"options\":{\"query\":\"| rest /servicesNS/nobody/-/storage/collections/config \\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\") \\n| where calc_date <= end\\n| stats count as total\\n| append [\\n| rest /servicesNS/nobody/-/storage/collections/config \\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\")\\n| stats count as total\\n]\\n| fields _time total\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}},\"name\":\"ds_count_kv_lookups\"},\"ds_count_csv_lookups\":{\"type\":\"ds.search\",\"options\":{\"query\":\"| rest /servicesNS/nobody/-/data/lookup-table-files \\n| where title like \\\"%.csv\\\"\\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\") \\n| where calc_date <= end\\n| stats count as total\\n| append [\\n| rest /servicesNS/nobody/-/data/lookup-table-files \\n| where title like \\\"%.csv\\\"\\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\")\\n| stats count as total\\n]\\n| fields _time total\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}},\"name\":\"ds_count_csv_lookups\"},\"ds_total_lookups\":{\"type\":\"ds.search\",\"options\":{\"query\":\"| rest /servicesNS/nobody/-/data/lookup-table-files \\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\") \\n| where calc_date <= end\\n| stats count as total\\n| append [\\n| rest /servicesNS/nobody/-/storage/collections/config \\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\") \\n| where calc_date <= end\\n| stats count as total\\n]\\n| stats sum(total) AS total\\n| append [\\n| rest /servicesNS/nobody/-/data/lookup-table-files \\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\")\\n| stats count as total\\n| append [\\n| rest /servicesNS/nobody/-/storage/collections/config \\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| eval eval_date=if(like(updated,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", updated) \\n| eval calc_date = strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\")\\n| stats count as total\\n]\\n| stats sum(total) as total\\n]\\n| fields _time total\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}},\"name\":\"ds_total_lookups\"},\"ds_search_base\":{\"type\":\"ds.search\",\"options\":{\"query\":\"| lookupdetails\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}},\"name\":\"ds_base_search\"},\"ds_large_csv_backups\":{\"type\":\"ds.chain\",\"options\":{\"query\":\"| sort limit=20 -backup_size \\n| eval size=case( \\n    backup_size>=(1024*1024*1024*1024),round(backup_size/(1024*1024*1024*1024),0).\\\" TB\\\",\\n    backup_size>=(1024*1024*1024),round(backup_size/(1024*1024*1024),0).\\\" GB\\\",\\n    backup_size>=(1024*1024),round(backup_size/(1024*1024),2).\\\" MB\\\",\\nbackup_size>=1024,round(backup_size/1024,0).\\\" KB\\\",\\n1=1,backup_size.\\\" B\\\")\\n| eval backup_date = strftime(recent_backup,\\\"%Y-%m-%d %H:%M:%S\\\")\\n|  where backup_date!=\\\"\\\"\\n| rename name as \\\"Lookup name\\\" size as \\\"Backup size\\\" backup_date as \\\"Backup date\\\" app as \\\"App\\\" endpoint_owner as \\\"Owner\\\"\\n| fields \\\"Lookup name\\\" \\\"Backup size\\\" \\\"Backup date\\\" \\\"App\\\" \\\"Owner\\\"\",\"extend\":\"ds_search_base\"},\"name\":\"ds_large_csv_backups\"},\"ds_large_csv_lookups\":{\"type\":\"ds.chain\",\"options\":{\"extend\":\"ds_base_lookup\",\"query\":\"| sort limit=20 -size \\n| eval lookup_size=case( \\n    size>=(1024*1024*1024*1024),round(size/(1024*1024*1024*1024),2).\\\" TB\\\",\\n    size>=(1024*1024*1024),round(size/(1024*1024*1024),2).\\\" GB\\\",\\n    size>=(1024*1024),round(size/(1024*1024),2).\\\" MB\\\", \\n    size>=1024,round(size/1024,2).\\\" KB\\\", \\n    1=1,size.\\\" B\\\")\\n| rename name as \\\"Lookup name\\\" lookup_size as \\\"Lookup size\\\" date as \\\"Created date\\\" namespace as \\\"App\\\" endpoint_owner as \\\"Owner\\\"\\n| fields \\\"Lookup name\\\" \\\"Lookup size\\\" \\\"Created date\\\" \\\"App\\\" \\\"Owner\\\"\"},\"name\":\"ds_large_csv_lookups\"},\"ds_base_lookup\":{\"type\":\"ds.search\",\"options\":{\"query\":\"| lookupinfo\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}},\"name\":\"ds_lookup_base\"},\"ds_total_csv_size\":{\"type\":\"ds.chain\",\"options\":{\"extend\":\"ds_base_lookup\",\"query\":\"| eval start = now()\\n| eval end=start - 86400\\n| eval eval_date=if(like(date,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", date)\\n| eval start_date = strftime(start,\\\"%Y-%m-%d %H:%M:%S\\\")\\n| eval end_date = strftime(end,\\\"%Y-%m-%d %H:%M:%S\\\")\\n| eval mytime=strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\")\\n| where mytime <= end\\n| stats sum(size) as total\\n| eval sizeMB=round(total/(1024*1024), 8)\\n| eval sizeGB=round(total/(1024*1024*1024), 8)\\n| eval unit=\\\"$unit_token$\\\"\\n| eval total_size=if(unit=\\\"MB\\\",sizeMB,sizeGB)\\n| append [\\n| lookupinfo\\n| eval start = now()\\n| eval end=start - 86400\\n| eval eval_date=if(like(date,\\\"1970-01-01T%\\\"), \\\"1971-01-01T05:30:00+05:30\\\", date)\\n| eval start_date = strftime(start,\\\"%Y-%m-%d %H:%M:%S\\\")\\n| eval end_date = strftime(end,\\\"%Y-%m-%d %H:%M:%S\\\")\\n| eval mytime=strptime(eval_date,\\\"%Y-%m-%dT%H:%M:%S.%Q\\\")\\n| stats sum(size) as total\\n| eval sizeMB=round(total/(1024*1024), 8)\\n| eval sizeGB=round(total/(1024*1024*1024), 8)\\n| eval unit=\\\"$unit_token$\\\"\\n| eval total_size=if(unit=\\\"MB\\\",sizeMB,sizeGB)\\n]\\n| fields _time total_size unit\",\"enableSmartSources\":true},\"name\":\"ds_total_csv_size\"},\"ds_csv_backup_count\":{\"type\":\"ds.chain\",\"options\":{\"extend\":\"ds_search_base\",\"query\":\"| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| where backup_size>0 AND eval_date<=end\\n| stats count as total\\n| append[\\n| lookupdetails\\n| eval start = now() | eval end=relative_time(now(), \\\"-1mon@d\\\")\\n| where backup_size>0\\n| stats count as total\\n]\\n| fields _time total\"},\"name\":\"ds_csv_backup_count\"},\"ds_backup_daily_trend\":{\"type\":\"ds.search\",\"options\":{\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"},\"query\":\"| lookupdailybackup \\n| stats sum(daily_backup) as total\\n| eval sizeMB=round(total/(1024*1024), 8)\\n| eval sizeGB=round(total/(1024*1024*1024), 8)\\n| eval unit=\\\"$unit_token$\\\"\\n| eval total_size=if(unit=\\\"MB\\\",sizeMB,sizeGB)\\n| append [\\n| lookupdetails\\n| eval start = now() | eval end=start - 86400\\n| eval start_date = strftime(start,\\\"%Y-%m-%d %H:%M:%S\\\")\\n| eval end_date = strftime(end,\\\"%Y-%m-%d %H:%M:%S\\\")\\n| stats sum(backup_size) as total\\n| eval sizeMB=round(total/(1024*1024), 8)\\n| eval sizeGB=round(total/(1024*1024*1024), 8)\\n| eval unit=\\\"$unit_token$\\\"\\n| eval total_size=if(unit=\\\"MB\\\",sizeMB,sizeGB)\\n]\\n| fields _time unit total_size\",\"enableSmartSources\":true},\"name\":\"ds_backup_daily_trend\"},\"ds_root_endpoint\":{\"type\":\"ds.search\",\"options\":{\"enableSmartSources\":true,\"query\":\"| rest /services/properties/web/settings/root_endpoint \\n|  fields value\",\"queryParameters\":{\"earliest\":\"-24h@h\",\"latest\":\"now\"}},\"name\":\"ds_root_endpoint\"}},\"defaults\":{\"dataSources\":{\"ds.search\":{\"options\":{\"queryParameters\":{\"latest\":\"$global_time.latest$\",\"earliest\":\"$global_time.earliest$\"}}}}},\"inputs\":{\"input_unit\":{\"options\":{\"items\":[{\"label\":\"MB\",\"value\":\"MB\"},{\"label\":\"GB\",\"value\":\"GB\"}],\"token\":\"unit_token\",\"defaultValue\":\"MB\"},\"title\":\"Size unit set to\",\"type\":\"input.dropdown\"}},\"layout\":{\"type\":\"grid\",\"options\":{},\"structure\":[{\"item\":\"viz_singleview_1\",\"type\":\"block\",\"position\":{\"x\":0,\"y\":0,\"w\":300,\"h\":200}},{\"item\":\"viz_singleview_5\",\"type\":\"block\",\"position\":{\"x\":0,\"y\":200,\"w\":600,\"h\":200}},{\"item\":\"viz_table_1\",\"type\":\"block\",\"position\":{\"x\":0,\"y\":400,\"w\":600,\"h\":500}},{\"item\":\"viz_singleview_2\",\"type\":\"block\",\"position\":{\"x\":300,\"y\":0,\"w\":300,\"h\":200}},{\"item\":\"viz_singleview_3\",\"type\":\"block\",\"position\":{\"x\":600,\"y\":0,\"w\":300,\"h\":200}},{\"item\":\"viz_singleview_6\",\"type\":\"block\",\"position\":{\"x\":600,\"y\":200,\"w\":600,\"h\":200}},{\"item\":\"viz_table_2\",\"type\":\"block\",\"position\":{\"x\":600,\"y\":400,\"w\":600,\"h\":500}},{\"item\":\"viz_singleview_4\",\"type\":\"block\",\"position\":{\"x\":900,\"y\":0,\"w\":300,\"h\":200}}],\"globalInputs\":[\"input_unit\"]},\"description\":\"\",\"title\":\"Overview\"}");

/***/ }),

/***/ "./package/src/main/webapp/pages/overview/index.tsx":
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
var Overview_1 = __importDefault(__webpack_require__("./package/src/main/webapp/pages/overview/Overview.tsx"));
(0, pageLoader_1["default"])(Overview_1["default"], {
  pageTitle: (0, i18n_1._)('Overview'),
  showPageTitle: true,
  pageTitleBorder: true
});

/***/ })

/******/ });