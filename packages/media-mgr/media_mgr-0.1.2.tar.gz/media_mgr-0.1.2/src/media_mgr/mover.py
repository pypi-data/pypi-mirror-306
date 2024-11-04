#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Media Relocation Methods
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from collections import defaultdict

import os

from quickcolor.color_def import color

from .comms_utility import run_cmd, is_server_active, group_list

from .media_cfg import MediaConfig
from .server_cfg import ServerConfig

from .search import find_items_in_search_paths

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def move_title(ipv4: str | None = None, searchTerms: str | None = None,
        fromBaseDir: str = "Movies", toBaseDir: str = "Primo-Movies",
        testMove: bool = False, debug: bool = False):

    if fromBaseDir == toBaseDir:
        print(f'\n{color.CRED2}-- Moving content from {color.CYELLOW2}{fromBaseDir} ' + \
                f'{color.CRED2}to {color.CYELLOW2}{toBaseDir} {color.CRED2}would ' + \
                f'be counter productive{color.CEND}!')
        return

    ipv4List = []
    if ipv4:
        ipv4List.append(ipv4)
    else:
        sc = ServerConfig()
        for srvName, srvCfg in sc.get_server_list():
            if srvCfg['serverType'] == 'plex':
                ipv4List.append(srvCfg['ipv4'])

    print("")
    for server in ipv4List:
        matched = []
        try:
            matched = find_items_in_search_paths(ipv4=server, searchPathList=None, searchTerms=searchTerms)

        except Exception as e:
            print(f'{color.CRED2}-- Processing error: Search aborted for ' + \
                    f'titles matching {color.CWHITE}--> {color.CYELLOW}' + \
                    f'{" ".join(searchTerms)} {color.CWHITE}<-- {color.CRED2}' + \
                    f'on {color.CWHITE}{server}\n{color.CRED2}   Investigate ' + \
                    f'{color.CWHITE}{server}{color.CRED2} for problems with ' + \
                    f'drive mounts!{color.CEND}\n{e}')
            return

        if not matched:
            test_move_msg = '(test move) ' if testMove else ''
            print(f'{color.CRED2}-- Did not find any titles matching ' + \
                    f'{color.CWHITE}--> {color.CYELLOW}{" ".join(searchTerms)}' + \
                    f'{color.CWHITE}<-- {color.CRED2}for {test_move_msg}' + \
                    f'relocation on {color.CWHITE}{server}{color.CEND}')
            continue

        failedToMoveMatch = False
        numMatchesMoved = 0
        for key in matched:
            for title in matched[key]:
                dirLabel = os.path.basename(key)
                dirRoot = os.path.dirname(key)
                if dirLabel == fromBaseDir:
                    fromPathAndFile = key + "/" + title
                    toPath = dirRoot + "/" + toBaseDir
                    toPathAndFile = toPath + "/" + title

                    if not run_cmd(ipv4=server, cmd="ls \"%s\"" % (fromPathAndFile)):
                        print(f'-- {color.CRED}could not find {color.CWHITE2}' + \
                                f'{fromPathAndFile}{color.CRED2} on ' + \
                                f'{color.CYELLOW}{server}{color.CEND}')
                        failedToMoveMatch = True
                        continue

                    if not run_cmd(ipv4=server, cmd="[[ -d \"%s\" ]] && echo -e \"Found %s\"" % (toPath, toPath)):
                        print(f'-- {color.CRED}could not find path ' + \
                                f'{color.CWHITE2}{toPath}{color.CRED} on ' + \
                                f'{color.CYELLOW}{server}{color.CEND}')
                        failedToMoveMatch = True
                        continue

                    if testMove:
                        pretext = 'testing move of '
                    else:
                        pretext = 'moving '

                    print(f'-- {pretext}{color.CYELLOW}{title}{color.CEND} ' + \
                            f'residing on {color.CRED2}{server}{color.CEND}')
                    print(f'      from: {color.CBLUE2}{key}{color.CEND}')
                    print(f'        to: {color.CBLUE}{dirRoot}/{toBaseDir}{color.CEND}')
                    print('')

                    if not testMove:
                        cmd = "mv \"%s\" \"%s\"" % (fromPathAndFile, toPathAndFile)
                        if debug:
                            print(f'... {color.CVIOLET2}running cmd:{color.CEND}\n{cmd}')
                        dumpThis = run_cmd(ipv4=server, cmd=cmd)
                        numMatchesMoved += 1

        if not testMove and numMatchesMoved == 0 and failedToMoveMatch == False:
            print(f'-- {color.CRED}could not find {color.CWHITE}any titles ' + \
                    f'{color.CRED}from path {color.CCYAN}{fromBaseDir} ' + \
                    f'{color.CRED} matching search terms ({color.CWHITE}' + \
                    f'{" ".join(searchTerms)}{color.CRED}) to move on ' + \
                    f'{color.CYELLOW}{server}{color.CEND}')

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

