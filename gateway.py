from asyncio import run
from json import load
from pymodbus.client import ModbusSerialClient
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusServerContext
from pymodbus.datastore.remote import RemoteSlaveContext
from threading import Thread


async def open_gateway():
    with open('config.json', encoding='UTF-8') as file:
        config = load(file)
    client = ModbusSerialClient(port="/dev/ttyUSB0", **config['serial'])
    client.connect()
    context = ModbusServerContext(
        slaves={x: RemoteSlaveContext(client, slave=x) for x in range(1, 255)},
        single=False
    )
    print(f'Gateway opened\nIP: {config['tcp']['host']}\nPort: 5020')
    await StartAsyncTcpServer(
			address=(config['tcp']['host'], 5020),
			context=context
	)



async def open_gateway2():
    with open('config.json', encoding='UTF-8') as file:
        config = load(file)
    client = ModbusSerialClient(port="/dev/ttyUSB1", **config['serial'])
    client.connect()
    context = ModbusServerContext(
        slaves={x: RemoteSlaveContext(client, slave=x) for x in range(1, 255)},
        single=False
    )
    print(f'Gateway opened\nIP: {config['tcp']['host']}\nPort: 5021')
    await StartAsyncTcpServer(
        address=(config['tcp']['host'], 5021),
        context=context
    )

def target1():
    run(open_gateway())

def target2():
    run(open_gateway2())

if __name__ == "__main__":
    owen_thread = Thread(target=target1)
    rs_thread = Thread(target=target2)
    owen_thread.start()
    rs_thread.start()
