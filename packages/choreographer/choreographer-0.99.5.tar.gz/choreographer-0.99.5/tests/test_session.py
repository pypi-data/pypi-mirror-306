import warnings

import pytest
import pytest_asyncio

import choreographer as choreo


@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def session(browser):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", choreo.protocol.ExperimentalFeatureWarning)
        session_browser = await browser.create_session()
    yield session_browser
    await browser.close_session(session_browser)


@pytest.mark.asyncio
async def test_send_command(session):
    response = await session.send_command("Target.getTargets")
    assert "result" in response and "targetInfos" in response["result"]
