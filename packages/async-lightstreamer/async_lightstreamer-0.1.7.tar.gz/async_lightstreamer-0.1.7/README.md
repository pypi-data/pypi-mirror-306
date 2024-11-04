# Async Light Streamer Client

This project is based on [lightstreamer-client](https://github.com/wjszlachta/lightstreamer-client)


# Install
```bash
pip install async-lightstreamer
# or if you are using poetry
poetry add async-lightstreamer
```

# Task Group
This client creates a task for receving new messages
You can pass TaskGroup to LightstreamerClient, and client will use
given TaskGroup for creating task
```python
async with asyncio.TaskGroup() as tg:
    async_lightstreamer.LightstreamerClient(
        lightstreamer_username="<username>",
        lightstreamer_password="<password>",
        lightstreamer_url="<url>",
        adapter_set="<adapter>",
        task_group=tg,
    )
```
# Reconnect
If you set `should_reconnect` flag to true in LightstreamerClient, client will reconnect
and subscribe all subscriptions
```python
async_lightstreamer.LightstreamerClient(
    lightstreamer_username="<username>",
    lightstreamer_password="<password>",
    lightstreamer_url="<url>",
    adapter_set="<adapter>",
    should_reconnect = True,
    reconnect_retries = 100, # set to -1 for infitine retry
)
```

# Example
```python
import asyncio
import async_lightstreamer

async def main():
    lc = async_lightstreamer.LightstreamerClient(
        lightstreamer_username="<username>",
        lightstreamer_password="<password>",
        lightstreamer_url="<url>",
        adapter_set="<adapter>",
    )
    await lc.connect()
    async def callback(data) -> None:
        print(data)

    await lc.subscribe(
        subscription=async_lightstreamer.LightstreamerSubscription(
            mode=async_lightstreamer.Mode.MERGE,
            items=["item1", "item2"],
            fields=["field1", "field2"],
            adapter="adapter",
        ).addlistener(callback),
    )
    await asyncio.sleep(60)
    await lc.disconnect()


asyncio.run(main())
```
