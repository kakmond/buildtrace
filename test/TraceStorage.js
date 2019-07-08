const SimpleStorage = artifacts.require("TraceStorage");

contract("TraceStorage", function () {

    it("should add the trace data", () =>
        SimpleStorage.deployed()
            .then(async instance => {
                await instance.addTrace('0x01')
                return instance.getTrace();
            })
            .then(traceData => {
                assert.equal(
                    traceData[0],
                    '0x01',
                    "0x01 wasn't in the trace data"
                );
            })
    )
});