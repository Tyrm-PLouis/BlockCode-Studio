
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */
(function () {
    const toolbox = {
        "kind": "categoryToolbox",
        "contents": [
            {
                "kind": "category",
                "name": "Control",
                "contents": [
                    {
                        "kind": "block",
                        "type": "controls_if"
                    }
                ]
            },
            {
                "kind": "category",
                "name": "Logic",
                "contents": [
                    {
                        "kind": "block",
                        "type": "logic_compare"
                    },
                    {
                        "kind": "block",
                        "type": "logic_operation"
                    },
                    {
                        "kind": "block",
                        "type": "logic_boolean"
                    }
                ]
            }
        ]
    };

    Blockly.inject('blocklyDiv', {
        toolbox: toolbox,
        scrollbars: false,
        horizontalLayout: true,
        toolboxPosition: 'end',
    });
})();
