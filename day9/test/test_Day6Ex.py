import asyncio
import pytest
import httpx


#async def test_without_marker():
    #await asyncio.sleep(0)
    #assert True


async def fetch(name, seconds):
    await asyncio.sleep(seconds)
    return name

@pytest.mark.asyncio
async def test_gather_keeps_order():
    results = await asyncio.gather(fetch("a", 0.2), fetch("b", 0.1))
    assert results == ["a", "b"]

async def good():
    return "ok"

async def bad():
     raise ValueError("boom")

@pytest.mark.asyncio
async def test_to_test_return_exceptions():
    results = await asyncio.gather(good(), bad(), return_exceptions=True)
    assert results[0] == "ok"
    assert isinstance(results[1], ValueError)

@pytest.mark.asyncio
async def test_wait_for_times_out():
    async def slow():
        await asyncio.sleep(5)

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow(), timeout=0.1)

async def fake_sleep(s):
    pass



"""def test_retry_503_success(monkeypatch, tmp_path, sample_items):
    calls = []
    def handler(request):
        calls.append(1)
        return httpx.Response(503)

    def fakeClient():
        return httpx.Client(
            base_url="http://fake-test", 
            transport=httpx.MockTransport(handler))
    
    monkeypatch.setattr(Day9Exercises.asyncio, "sleep", fake_sleep)

    with pytest.raises(httpx.HTTPStatusError):
        assert len(calls) == 3"""