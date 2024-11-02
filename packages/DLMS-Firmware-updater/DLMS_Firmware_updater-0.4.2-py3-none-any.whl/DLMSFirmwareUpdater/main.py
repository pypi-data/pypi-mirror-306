import argparse
import time
from DLMS_SPODES_client.servers import TransactionServer, Result
from DLMS_SPODES_client import task, services
from DLMS_SPODES_client.client import Client, logL, IDFactory
from DLMSAdapter.xml_ import xml50
from DLMS_SPODES_communications import Serial, Network


task.get_adapter(adapter := xml50)
id_factory = IDFactory("#")


def main():
    parser = argparse.ArgumentParser(
        description="Update Firmware Program for DLMS meters")
    parser.add_argument(
        '-t', '--type',
        choices=("File", "Serial", "Net"),
        required=True,
        help="Communication type")
    parser.add_argument(
        "-p",
        nargs='*',
        help="connection parameters")
    parser.add_argument(
        "-T", "--timeout",
        type=int,
        default=60,
        help="communication timeout %(default)")
    parser.add_argument(
        "-s", "--secret",
        type=lambda value: str.encode(value, "ascii"),
        default="0000000000000000",
        help="DLMS association secret")
    parser.add_argument(
        "-sap",
        type=int,
        default=0x30,
        help="DLMS SAP [default=0x30] ")
    parser.add_argument(
        "-da",
        type=int,
        default=0x10,
        help="DLMS Device Address")
    parser.add_argument(
        "-m", "--mechanism_id",
        type=int,
        default=2,
        help="DLMS association mechanism ID")
    parser.add_argument(
        "-u", "--universal",
        action='store_true',
        # type=bool,
        # default=False,
        help="Client is universal(not check LDN)")
    parser.add_argument(
        "-as", "--addr_size",
        type=int,
        choices=(-1, 1, 2, 4),
        default=1,
        help="Client HDLC address size type from :-1, 1, 2, 4")
    parser.add_argument(
        "-d", "--loop_delay",
        type=int,
        default=2,
        help="delay between attempts of loop(in second)")
    parser.add_argument(
        "-l", "--n_loops",
        type=int,
        default=3,
        help="attempts amount")
    parser.add_argument(
        "-f", "--file",
        type=str,
        default=".//output.txt",
        help="output result file"
    )
    args = parser.parse_args()
    if (source := args.type) in ("Serial", "Net"):
        clients = [
            c := Client(
                SAP=args.sap,
                secret=args.secret.hex(),
                addr_size=-1,
                id_=id_factory.create(),
                response_timeout=args.timeout,
                universal=args.universal
            )
        ]
        c.m_id.set(args.mechanism_id)
        c.com_profile.parameters.device_address = args.da
        match source, args.p:
            case "Serial", [port]:
                c.media = Serial(port=port)
            case "Serial", [port, baudrate]:
                c.media = Serial(port=port, baudrate=baudrate)
            case "Net", [host, port]:
                c.media = Network(host=host, port=port)
            case _:
                raise RuntimeError(F"unknown {source=} with {', '.join(args.p)}")
    elif source == "File":
        if len(args.p) == 1:
            clients = services.get_client_from_csv(
                file_name=args.p[0],
                id_factory=id_factory)
        else:
            raise ValueError("-p for \"File\" must have 1 file name")
    else:
        raise ValueError(F"unknown {source=}")
    t_server = TransactionServer(
        clients=clients,
        tsk=task.Loop(
            task=task.UpdateFirmware(),
            func=lambda res: res,
            delay=args.loop_delay,
            attempt_amount=args.n_loops
        )
    )
    t_server.start()
    results = list(t_server.results)
    with open(
            file=args.file,
            mode="w+",
            encoding="utf-8") as file:
        while results:
            try:
                time.sleep(3)
            except KeyboardInterrupt:
                t_server.abort()
                print("Abort")
                raise SystemExit
            for res in results:
                res: Result
                if res.complete:
                    results.remove(res)
                    res.client.log(logL.INFO, F"Для {res.client} обновление: {'Удачно' if res.value else 'Неудачно'}")
                    file.write(F"{res.client} {res.value} {res.errors}\n")


if __name__ == "__main__":
    main()
