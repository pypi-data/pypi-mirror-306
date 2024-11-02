"""Usage example for this package."""

from loguru import logger as log

import uv_demo


def main() -> None:
    """Main entrypoint and usage example for uv-demo."""
    log.info(uv_demo.__version__)
    log.info(uv_demo.LIB_NAME)
    uv_demo.say_hello()


if __name__ == "__main__":
    main()
