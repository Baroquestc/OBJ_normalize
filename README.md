# SimpleMesh

[TOC]

A simple mesh processing tool based on Trimesh for command line use.

## Overview

The program currently supports the following flags

`-i/--input`: input file name (required). _Added 2021/04/08_

`-I/--info`: display mesh info. _Added 2021/04/08_

`-r/--rotate`: rotate along either of the x, y, z axes by a certain degree. _Added 2021/04/08_

`-n/--normalize`: normalize the mesh by its bounding box. _Added 2021/04/08_

`-o/--output`: output the transformed mesh to a file. _Added 2021/04/08_

### Execution Sequence

The execution order of the corresponding commands is:

`-i/--input`

`-I/--info`

`-r/--rotate`

`-n/--normalize`

`-o/--output`

## Usage

### Input

Need not to explain.

### Info

Use `-I/--info` to display the info of the mesh. Currently supported:

- mesh bounding box

### Rotate

Use `-r/--rotate` for rotating the mesh. For example, to rotate around the x axis for 45 degrees:

```bash
python simplemesh.py --input input.obj -r x 45
```

You can rotate multiple times in a single command

```bash
python simplemesh.py --input input.obj -r x 45 y 70 z 25
```

### Normalize

Use `-n/--normalize` to normalize the mesh. For example, using

```bash
python simplemesh.py --input input.obj -n 0.8
```

will scale (isotropically) and translate the mesh so that its bounding box is $[-0.8, 0.8]^3$.