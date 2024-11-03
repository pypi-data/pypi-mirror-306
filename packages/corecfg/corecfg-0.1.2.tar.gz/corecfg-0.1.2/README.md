# CoreCfg

**CoreCfg** consists of a discrete set of base configuration classes to serve as the core foundation for configuring python projects.

Imagine a python project, such as a connection management tool providing quick access to ssh or telnet sessions. That project itself, provides session access methods, possibly logging and other functionality. Using the python project flexibly implies providing several runtime options/attributes that would be used such as an IPV4 address, an ephemeral port, possibly a connection username, etc. Instead of having to memorize session specific attributes and provide them when opening each session, it is desirable to create a set of configuration details for multiple connection sessions and store their attributes in a persistent config file, allocating these session attributes to a session label. This way, opening a connection session only depends on providing one of the configured session labels and all attributes associated with the session are available to the runtime script.

CoreCfg serves as the base class to project specific configuration handlers. CoreCfg provides the basic interfaces to deal with the project configuration without concerning itself about specific attributes. That part is left up to child classes inheriting from CoreCfg in the context of specific projects.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **corecfg**.

```bash
pip install corecfg
```

## Multi-Entity Sample Usage
```python
from quickcolor.color_def import color
from corecfg.multi_entity import MultiEntityCoreCfg

class TestConfig(MultiEntityCoreCfg):

    def __init__(self):
        super(TestConfig, self).__init__(cfgFileName='test_config.json')

        cfgMetadataInit = { 'label' : 'Test Items', 'maxLabelLen' : 20 }
        categoryMetadataInit = {
                'trait-A' : { 'color' : color.CGREEN, 'maxLen' : 15 },
                'trait-B' : { 'color' : color.CWHITE2, 'maxLen' : 12 },
                'trait-C' : { 'color' : color.CBLUE2, 'maxLen' : 12 },
                'trait-D' : { 'color' : color.CVIOLET2, 'maxLen' : -1 },
                }

        if cfgMetadataInit != self.get_cfg_metadata() or categoryMetadataInit != self.get_category_metadata():
            self.initialize_metadata(cfgMetadata=cfgMetadataInit, categoryMetadata=categoryMetadataInit)


    def register(self, itemLabel, itemTraitA, itemTraitB, itemTraitC, itemTraitD):
        tupleList = {}
        tupleList['trait-A'] = itemTraitA
        tupleList['trait-B'] = itemTraitB
        tupleList['trait-C'] = itemTraitC
        tupleList['trait-D'] = itemTraitD

        cfgItemList = self.get_all_configured_items()

        if itemLabel in cfgItemList and tupleList in cfgItemList.values():
            print(f'{color.CRED2}Error: {color.CWHITE}Item {itemLabel} and tuple ' + \
                    f'{color.CBLUE2}{str(tupleList.values())} ' + \
                    f'{color.CWHITE}are already registered!{color.CEND}')
            return

        self.update_item(itemLabel = itemLabel, newTuple = tupleList)

    def unregister(self, itemLabel):
        cfgItemList = self.get_all_configured_items()
        if itemLabel not in cfgItemList:
            print(f'{color.CRED2}Error: {color.CWHITE} Test item label {color.CBLUE2}{itemLabel} ' + \
                    f'{color.CWHITE}is not registered in test config!{color.CEND}')
            return

        print(f'{color.CVIOLET2}\n   -- removing test item {color.CYELLOW}{itemLabel} ' + \
                f'{color.CVIOLET2}containing\n{color.CWHITE2}{str(cfgItemList[itemLabel])}{color.CEND}')

        self.remove_item(itemLabel=itemLabel)

tc = TestConfig()
tc.register('item #1', 'i1.a', 'i1.b', 'i1.c', 'i1.d')
tc.register('item #2', 'i2.a', 'i2.b', 'i2.c', 'i2.d')
tc.register('item #3', 'i3.a', 'i3.b', 'i3.c', 'i3.d')

tc.show_full_config()

tc.unregister('item #2')

tc.show_full_config()
```

## Multi-Entity Sample Output
```bash
  ----------------------------------------
  |  test_config.json          (custom)  |
  ----------------------------------------

   Test Items          trait-A        trait-B     trait-C     trait-D
   ----------          -------        -------     -------     -------
   item #1             i1.a           i1.b        i1.c        i1.d
   item #2             i2.a           i2.b        i2.c        i2.d
-> item #3             i3.a           i3.b        i3.c        i3.d


   -- removing test item item #2 containing
{'trait-A': 'i2.a', 'trait-B': 'i2.b', 'trait-C': 'i2.c', 'trait-D': 'i2.d'}

  ----------------------------------------
  |  test_config.json          (custom)  |
  ----------------------------------------

   Test Items          trait-A        trait-B     trait-C     trait-D
   ----------          -------        -------     -------     -------
   item #1             i1.a           i1.b        i1.c        i1.d
-> item #3             i3.a           i3.b        i3.c        i3.d
```

## CLI Utilities

The following multi entity CLI is provided in this package.

```bash
# corecfg-me -h
usage: corecfg-me [-h] [--cfgfile <cfg file>] [-d]
                  {remove.cfg,read.cfg,write.cfg,select.item,update.item,remove.item,remove.item.list,show.full.cfg,show.item.labels} ...

-.-.-. Core Config multi-entity controls

positional arguments:
  {remove.cfg,read.cfg,write.cfg,select.item,update.item,remove.item,remove.item.list,show.full.cfg,show.item.labels}
    remove.cfg          remove config file
    read.cfg            read from config file
    write.cfg           write to config file
    select.item         select config tuple
    update.item         update config tuple
    remove.item         remove config tuple
    remove.item.list    remove identified config tuples
    show.full.cfg       show full config
    show.item.labels    show item labels

options:
  -h, --help            show this help message and exit
  --cfgfile <cfg file>  Config filename
  -d, --debug           Run with debug hooks enabled

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

