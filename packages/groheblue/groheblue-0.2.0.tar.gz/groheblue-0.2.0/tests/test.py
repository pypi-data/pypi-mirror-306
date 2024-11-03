from groheblue import GroheClient

client = GroheClient("kirstin.weber25@gmail.com", "Uut7fvdG<aKK")


async def main():
    await client.login()

    devices = await client.get_devices()  # get all devices
    device = devices[0]  # select the first device

    # To see all available data, look into the classes.py file. Here are some example values:
    print(device.appliance_id)  # print the appliance id of the device

    print(
        device.data_latest.remaining_co2
    )  # print the remaining co2 of the device in %

    print(
        device.data_latest.remaining_filter
    )  # print the remaining filter of the device in %

    print(
        device.config.co2_consumption_carbonated
    )  # print the co2 consumption for carbonated water

    #await client.dispense(device, 3, 850)  # dispense 50ml of still water


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
