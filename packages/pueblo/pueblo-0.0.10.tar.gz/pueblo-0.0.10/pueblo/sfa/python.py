import logging
from tempfile import NamedTemporaryFile

from upath import UPath

logger = logging.getLogger(__name__)


def load_target(target: str):

    app_file = None
    if True:
        upath = UPath(target)
        frag = upath._url.fragment
        suffix = upath.suffix
        suffix = suffix.replace(f"#{frag}", "")
        logger.info(f"Loading remote single-file application, source: {upath}")
        name = "_".join([upath.parent.stem, upath.stem])
        app_file = NamedTemporaryFile(prefix=f"{name}_", suffix=suffix, delete=False)
        target = app_file.name
        if frag:
            target = f"{app_file.name}:{frag}"
        logger.info(f"Writing remote single-file application, target: {target}")
        app_file.write(upath.read_bytes())
        app_file.flush()
