'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.createSourceEventStream = undefined;

/**
 * Implements the "CreateSourceEventStream" algorithm described in the
 * GraphQL specification, resolving the subscription source event stream.
 *
 * Returns a Promise<AsyncIterable>.
 *
 * If the client-provided invalid arguments, the source stream could not be
 * created, or the resolver did not return an AsyncIterable, this function will
 * will throw an error, which should be caught and handled by the caller.
 *
 * A Source Event Stream represents a sequence of events, each of which triggers
 * a GraphQL execution for that event.
 *
 * This may be useful when hosting the stateful subscription service in a
 * different process or machine than the stateless GraphQL execution engine,
 * or otherwise separating these two steps. For more on this, see the
 * "Supporting Subscriptions at Scale" information in the GraphQL specification.
 */
var createSourceEventStream = exports.createSourceEventStream = function () {
  var _ref = _asyncToGenerator(regeneratorRuntime.mark(function _callee(schema, document, rootValue, contextValue, variableValues, operationName, fieldResolver) {
    var exeContext, type, fields, responseNames, responseName, fieldNodes, fieldNode, fieldDef, resolveFn, path, info, subscription;
    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            // If arguments are missing or incorrectly typed, this is an internal
            // developer mistake which should throw an early error.
            (0, _execute.assertValidExecutionArguments)(schema, document, variableValues);

            // If a valid context cannot be created due to incorrect arguments,
            // this will throw an error.
            exeContext = (0, _execute.buildExecutionContext)(schema, document, rootValue, contextValue, variableValues, operationName, fieldResolver);
            type = (0, _execute.getOperationRootType)(schema, exeContext.operation);
            fields = (0, _execute.collectFields)(exeContext, type, exeContext.operation.selectionSet, Object.create(null), Object.create(null));
            responseNames = Object.keys(fields);
            responseName = responseNames[0];
            fieldNodes = fields[responseName];
            fieldNode = fieldNodes[0];
            fieldDef = (0, _execute.getFieldDef)(schema, type, fieldNode.name.value);

            !fieldDef ? (0, _invariant2.default)(0, 'This subscription is not defined by the schema.') : void 0;

            // Call the `subscribe()` resolver or the default resolver to produce an
            // AsyncIterable yielding raw payloads.
            resolveFn = fieldDef.subscribe || exeContext.fieldResolver;
            path = (0, _execute.addPath)(undefined, responseName);
            info = (0, _execute.buildResolveInfo)(exeContext, fieldDef, fieldNodes, type, path);

            // resolveFieldValueOrError implements the "ResolveFieldEventStream"
            // algorithm from GraphQL specification. It differs from
            // "ResolveFieldValue" due to providing a different `resolveFn`.

            _context.next = 15;
            return (0, _execute.resolveFieldValueOrError)(exeContext, fieldDef, fieldNodes, resolveFn, rootValue, info);

          case 15:
            subscription = _context.sent;

            if (!(subscription instanceof Error)) {
              _context.next = 18;
              break;
            }

            throw (0, _locatedError.locatedError)(subscription, fieldNodes, (0, _execute.responsePathAsArray)(path));

          case 18:
            if ((0, _iterall.isAsyncIterable)(subscription)) {
              _context.next = 20;
              break;
            }

            throw new Error('Subscription must return Async Iterable. ' + 'Received: ' + String(subscription));

          case 20:
            return _context.abrupt('return', subscription);

          case 21:
          case 'end':
            return _context.stop();
        }
      }
    }, _callee, this);
  }));

  return function createSourceEventStream(_x, _x2, _x3, _x4, _x5, _x6, _x7) {
    return _ref.apply(this, arguments);
  };
}();

exports.subscribe = subscribe;

var _iterall = require('iterall');

var _GraphQLError = require('../error/GraphQLError');

var _locatedError = require('../error/locatedError');

var _execute = require('../execution/execute');

var _schema = require('../type/schema');

var _invariant = require('../jsutils/invariant');

var _invariant2 = _interopRequireDefault(_invariant);

var _mapAsyncIterator = require('./mapAsyncIterator');

var _mapAsyncIterator2 = _interopRequireDefault(_mapAsyncIterator);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _asyncToGenerator(fn) { return function () { var gen = fn.apply(this, arguments); return new Promise(function (resolve, reject) { function step(key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { return Promise.resolve(value).then(function (value) { step("next", value); }, function (err) { step("throw", err); }); } } return step("next"); }); }; } /**
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
 * Implements the "Subscribe" algorithm described in the GraphQL specification.
 *
 * Returns a Promise which resolves to either an AsyncIterator (if successful)
 * or an ExecutionResult (client error). The promise will be rejected if a
 * server error occurs.
 *
 * If the client-provided arguments to this function do not result in a
 * compliant subscription, a GraphQL Response (ExecutionResult) with
 * descriptive errors and no data will be returned.
 *
 * If the the source stream could not be created due to faulty subscription
 * resolver logic or underlying systems, the promise will resolve to a single
 * ExecutionResult containing `errors` and no `data`.
 *
 * If the operation succeeded, the promise resolves to an AsyncIterator, which
 * yields a stream of ExecutionResults representing the response stream.
 *
 * Accepts either an object with named arguments, or individual arguments.
 */

/* eslint-disable no-redeclare */
function subscribe(argsOrSchema, document, rootValue, contextValue, variableValues, operationName, fieldResolver, subscribeFieldResolver) {
  // Extract arguments from object args if provided.
  var args = arguments.length === 1 ? argsOrSchema : undefined;
  var schema = args ? args.schema : argsOrSchema;

  return args ? subscribeImpl(schema, args.document, args.rootValue, args.contextValue, args.variableValues, args.operationName, args.fieldResolver, args.subscribeFieldResolver) : subscribeImpl(schema, document, rootValue, contextValue, variableValues, operationName, fieldResolver, subscribeFieldResolver);
}

/**
 * This function checks if the error is a GraphQLError. If it is, report it as
 * an ExecutionResult, containing only errors and no data. Otherwise treat the
 * error as a system-class error and re-throw it.
 */
function reportGraphQLError(error) {
  if (error instanceof _GraphQLError.GraphQLError) {
    return { errors: [error] };
  }
  throw error;
}

function subscribeImpl(schema, document, rootValue, contextValue, variableValues, operationName, fieldResolver, subscribeFieldResolver) {
  var sourcePromise = createSourceEventStream(schema, document, rootValue, contextValue, variableValues, operationName, subscribeFieldResolver);

  // For each payload yielded from a subscription, map it over the normal
  // GraphQL `execute` function, with `payload` as the rootValue.
  // This implements the "MapSourceToResponseEvent" algorithm described in
  // the GraphQL specification. The `execute` function provides the
  // "ExecuteSubscriptionEvent" algorithm, as it is nearly identical to the
  // "ExecuteQuery" algorithm, for which `execute` is also used.
  var mapSourceToResponse = function mapSourceToResponse(payload) {
    return (0, _execute.execute)(schema, document, payload, contextValue, variableValues, operationName, fieldResolver);
  };

  // Resolve the Source Stream, then map every source value to a
  // ExecutionResult value as described above.
  return sourcePromise.then(function (sourceStream) {
    return (0, _mapAsyncIterator2.default)(sourceStream, mapSourceToResponse, reportGraphQLError);
  }, reportGraphQLError);
}