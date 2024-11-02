# Neatlogger

Neat adaptions to the loguru package which wraps logging in python.

## Idea

This wrapper around loguru shortcuts your way to more simple usage of loggers, especially useful in small, production-ready scripts:
- Provides the shorthand `log` instead of `logger` 
- Provides new levels: `NEW`, `PROGRESS`, `READ`, `WRITE`, `DONE`.
- Formats logger outputs more cleanly, skips unnecessary information.

## Example usage:

```python
from neatlogger import log

log.new("Welcome to my script")
log.trace("Some minor tracing message")
x = 42
log.debug("Let's debug value x={}", x)
log.info("By the way, it's going well so far.")
log.progress("Heavy calculation ahead...")
log.read("Reading in some data...")
log.write("Writing some output file...")
log.warning("Note that writing files could take some time!")
try:
    x / 0
except Exception as e:
    log.error("An error occured: {}", e)
log.success("Yey, found a solution to the problem eventually.")
log.done("")
```

![Example output](https://github.com/mschroen/neatlogger/blob/main/docs/example_output.png)

## Install

```bash
pip install neatlogger
```

Requires:
- loguru