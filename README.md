# inkscape-slide

Generate slides from Inkscape SVG with LaTeX beamer overlay syntax[1].

## Usage

1. Create SVG with Inkscape
2. Append beamer overlay syntax to layer label
    - Only available for **top level** layers

```sh
python3 inkscape-slide.py ./example/sample.svg
```

```sh
# change output format
python3 inkscape-slide.py ./example/sample.svg --format '{0}-{1:03d}.png'
```

## Example

<img src="example/inkscape-screenshot.png" width="500px">

Output

|Slide 1|Slide 2|Slide 3|
|---|---|---|
|<img src="example/sample-1.png" width="150px">|<img src="example/sample-2.png" width="150px">|<img src="example/sample-3.png" width="150px">|

## Layer label syntax

```
<1>
item<1>
item<1,2>
item<1,2,3>
item<1-3>
item<1->
item<-3>
```

## References

- [1] [The beamer class User Guide for version 3.68.](http://tug.ctan.org/macros/latex/contrib/beamer/doc/beameruserguide.pdf) 3.10 Using Overlay Specifications
