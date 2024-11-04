NAME

::

    OPD - Original Programmer Daemon


SYNOPSIS

::

    opdctl <cmd> [key=val] [key==val]


DESCRIPTION

::

    OPD has all the python3 code to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    OPD uses object programming (OP) that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.

    OPD has a demo bot, it can connect to IRC, fetch and display RSS
    feeds, take todo notes, keep a shopping list and log text. You can
    also copy/paste the service file and run it under systemd for 24/7
    presence in a IRC channel.

    OPD is Public Domain.


INSTALL

::

    $ pipx install opd
    $ pipx ensurepath

    <new terminal>

    $ opdctl srv > opd.service
    # mv *.service /etc/systemd/system/
    # systemctl enable opd --now

    joins #opd on localhost


USAGE

::

    without any argument the bot does nothing::

    $ opdctl
    $

    see list of commands

    $ opdctl cmd
    cfg,cmd,dne,dpl,err,exp,fnd,imp,log,mod,mre,nme,pwd
    rem,res,rss,srv,syn,tdo,thr,upt

    start daemon

    $ opd
    $

    start service

    $ opds
    <runs until ctrl-c>


CONFIGURATION

::

    irc

    $ opdctl cfg server=<server>
    $ opdctl cfg channel=<channel>
    $ opdctl cfg nick=<nick>

    sasl

    $ opdctl pwd <nsvnick> <nspass>
    $ opdctl cfg password=<frompwd>

    rss

    $ opdctl rss <url>
    $ opdctl dpl <url> <item1,item2>
    $ opdctl rem <url>
    $ opdctl nme <url> <name>


COMMANDS

::

    cfg - irc configuration
    cmd - commands
    dpl - sets display items
    err - show errors
    exp - export opml (stdout)
    imp - import opml
    log - log text
    mre - display cached output
    now - show genocide stats
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    res - restore deleted feeds
    req - reconsider
    rss - add a feed
    syn - sync rss feeds
    tdo - add todo item
    thr - show running threads
    upt - show uptime


FILES

::

    ~/.opd
    ~/.local/bin/opdctl
    ~/.local/bin/opd
    ~/.local/bin/opds
    ~/.local/pipx/venvs/opd/*


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    OPD is Public Domain.
