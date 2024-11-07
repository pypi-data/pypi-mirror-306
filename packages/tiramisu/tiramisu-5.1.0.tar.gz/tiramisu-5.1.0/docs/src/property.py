from tiramisu import Config
from tiramisu import StrOption, OptionDescription

# let's declare some options
var1 = StrOption('var1', 'first option')
# an option with a default value
var2 = StrOption('var2', 'second option', u'value')
# let's create a group of options
od1 = OptionDescription('od1', 'first OD', [var1, var2])

# let's create another group of options
rootod = OptionDescription('rootod', '', [od1])

# let's create the config
cfg = Config(rootod)
# the api is read only
cfg.property.read_only()
# the read_write api is available
cfg.property.read_write()

