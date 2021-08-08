# Purpose

The tools in this package are meant for two purposes:

* day-in-day-out use in my home directory on a few familiar machines;
* drop-in use on machines I don't regularly visit.

The intent of this package in the latter is to make myself at home, and
productive, as quickly as possible: a **suitcase**, or a toolbox.
(See also https://github.com/johnkerl/away which is simpler.)

What makes a house a home?  A home environment consists of (at
least)

* executables
* aliases
* `$PATH`
* `$PS1`
* various environment variables such as `export vlp=/very/long/path/goes/here/so/I/need/not/type/it/each/time`
* editor setup

Moreover, items in my suitcase fall into two categories: (a) always useful; (b)
per-project useful. The `aux` subdirectory is for the latter.

# Suitcase setup on the home machine

```
# Set up always-useful things
rm -rf ./scripts
git clone http://github.com/johnkerl/scripts
rm -rf ./scripts/.git # Prune for quicker scp

# Add in per-project useful things
cp something-or-other scripts/aux
cp somedir/*          scripts/aux
echo "export vlp= /very/long/path/goes/here/so/I/need/not/type/it/each/time" >> scripts/aux/rc
echo 'alias  vlp="cd $vlp; "'  >> scripts/aux/rc
```

# Shipping the suitcase

```
scp -C -r scripts user@away-machine.domain.name:/path/over/there/scripts
```

# Suitcase unpack on the away machine

```
eval $(/path/over/there/scripts/rc)
```

If I've access to a persistent `~/.bashrc` on the away machine I can add this to it:

```
if [ -f ~/scripts/rc ]; then
  eval $(~/scripts/rc)
fi
```

----------------------------------------------------------------

John Kerl 2013-10-04
