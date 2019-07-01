pragma solidity ^0.4.24;

contract Trace_hash {
    struct Hash {
        string inputHash;
        string outputHash;
        string commandHash;
    }

    Hash[] public hashes;

    function recordHash(string _inputHash, string _outputHash, string _commandHash) returns (uint) {
        hashes.length++;
        hashes[hashes.length - 1].inputHash = _inputHash;
        hashes[hashes.length - 1].outputHash = _outputHash;
        hashes[hashes.length - 1].commandHash = _commandHash;
        return hashes.length;
    }

    function getHashesCount() public view returns(uint) {
        return hashes.length;
    }

    function getHash(uint index) public view returns (string, string, string) {
        return (hashes[index].inputHash, hashes[index].outputHash, hashes[index].commandHash);
    }
}

