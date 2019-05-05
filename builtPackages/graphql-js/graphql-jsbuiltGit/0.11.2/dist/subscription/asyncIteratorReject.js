'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = asyncIteratorReject;

var _iterall = require('iterall');

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; } /**
                                                                                                                                                                                                                   * Copyright (c) 2017, Facebook, Inc.
                                                                                                                                                                                                                   * All rights reserved.
                                                                                                                                                                                                                   *
                                                                                                                                                                                                                   * This source code is licensed under the BSD-style license found in the
                                                                                                                                                                                                                   * LICENSE file in the root directory of this source tree. An additional grant
                                                                                                                                                                                                                   * of patent rights can be found in the PATENTS file in the same directory.
                                                                                                                                                                                                                   *
                                                                                                                                                                                                                   * 
                                                                                                                                                                                                                   */

/**
 * Given an error, returns an AsyncIterable which will fail with that error.
 *
 * Similar to Promise.reject(error)
 */
function asyncIteratorReject(error) {
  var isComplete = false;
  return _defineProperty({
    next: function next() {
      var result = isComplete ? Promise.resolve({ value: undefined, done: true }) : Promise.reject(error);
      isComplete = true;
      return result;
    },
    return: function _return() {
      isComplete = true;
      return Promise.resolve({ value: undefined, done: true });
    },
    throw: function _throw() {
      isComplete = true;
      return Promise.reject(error);
    }
  }, _iterall.$$asyncIterator, function () {
    return this;
  });
}