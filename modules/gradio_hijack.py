"""gr.Image() component wrapper for Gradio 6.x compatibility."""

from __future__ import annotations

import importlib
import gradio
import gradio.routes

import gradio as gr
from gradio.blocks import Block


all_components = []

if not hasattr(Block, 'original_init'):
    Block.original_init = Block.__init__


def blk_ini(self, *args, **kwargs):
    all_components.append(self)
    return Block.original_init(self, *args, **kwargs)


Block.__init__ = blk_ini


gradio.routes.asyncio = importlib.reload(gradio.routes.asyncio)

if not hasattr(gradio.routes.asyncio, 'original_wait_for'):
    gradio.routes.asyncio.original_wait_for = gradio.routes.asyncio.wait_for


def patched_wait_for(fut, timeout):
    del timeout
    return gradio.routes.asyncio.original_wait_for(fut, timeout=65535)


gradio.routes.asyncio.wait_for = patched_wait_for


class Image(gr.Image):
    """
    Wrapper around gr.Image that maintains backwards compatibility with the
    Gradio 3.x/4.x API used throughout Fooocus (e.g. source= instead of
    sources=).  Parameters that were removed in Gradio 5/6 are silently
    accepted and ignored.  The sketch/mask tool parameter is deprecated; use
    gr.ImageEditor for drawing functionality instead.
    """

    def __init__(
        self,
        value=None,
        *,
        shape=None,
        height=None,
        width=None,
        image_mode="RGB",
        invert_colors=False,
        source="upload",
        tool=None,
        type="numpy",
        label=None,
        every=None,
        show_label=None,
        show_download_button=True,   # removed in Gradio 5/6 – accepted but ignored
        container=True,
        scale=None,
        min_width=160,
        interactive=None,
        visible=True,
        streaming=False,
        elem_id=None,
        elem_classes=None,
        mirror_webcam=True,          # removed in Gradio 5/6 – accepted but ignored
        brush_radius=None,
        brush_color="#000000",
        mask_opacity=0.7,
        show_share_button=None,      # removed in Gradio 5/6 – accepted but ignored
        **kwargs,
    ):
        # Map the Gradio 3.x source= string to the Gradio 6.x sources= list.
        sources = [source] if source else ["upload"]

        if tool is not None:
            import warnings
            warnings.warn(
                "The 'tool' parameter is deprecated and no longer supported. "
                "Use gr.ImageEditor for sketch/masking functionality.",
                DeprecationWarning,
                stacklevel=2,
            )

        super().__init__(
            value=value,
            height=height,
            width=width,
            image_mode=image_mode,
            sources=sources,
            type=type,
            label=label,
            every=every,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            streaming=streaming,
            elem_id=elem_id,
            elem_classes=elem_classes,
            **kwargs,
        )
