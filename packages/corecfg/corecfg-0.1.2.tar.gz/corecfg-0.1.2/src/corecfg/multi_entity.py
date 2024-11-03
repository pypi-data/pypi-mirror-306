#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Base Class for Configurations
# ------------------------------------------------------------------------------------------------------
# Config contents:
# - type: default/custom
# - last.updated: <date>
# - name: config filename
# - last selected: item tuple key
# - metadata:
#   [
#       itemType: { label:itemTypeName, maxLabelLen:<len> }
#       metadata:
#       {
#           "item.1" : { color:<color>, maxLen:<len> },
#           "item.2" : { color:<color>, maxLen:<len> },
#           "item.3" : { color:<color>, maxLen:<len> },
#           ...
#       }
#   ]
# - items:
#   {
#      item.1: { a:x, b:y, c:z, ... }
#      item.2: { a:x, b:y, c:z, ... }
#      item.3: { a:x, b:y, c:z, ... }
#      ...
#   }
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

import sys
import operator
import os
import json

from pathlib import Path
from datetime import datetime

from quickcolor.color_def import color
from showexception.showexception import exception_details

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

class MultiEntityCoreCfg:
    def __init__(self, cfgFileName=None, cfgFilePath=None, debug=False):
        self._dfltCfgInfo = {
            "cfgClassification" : "default",
            "cfgName" : "unconfigured",
            "lastSelectedItem" : "n/a",
            'cfgMetadata' : {},
            "categoryMetadata" : {},
            "items" : {}
            }

        self._runDebug = debug
        if self._runDebug:
            print(f' ---> Initializing {color.CGREEN2}{cfgFileName}{color.CEND} in multi-entity core obj id ({color.CVIOLET2}{str(id(self))}{color.CEND})!')

        if not cfgFilePath:
            cfgFilePath = f"{os.path.expanduser('~')}/.config/coreCfg"
            if self._runDebug:
                print(f' ---> Using cfg file path {color.CYELLOW2}{cfgFilePath}{color.CEND}!')

        if not os.path.isdir(cfgFilePath):
            Path(cfgFilePath).mkdir(parents=True, exist_ok=True)
            if self._runDebug:
                print(f' ---> Creating cfg file path {color.CYELLOW2}{cfgFilePath}{color.CEND}!')

        self._cfgFileFullPath = cfgFilePath + '/' + cfgFileName
        self._cfgInfo = self.read_config_from_file()
        if self._cfgInfo["cfgClassification"] == "default":
            self._cfgInfo["cfgName"] = cfgFileName

        if self._runDebug:
            print(f' ---> {color.CGREEN2}{cfgFileName}{color.CEND} initialization is complete!')

    def remove_config_file(self):
        if self._cfgFileFullPath:
            os.remove(self._cfgFileFullPath)
            if self._runDebug:
                print(f' ---> Removed {color.CBLUE2}{self._cfgFileFullPath}{color.CEND} config file!')

    def read_config_from_file(self) -> dict:
        try:
            with open(self._cfgFileFullPath, "r") as jsonfile:
                return json.load(jsonfile)

        except FileNotFoundError:
            print(f'{color.CRED2}Warning:{color.CWHITE2} Could not find {color.CCYAN2}{self._cfgFileFullPath}', end='', flush=True)
            print(f'{color.CWHITE2} -- Using default config settings!{color.CEND}')
            if self._runDebug:
                print(f'Default Config Info:\n{json.dumps(self._dfltCfgInfo, indent=4)}')

            return self._dfltCfgInfo


    def write_config_to_file(self, configInfo=None):
        if not configInfo:
            configInfo = self._cfgInfo

        configInfo['cfgClassification'] = "custom"
        # note: operator.itemgetter() is a callable that uses the zeroth field in each item as a sort key
        configInfo['items'] = dict(sorted(configInfo['items'].items(), key=operator.itemgetter(0)))
        localJsonCfg = json.dumps(configInfo)

        cfgDir = os.path.dirname(self._cfgFileFullPath)
        if not os.path.exists(cfgDir):
            os.makedirs(cfgDir)

        with open(self._cfgFileFullPath, "w") as jsonfile:
            jsonfile.write(localJsonCfg)


    def initialize_metadata(self, cfgMetadata=None, categoryMetadata=None):
        if self._runDebug:
            print(f'{color.CYELLOW2}Initializing metadata ...{color.CEND}')

        # format for cfgMetadata: { label : 'Cfg Label Name', 'maxLabelLen' : <maxCfgLabelLen> }
        # format for categoryMetadata: { category_1 : { 'color' : <categoryColor>, 'maxLen' : <maxCategoryLabelLen> }, ... }
        self._cfgInfo['cfgMetadata'] = cfgMetadata
        self._cfgInfo['categoryMetadata'] = categoryMetadata
        self._cfgInfo['lastSelectedItem'] = "n/a"

        self.write_config_to_file()


    def select_item(self, itemLabel: str | None = None, ignoreDebug: bool = False):
        if not itemLabel or itemLabel not in self._cfgInfo['items'].keys():
            raise ValueError(f"Error: Need a valid item label to select! {itemLabel} is invalid!")

        if self._cfgInfo['lastSelectedItem'] == itemLabel:
            # necessary to avoid prints when repeated/duplicate selection is expected during runtime
            if self._runDebug and not ignoreDebug:
                print(f'{color.CRED2}Error: {color.CWHITE2}{str(itemLabel)}{color.CRED2} is already selected!{color.CEND}')
            return

        self._cfgInfo['lastSelectedItem'] = itemLabel
        self.write_config_to_file()


    def update_item(self,
                    itemLabel: str | None = None,
                    newTuple : tuple | None = None,
                    writeToFile: bool = True):
        if not itemLabel or not newTuple:
            raise ValueError("Error: Need a tuple with content for a valid item!")

        self._cfgInfo['lastSelectedItem'] = itemLabel
        self._cfgInfo['items'][itemLabel] = newTuple
        if writeToFile:
            self.write_config_to_file()


    def remove_item(self, itemLabel: str | None = None, writeToFile: bool = True):
        if not itemLabel:
            raise ValueError("Error: Need a valid item label!")

        if itemLabel not in self._cfgInfo['items']:
            raise ValueError(f"Error: {itemLabel} does not appear to be a valid item label!")

        self._cfgInfo['items'].pop(itemLabel)

        if self._cfgInfo['lastSelectedItem'] == itemLabel:
            self._cfgInfo['lastSelectedItem'] = "n/a"

        if writeToFile:
            self.write_config_to_file()


    def remove_multiple_items(self,
                             itemLabelList: list | None = None,
                             writeToFile: bool = True):
        if not itemLabelList:
            raise ValueError("Error: Need at least one valid item label in the list!")

        for itemLabel in itemLabelList:
            try:
                self._cfgInfo['items'].pop(itemLabel)

                if self._cfgInfo['lastSelectedItem'] == itemLabel:
                    self._cfgInfo['lastSelectedItem'] = "n/a"

            except Exception as e:
                continue

        # 2024-0728 - not sure what the purpose of this is anymore - deprecate soon unless it is needed
        '''
        remainingItems = self._cfgInfo['items'].values()
        if len(remainingItems):
            self._cfgInfo['items'] = {}
            for itemTuple in remainingItems:
                self._cfgInfo['items'][str(len(self._cfgInfo['items'])+1)] = itemTuple
            self._cfgInfo['lastSelectedItem'] = str(len(self._cfgInfo['items']))
        '''

        if writeToFile:
            self.write_config_to_file()

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

    def get_cfg_metadata(self) -> dict:
        return self._cfgInfo["cfgMetadata"]

    def get_category_metadata(self):
        return self._cfgInfo["categoryMetadata"]

    def get_all_configured_items(self):
        return self._cfgInfo["items"]

    def get_last_selected_item_label(self):
        return self._cfgInfo["lastSelectedItem"]

    def get_cfg_data_for_last_selected_item(self):
        return self._cfgInfo["items"][self._cfgInfo["lastSelectedItem"]]

    def get_cfg_data_for_item_label(self, itemLabel):
        try:
            return self._cfgInfo["items"][itemLabel]

        except Exception as e:
            exception_details(e, "get_cfg_data_for_item_label")

    def get_available_item_labels(self):
        if not len(self._cfgInfo['items']):
            return None
        return self._cfgInfo['items'].keys()

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

    def show_cfg_title_box(self):
        typeColor = { 'default' : color.CWHITEBG + color.CRED, 'custom' : color.CGREEN }
        hdash = '-' * ( 3 + len(self._cfgInfo['cfgName']) + 10 + 1 + len(self._cfgInfo['cfgClassification']) + 1 + 3 )

        print(f'\n{color.CWHITE2}  {hdash}')
        print(f"{color.CWHITE2}  |  {color.CYELLOW}{self._cfgInfo['cfgName']}{' '*10}" + \
              f"{typeColor[self._cfgInfo['cfgClassification']]}({self._cfgInfo['cfgClassification']}){color.CEND}{color.CWHITE2}  |")
        print(f'{color.CWHITE2}  {hdash}{color.CEND}\n')


    def show_table_header(self):
        # first column label
        cfgMetadataLabel = self._cfgInfo['cfgMetadata']['label']
        cfgMetadataMaxLabelLen = self._cfgInfo['cfgMetadata']['maxLabelLen']
        print(f"   {color.CYELLOW}%-*s" % (cfgMetadataMaxLabelLen, cfgMetadataLabel), end='', flush=True)

        # other columns for all categories in this config
        for header, md in self._cfgInfo['categoryMetadata'].items():
            if md['maxLen'] != 0:
                print('%s%-*s' % (md['color'], md['maxLen'], header), end='', flush=True)

        # separator bar for first column
        print(f"\n   {color.CWHITE2}" + "%-*s" % (cfgMetadataMaxLabelLen, '-'*len(cfgMetadataLabel)), end='', flush=True)

        # separator bars for other columns
        for header, md in self._cfgInfo['categoryMetadata'].items():
            if md['maxLen'] != 0:
                print('%s%-*s' % (color.CWHITE2, md['maxLen'], '-'*len(header)), end='', flush=True)

    def show_item_data(self):
        cfgMetadataLabel = self._cfgInfo['cfgMetadata']['label']
        cfgMetadataMaxLabelLen = self._cfgInfo['cfgMetadata']['maxLabelLen']
        print()
        for itemLabel, cfgData in self._cfgInfo['items'].items():
            if self._cfgInfo['lastSelectedItem'] == itemLabel:
                print(f'{color.CCYAN2}-> ', end='', flush=True)
            else:
                print('   ', end='', flush=True)
            print(f'{color.CWHITE2}%-*s' % (cfgMetadataMaxLabelLen, itemLabel), end='', flush=True)
            for key, value in cfgData.items():
                dataColor = self._cfgInfo['categoryMetadata'][key]['color']
                maxLen = self._cfgInfo['categoryMetadata'][key]['maxLen']
                if dataColor and maxLen:
                    if maxLen < 0 and value and len(str(value)) > 50:
                        value = f"{value[0:10]} ... {value[-10:]}"
                    if 'qualifier' in self._cfgInfo['categoryMetadata'][key] and self._cfgInfo['categoryMetadata'][key]['qualifier']:
                        value = self.modify_value_by_qualifier(self._cfgInfo['categoryMetadata'][key]['qualifier'], value)
                    print('%s%-*s' % (dataColor, maxLen, value), end='', flush=True)
            print("")
        print(color.CEND)

    def show_full_config(self):
        self.show_cfg_title_box()

        if not len(self._cfgInfo['items']):
            print(f'  {color.CRED2}Warning: {color.CWHITE}No ' + \
                    f'{color.CCYAN}{str(self._cfgInfo["cfgMetadata"]["label"])} ' + \
                    f'{color.CWHITE}items provisioned!{color.CEND}')
            return

        self.show_table_header()
        self.show_item_data()

    def modify_value_by_qualifier(self, qualifier, value):
        if qualifier == 'timestamp':
            return value if not value else f'{datetime.fromtimestamp(value).strftime("%A, %B %d, %Y %I:%M:%S")}'
        return value


    def show_available_item_labels(self):
        if not len(self._cfgInfo['items']):
            print('No items defined, therefore no labels available to show!')
            return

        for label in self._cfgInfo['items'].keys():
            print(str(label), end=' ', flush=True)
        print()

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

