try:

    import argparse
    import sys
    import globalvars as v


    #### PARSE THE INPUT

    parser = argparse.ArgumentParser()


    ## CREATE ACTION ARG
    parser.add_argument('action', help='task to perform', nargs='*', default='none')

    ## CREATEION ACTION SHORTS
    parser.add_argument('-q', help='no output except for errors; works on all actions', action='store_true')
    parser.add_argument('-Q', help='no output except strictly necessary; works on all actions', action='store_true')
    parser.add_argument('-s', help='get a server\'s status', dest='server')
    parser.add_argument('-t', help='follow a server\'s log file', action='store_true')
    parser.add_argument('-v', help='get gorp\'s version and install information', action='store_true')

    ## CREATE RUNTIME SHORTS
    parser.add_argument('-a', help='do on all servers; used on [start, stop, restart]', action='store_true')
    parser.add_argument('-f', help='skip backup; used on [stop, restart]', action='store_true')
    parser.add_argument('-n', help='skip backup and warning; used on [stop, restart]', action='store_true')
    parser.add_argument('-y', help='auto-accept world generation (skip prompt); used on [start]', action='store_true')
    parser.add_argument('-g', help='specify game version to download; used on [get-jar]', dest='gameversion')
    parser.add_argument('-u', help='download jar by at a url; used on [get-jar]', dest='url')

    ## PARSE ARGS
    args = parser.parse_args()







    #### STORE ACTION ARGS

    try:
        action = args.action[0]
    except IndexError:
        action = 'none'

    try:
        arg1 = args.action[1]
    except IndexError:
        arg1 = 'none'

    try:
        arg2 = args.action[2]
    except IndexError:
        arg2 = 'none'







    #### SET VERBOSITY

    global e
    global o

    if args.q:
        v.e = True
        v.o = False

    elif args.Q:
        v.e, v.o = False, False

    else:
        v.e, v.o = True, True








    #### LAUNCH ACTIONS


    ## START
    from mcstart import Start

    if action == 'start':
        Start(arg1, args.y)



except KeyboardInterrupt:
    print('User cancelled. Exit (19).')
    sys.exit(19)