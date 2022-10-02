import os
import subprocess
from typing import Dict, NamedTuple
import argparse
from lxml import etree
import pyparsing as pp


class SlideTuple(NamedTuple):
    start: int
    end: int
    list: list


def parse_slide_label(label: str):
    num = pp.Word(pp.nums).set_parse_action(lambda e: int(e[0]))
    spacing = pp.Optional(pp.White())
    slide_list = pp.delimited_list(num, ",")("list")
    slide_range = pp.Optional(num)("start") + pp.Suppress("-") + pp.Optional(num)("end")
    slide_expr = (
        pp.Suppress("<") + pp.Or([slide_list, slide_range]) + pp.Suppress(">")
    )("expr")
    slide_label = (
        spacing
        + pp.Optional(pp.Word(pp.printables, exclude_chars="<>") + spacing)
        + pp.Optional(slide_expr + spacing)
    )

    match_obj = slide_label.parse_string(label)
    if match_obj is None:
        raise RuntimeError(f"Syntax Error: slide label: {label}")

    match_dict: Dict[str, object] = match_obj.as_dict()

    if match_dict.get("expr") is not None:
        return SlideTuple(
            match_dict.get("start"), match_dict.get("end"), match_dict.get("list")
        )
    else:
        return None


def slide_match(slide_tuple: SlideTuple, slide_id: int):
    if slide_tuple.list and slide_id not in slide_tuple.list:
        return False
    if slide_tuple.start and slide_id < slide_tuple.start:
        return False
    if slide_tuple.end and slide_tuple.end < slide_id:
        return False

    return True


class LayerTuple(NamedTuple):
    layer: etree.Element
    slide_tuple: SlideTuple


def render(input_path: str, **kwargs):
    with open(input_path) as fp:
        doc = etree.parse(fp)

    layers = [
        LayerTuple(
            child,
            parse_slide_label(
                child.get("{http://www.inkscape.org/namespaces/inkscape}label")
            ),
        )
        for child in doc.getroot().getchildren()
        if child.tag == "{http://www.w3.org/2000/svg}g"
        and child.get("{http://www.inkscape.org/namespaces/inkscape}groupmode")
        == "layer"
    ]

    # get all slide ids
    slide_ids = set()
    for layer_tuple in layers:
        slide_tuple = layer_tuple.slide_tuple
        if slide_tuple is None:
            continue
        if slide_tuple.list:
            slide_ids.update(slide_tuple.list)
        if slide_tuple.start:
            slide_ids.add(slide_tuple.start)
        if slide_tuple.end:
            slide_ids.add(slide_tuple.end)

    for slide_id in slide_ids:
        base, _ = os.path.splitext(input_path)
        output_svg_path = base + f"-{slide_id}.svg"
        output_pdf_path = base + f"-{slide_id}.pdf"

        for layer_tuple in layers:
            if layer_tuple.slide_tuple is None:
                continue

            if slide_match(layer_tuple.slide_tuple, slide_id):
                layer_tuple.layer.attrib["style"] = "display:inline"
            else:
                layer_tuple.layer.attrib["style"] = "display:none"

        # output svg
        if kwargs["svg"]:
            with open(output_svg_path, "wb") as fp:
                fp.write(etree.tostring(doc))

        # output
        subprocess.run(
            f"inkscape --pipe {kwargs['inkscape_args']} -o {output_pdf_path}",
            input=etree.tostring(doc),
            shell=True,
            check=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("svg-slide-export.py")
    parser.add_argument("input", help="input svg path")
    parser.add_argument("--svg", action="store_true", default=False)
    parser.add_argument(
        "--inkscape-args",
        type=str,
        default="--export-type=pdf --export-text-to-path --export-background=white",
    )
    args = parser.parse_args()

    render(args.input, **vars(args))
