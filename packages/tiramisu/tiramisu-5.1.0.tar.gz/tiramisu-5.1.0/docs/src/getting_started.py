"getting started with the tiramisu library (it loads and prints properly)"

from tiramisu import Config
from tiramisu import OptionDescription, BoolOption

# let's create a group of options
descr = OptionDescription("optgroup", "", [
                          # ... with only one option inside
                          BoolOption("bool", "", default=False)
                          ])

cfg = Config(descr)

# the global help about the config
cfg.help()
# help about an option
cfg.option("bool").help()
# the config's __repr__
print(cfg)
