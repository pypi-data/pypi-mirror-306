#!/usr/bin/python3
import logging
from argparse import ArgumentParser
from os import environ, path
from subprocess import Popen
import tempfile
from sys import stderr

from confit2canard import Vault

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stderr)
logger.addHandler(handler)


def main(configuration, passkey: str = ""):
    if not path.exists(path.abspath(path.dirname(configuration))):
        logger.error("Parent folder for %s doesn't exist", configuration)
        return
    editor = environ.get("EDITOR")
    vault = Vault((environ.get("VAULT_PASSKEY") or passkey).encode("utf-8"))
    if not editor:
        logging.error("EDITOR environment variable not set")
        return

    extension = "." + configuration.split(".")[-1]
    old = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension,
                                     mode="w") as tfile:
        if path.exists(configuration):
            logger.info("Reading configuration from %s", configuration)
            with open(configuration, "r") as fd:
                buffer = fd.read()
                if buffer:
                    old = vault.decrypt(fd.read())
                    tfile.write(old)
        tfile.close()
        process = Popen([editor, tfile.name])
        process.wait()

        if process.returncode != 0:
            logging.error("An error occurred with editor %s", editor)
            return

        with open(tfile.name, "r") as fd:
            payload = fd.read()

    if len(payload) == 0:
        logger.info("Nothing to write")
        return
    if payload != "":
        payload = vault.encrypt(payload)
    try:
        with open(configuration, "w+") as fd:
            fd.write(payload)
            logger.info("Writing %d bytes", len(payload))
    except PermissionError:
        logger.error("Couldn't write configuration to file: %s", payload)


if __name__ == "__main__":
    args = ArgumentParser("Confit2Canard")
    args.add_argument("config", action="store",
                      help="The path to the file to edit")

    parsed = args.parse_args()
    main(parsed.config)
