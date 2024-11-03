#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI for multi-entity corecfg operations
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

import json
import os
import sys

from quickcolor.color_def import color
from showexception.showexception import exception_details

from .multi_entity import MultiEntityCoreCfg

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def instantiate_core_cfg(cfgFileName: str, debug: bool = False) -> MultiEntityCoreCfg:
    coreCfg = MultiEntityCoreCfg(cfgFileName=cfgFileName, debug = debug)
    cfgMetadataInit = { 'label' : 'Test Config', 'maxLabelLen' : 20 }
    categoryMetadataInit = {
            'cat1' : { 'color' : color.CGREEN, 'maxLen' : 20 },
            'cat2' : { 'color' : color.CWHITE2, 'maxLen' : 20 },
            'cat3' : { 'color' : color.CBLUE2, 'maxLen' : 20 }
            }

    if cfgMetadataInit != coreCfg.get_cfg_metadata() or categoryMetadataInit != coreCfg.get_category_metadata():
        if debug:
            print(f'Initializing metadata for cfg and categories!')
        coreCfg.initialize_metadata(cfgMetadata=cfgMetadataInit, categoryMetadata=categoryMetadataInit)

    return coreCfg

# ------------------------------------------------------------------------------------------------------

def cli():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}Core Config {color.CYELLOW2}multi-entity{color.CEND} controls',
                    epilog='-.' * 40)

        parser.add_argument(
                '--cfgfile',
                metavar='<cfg file>',
                default="test_multi_entity_cfg.json",
                help='Config filename')

        parser.add_argument(
                '-d', '--debug',
                action="store_true",
                help='Run with debug hooks enabled')


        subparsers = parser.add_subparsers(dest='cmd')

        parser_removeCfgFile = subparsers.add_parser('remove.cfg', help='remove config file')

        parser_readFromCfgFile = subparsers.add_parser('read.cfg', help='read from config file')
        parser_readFromCfgFile.add_argument('--raw', metavar='<raw>', help='display raw config contents')

        parser_writeToCfgFile = subparsers.add_parser('write.cfg', help='write to config file')

        parser_selectItem = subparsers.add_parser('select.item', help='select config tuple')
        parser_selectItem.add_argument('label', metavar='<cfgLabel>', help='config item label')

        parser_updateItem = subparsers.add_parser('update.item', help='update config tuple')
        parser_updateItem.add_argument('label', metavar='<cfgLabel>', help='config item label')
        parser_updateItem.add_argument('--cat1', default=None, help='config category 1 value')
        parser_updateItem.add_argument('--cat2', default=None, help='config category 1 value')
        parser_updateItem.add_argument('--cat3', default=None, help='config category 1 value')

        parser_removeItem = subparsers.add_parser('remove.item', help='remove config tuple')
        parser_removeItem.add_argument('label', metavar='<cfgLabel>', help='config item label')

        parser_removeItemList = subparsers.add_parser('remove.item.list', help='remove identified config tuples')
        parser_removeItemList.add_argument('labellist', nargs='*', help='config item label list')

        parser_showFullCfg = subparsers.add_parser('show.full.cfg', help='show full config')

        parser_showItemLabels = subparsers.add_parser('show.item.labels', help='show item labels')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        coreCfg = instantiate_core_cfg(cfgFileName = args.cfgfile, debug = args.debug)

        if args.cmd == 'remove.cfg':
            coreCfg.remove_config_file()
            print(f'Config file {color.CVIOLET}{args.cfgfile}{color.CEND} is removed!')

        elif args.cmd == 'read.cfg':
            if args.raw:
                print(json.dumps(coreCfg.read_config_from_file(), indent=4))
            else:
                cfgFileContents = coreCfg.read_config_from_file()
                for key, value in cfgFileContents.items():
                    print(f"Key - {key} : {json.dumps(value, indent=4)}")

        elif args.cmd == 'write.cfg':
            coreCfg.write_config_to_file()
            print(f'Config file {color.CCYAN2}{args.cfgfile}{color.CEND} was written with cached content!')

        elif args.cmd == 'select.item':
            coreCfg.select_item(itemLabel = args.label)
            print(f'Item label {color.CYELLOW2}{args.label}{color.CEND} is now selected!')
            coreCfg.show_full_config()

        elif args.cmd == 'update.item':
            tupleList = {}
            tupleList['cat1'] = args.cat1
            tupleList['cat2'] = args.cat2
            tupleList['cat3'] = args.cat3

            allItems = coreCfg.get_all_configured_items()
            if args.label in allItems.keys() and tupleList in allItems.values():
                print(f'{color.CRED2}Error: {color.CWHITE2}Tuple ' + \
                        f'{color.CBLUE2}{str(tupleList.values())} ' + \
                        f'{color.CWHITE}is already registered!{color.CEND}')
                sys.exit(1)
            coreCfg.update_item(itemLabel=args.label, newTuple=tupleList)
            print(f'Item label {color.CBLUE2}{args.label}{color.CEND} is now updated!')
            coreCfg.show_full_config()

        elif args.cmd == 'remove.item':
            coreCfg.remove_item(itemLabel=args.label)
            print(f'Item label {color.CRED2}{args.label}{color.CEND} is now removed!')
            coreCfg.show_full_config()

        elif args.cmd == 'remove.item.list':
            coreCfg.remove_multiple_items(itemLabelList=args.labellist)
            print(f'Items from list {color.CRED2}{args.labellist}{color.CEND} are now removed!')
            coreCfg.show_full_config()

        elif args.cmd == 'show.full.cfg':
            coreCfg.show_full_config()

        elif args.cmd == 'show.item.labels':
            coreCfg.show_item_labels()

    except Exception as e:
        exception_details(e, "CoreCfg Multi-Entity CLI", raw=False)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

