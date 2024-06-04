# 42CTF Plugin

This ctfd plugin import new features to the platform.
It depends on the [42CTF theme](https://github.com/42CTF/42ctfd_theme). \
As the plugin is developed exclusively for the 42CTF platform, CTFd's team mode is not supported.

## Features

For now, the plugin adds the following features:
- Add a campuses model with a relationship between users and campus
- Add a campuses scoreboard
- Add an admin page to add and manage campuses

## Subtree Installation

### Add repo to themes folder

```
git subtree add --prefix CTFd/plugins/42ctf git@github.com:42CTF/42ctfd_plugin.git main --squash
```

### Pull latest changes to subtree
```
git subtree pull --prefix CTFd/plugins/42ctf git@github.com:42CTF/42ctfd_plugin.git main --squash
```

### Subtree Gotcha

Make sure to use Merge Commits when dealing with the subtree here. For some reason Github's squash and commit uses the wrong line ending which causes issues with the subtree script: https://stackoverflow.com/a/47190256. 
