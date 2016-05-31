# Continous tool for working with git

By [Claudio Walser]

## Description
**gitcd** gitcd is a little helper for continous integration workflows using git as scm.

## Installation for python 3

Run the following command to install prerequisites:

```console
pip install pyyaml
pip install argcomplete
```

Run the following command to install argument completion on linux:

```console
pip install pyyaml
pip install argcomplete
```

Run the generator:

```console
rails generate my_example_gem:install
```


## Usage

Usage explanation goes here

```erb
<%= your_code_goes @here do |f| %>
  <%= f.input :example %>
  <%= f.input :example %>
  <%= f.button :example %>
<% end %>
```


## Configuration

This block of text should explain how to configure your application:

`rails generate my_example_gem:install`


## Information

Screenshots of your application below:

![Screenshot 1](http://placekitten.com/400/300)

![Screenshot 2](http://placekitten.com/400/300)


### Known Issues

If you discover any bugs, feel free to create an issue on GitHub fork and
send us a pull request.

[Issues List](Github Issues List URL goes here).

## Authors

* Your Name (Your Github URL goes here)
* Additional Author's name (Their Github URL goes here)


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


## License

Your Licensing Information goes here. Example: MIT/X11.


Readme File

pip install argcomplete
pip install pyyaml

Init config file
gitcd init

Start new feature
gitcd feature start <branchname>
Starts a new feature branch from your master branch

Test a feature branch
gitcd feature test <branchname>
Merges a feature branch into your development branch

Open a pull request for code review
gitcd feature review <branchname>
Opens a pull request to your master branch - not working yet

Finish a feature branch
gitcd feature finish <branchname>
Merges it into your master and create a tag of the current master code