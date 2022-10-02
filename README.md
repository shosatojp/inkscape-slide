# inkscape-slide

Generate slides from inkscape svg with LaTeX beamer overlay syntax.

## Usage

- Create SVG with Inkscape
- Append beamer overlay syntax to layer label
- Only available for **top level** layers

```sh
python3 inkscape-slide.py ./sample.svg
```


```sh
# change output format
python inkscape-slide.py example/sample.svg \
    --inkscape-args \
    '--export-type=png --export-text-to-path --export-background=white'
```

## Example

<img src="example/inkscape-screenshot.png" width="500px">

<img src="example/sample-1.png" width="150px">
<img src="example/sample-2.png" width="150px">
<img src="example/sample-3.png" width="150px">

## Syntax

```
<1>
item<1>
item<1,2>
item<1,2,3>
item<1-3>
item<1->
item<-3>
```
