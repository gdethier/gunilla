# Gunilla

## Introduction

Gunilla is a command-line Wordpress development tool. It creates a sandboxed Wordpress environment and allows, via the execution of
a single command line, to:

- deploy a local Wordpress installation for testing purposes,
- deploy a set of plugins and themes in the local Wordpress installation.

Gunilla also enables a prototype-based approach to custom Wordpress theme development:

1. you create/update a static clickable prototype with your favorite tools,
2. you validate it with your customer,
3. you generate the related theme using Gunilla,
4. you deploy in your local environment for testing,
5. finally, you push your theme wherever makes sense.

Each time you need to update your theme, just re-run above sequence.

So if you are:

- a Wordpress plugin developer,
- a Wordpress theme developer,
- someone who wants to play with existing themes and/or plugins on a fresh local installaton,

then Gunilla can help you.

## Usage

1. Run `gnl init`: this creates an empty Gunilla workspace which consists in a set of directories and the Gunilla file `gunilla.json'.
2. Update the Gunilla file by adding some plugins and themes (see below for a description of Gunilla file).
3. Run `gnl start` to run the local Wordpress installation.
4. Run `gnl deploy` to download and install the plugins and themes described in the Gunilla file.
