pragma solidity >=0.4.0 <0.7.0;
pragma experimental ABIEncoderV2;

contract TraceStorage {
    bytes[] public trace;

    function addTrace(bytes memory x) public {
        trace.push(x);
    }

    function getTrace() public view returns (bytes[] memory) {
        return trace;
    }
}