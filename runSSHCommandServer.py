import time
import logging
import asyncio, asyncssh
import sys
import time
import argparse

from aiohttp import ClientSession, ClientResponseError

logging.getLogger().setLevel(logging.DEBUG)


async def run_client(host, command, retry=3):

    async with asyncssh.connect(host, username="username",
                                password="password",
                                known_hosts=None) as conn:
        return await conn.run(command)


async def run_clients(host, command, retry=5):
    attempt = 0
    conn = None
    import pdb; pdb.set_trace()
    while attempt < retry:
        try:
            async with asyncssh.connect(host, username="username",
                                        password="password",
                                        known_hosts=None) as conn:
                return await conn.run(command)

        except (OSError, asyncssh.Error) as e:
            if attempt < retry:
                logging.info("Hitting Exception in attempts : %d and exception: %s" % (attempt, str(e)))
                logging.info("Increase retry")
            else:
                logging.info("Hitting Exception in attempts : %d and exception: %s" % (attempt, str(e)))
            attempt += 1


async def run_multiple_clients(hosts):
    # Put your lists of hosts here
    # hosts = hosts * 10
    hosts = hosts * 5
    # tasks = (run_client(host, 'ls -l') for host in hosts)
    tasks = (asyncio.wait_for(run_client(host, 'ls -l'), timeout=1000)
             for host in hosts)
    results = await asyncio.gather(*tasks, return_exceptions=True)
    rcs = []
    outs = []
    errs = []

    for i, (result, host) in enumerate(zip(results, hosts), 1):
        if isinstance(result, asyncio.TimeoutError):
            logging.info(print('Task %d timed out result: %s in host: %s' % (i, result, host)))
            rcs.append(1)
            errs.append("")
            outs.append("")

        elif isinstance(result, Exception):
            logging.info('Task %d failed: %s in host: %s' % (i, str(result), host))
            rcs.append(1)
            errs.append("")
            outs.append("")

        elif result.exit_status != 0:
            logging.info('Task %d exited with status %s in host: %s' % (i, result.exit_status, host))
            rcs.append(1)
            outs.append(result.stdout)
            errs.append(result.stderr)
            logging.info(result.stderr)

        else:
            logging.info('Task %d succeeded in host: %s and stdout: %s:' % (i, host, result.stdout))
            rcs.append(0)
            outs.append(result.stdout)
            errs.append(result.stderr)
    return (rcs, outs, errs)

        # logging.info(75*'-')

def read_from_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = read_from_arguments()
    start_time = time.time()
    try:
        hosts = [host.strip() for host in args.server.split(",")]
    except Exception as e:
        raise("Server list is empty")
    # asyncio.get_event_loop().run_until_complete(run_multiple_clients(hosts))
    res = asyncio.run(run_multiple_clients(hosts))
    logging.info(f"{res}")
    logging.info("Total execution completed %s" % str(time.time() - start_time))


