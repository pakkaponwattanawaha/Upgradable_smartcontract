//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Box {
    //type [prefix] scope variablename;
    uint256 private value;

    event ValueChange(uint256 newValue);

    //function function_name(param_type param) [prefix] scope [returns (return_types)] {}
    function store(uint256 newValue) public {
        value = newValue;
        emit ValueChange(newValue);
        //emit event(parameter);
    }

    function retrieve() public view returns (uint256) {
        return value;
    }
}
