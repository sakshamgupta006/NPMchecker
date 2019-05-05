"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.undefinedFieldMessage = undefinedFieldMessage;
exports.FieldsOnCorrectType = FieldsOnCorrectType;

var _error = require("../../error");

var _suggestionList = _interopRequireDefault(require("../../jsutils/suggestionList"));

var _quotedOrList = _interopRequireDefault(require("../../jsutils/quotedOrList"));

var _definition = require("../../type/definition");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

/**
 * Copyright (c) 2015-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 *
 * 
 */
function undefinedFieldMessage(fieldName, type, suggestedTypeNames, suggestedFieldNames) {
  var message = "Cannot query field \"".concat(fieldName, "\" on type \"").concat(type, "\".");

  if (suggestedTypeNames.length !== 0) {
    var suggestions = (0, _quotedOrList.default)(suggestedTypeNames);
    message += " Did you mean to use an inline fragment on ".concat(suggestions, "?");
  } else if (suggestedFieldNames.length !== 0) {
    message += " Did you mean ".concat((0, _quotedOrList.default)(suggestedFieldNames), "?");
  }

  return message;
}
/**
 * Fields on correct type
 *
 * A GraphQL document is only valid if all fields selected are defined by the
 * parent type, or are an allowed meta field such as __typename.
 */


function FieldsOnCorrectType(context) {
  return {
    Field: function Field(node) {
      var type = context.getParentType();

      if (type) {
        var fieldDef = context.getFieldDef();

        if (!fieldDef) {
          // This field doesn't exist, lets look for suggestions.
          var schema = context.getSchema();
          var fieldName = node.name.value; // First determine if there are any suggested types to condition on.

          var suggestedTypeNames = getSuggestedTypeNames(schema, type, fieldName); // If there are no suggested types, then perhaps this was a typo?

          var suggestedFieldNames = suggestedTypeNames.length !== 0 ? [] : getSuggestedFieldNames(schema, type, fieldName); // Report an error, including helpful suggestions.

          context.reportError(new _error.GraphQLError(undefinedFieldMessage(fieldName, type.name, suggestedTypeNames, suggestedFieldNames), [node]));
        }
      }
    }
  };
}
/**
 * Go through all of the implementations of type, as well as the interfaces
 * that they implement. If any of those types include the provided field,
 * suggest them, sorted by how often the type is referenced,  starting
 * with Interfaces.
 */


function getSuggestedTypeNames(schema, type, fieldName) {
  if ((0, _definition.isAbstractType)(type)) {
    var suggestedObjectTypes = [];
    var interfaceUsageCount = Object.create(null);
    schema.getPossibleTypes(type).forEach(function (possibleType) {
      if (!possibleType.getFields()[fieldName]) {
        return;
      } // This object type defines this field.


      suggestedObjectTypes.push(possibleType.name);
      possibleType.getInterfaces().forEach(function (possibleInterface) {
        if (!possibleInterface.getFields()[fieldName]) {
          return;
        } // This interface type defines this field.


        interfaceUsageCount[possibleInterface.name] = (interfaceUsageCount[possibleInterface.name] || 0) + 1;
      });
    }); // Suggest interface types based on how common they are.

    var suggestedInterfaceTypes = Object.keys(interfaceUsageCount).sort(function (a, b) {
      return interfaceUsageCount[b] - interfaceUsageCount[a];
    }); // Suggest both interface and object types.

    return suggestedInterfaceTypes.concat(suggestedObjectTypes);
  } // Otherwise, must be an Object type, which does not have possible fields.


  return [];
}
/**
 * For the field name provided, determine if there are any similar field names
 * that may be the result of a typo.
 */


function getSuggestedFieldNames(schema, type, fieldName) {
  if ((0, _definition.isObjectType)(type) || (0, _definition.isInterfaceType)(type)) {
    var possibleFieldNames = Object.keys(type.getFields());
    return (0, _suggestionList.default)(fieldName, possibleFieldNames);
  } // Otherwise, must be a Union type, which does not define fields.


  return [];
}