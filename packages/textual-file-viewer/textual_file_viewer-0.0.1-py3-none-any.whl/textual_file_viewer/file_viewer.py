#!/home/pjhdekoning/.virtualenvs/file_viewer/bin/python
from pathlib import Path
from typing import Any

import PIL.Image
import numpy as np
import pandas
import pydicom
import typer
from pydicom.errors import InvalidDicomError
from pydicom.pixel_data_handlers import util
from rich.highlighter import RegexHighlighter
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container
from textual.widget import Widget
from textual.widgets import Header, Footer, ContentSwitcher, Label, TabbedContent, TabPane
from textual_pandas.widgets import DataFrameTable

from textual_file_viewer.image_viewer import ImageViewer

app = typer.Typer(add_completion=False, no_args_is_help=True)


SUPPORTED_PHOTOMETRIC_INTERPRETATIONS = {'MONOCHROME1', 'MONOCHROME2', 'YBR_FULL_422'}


class DicomHighlighter(RegexHighlighter):
    """Highlights the text produced by pydicom. """

    base_style = "repr."
    highlights = [
        r"(?P<tag_start>\()(?P<attrib_name>.{4}), (?P<attrib_value>.{4})(?P<tag_end>\)) (?P<str>.*) "
        r"(?P<none>([A-Z]{2})|([A-Z]{2}.[A-Z]{2})): (?P<number>.*)",
    ]


class Loading:
    def __init__(self, widget: Widget) -> None:
        self.widget = widget

    def __enter__(self) -> None:
        self.widget.loading = True

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.widget.loading = False


class FileViewer(App):
    CSS_PATH = 'file_viewer.tcss'

    def __init__(self, filename: Path) -> None:
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with ContentSwitcher(initial='dicom_viewer', id='content_switcher'):
            with TabbedContent(id='dicom_viewer'):
                with TabPane('Image', id='tab_image'):
                    yield ImageViewer(id='image_viewer')
                with TabPane('Tags', id='tab_tags'):
                    with ScrollableContainer():
                        yield Label(id='dicom_tags')
            with Container(id='dataframe_table'):
                yield DataFrameTable()
        yield Footer()

    async def on_mount(self) -> None:
        await self.update()

    async def update(self) -> None:
        try:
            self.query_one(DataFrameTable).add_df(pandas.read_excel(self.filename))
            self.query_one('#content_switcher', ContentSwitcher).current = 'dataframe_table'
            self.title = f'Excel: {self.filename}'  # type: ignore
            return
        except ValueError:
            pass

        try:
            await self._process_dicom()
            return
        except InvalidDicomError:
            pass

        raise RuntimeError('Could not determine file type.')

    async def _process_dicom(self) -> None:
        ds = pydicom.dcmread(self.filename, stop_before_pixels=True)
        self.title = f'DICOM: {self.filename}'  # type: ignore

        self.query_one('#dicom_tags', Label).update(DicomHighlighter()(str(ds)))
        self.query_one('#content_switcher', ContentSwitcher).current = 'dicom_viewer'
        self.query_one('#dicom_viewer', TabbedContent).active = 'tab_tags'

        if ds.PhotometricInterpretation not in SUPPORTED_PHOTOMETRIC_INTERPRETATIONS:
            self.notify(message=f'Only {" ".join(SUPPORTED_PHOTOMETRIC_INTERPRETATIONS)} are supported',
                        title='No image view',
                        severity='warning')
            return

        ds = pydicom.dcmread(self.filename)
        match len(ds.pixel_array.shape), ds.PhotometricInterpretation:
            case 4, 'YBR_FULL_422':
                self.notify(message='3D not fully supported, showing first slice', title='No image view',
                            severity='warning')
                np_array = ds.pixel_array[0]
            case 3, _:
                self.notify(message='3D not fully supported, showing first slice', title='No image view',
                            severity='warning')
                np_array = ds.pixel_array[0]
            case _:
                np_array = ds.pixel_array

        match ds.PhotometricInterpretation:
            case 'MONOCHROME1':
                # minimum is white, maximum is black
                # (https://dicom.innolitics.com/ciods/ct-image/image-pixel/00280004)
                np_array = pydicom.pixel_data_handlers.apply_voi_lut(ds.pixel_array, ds)
                minimum, maximum = np.amin(np_array), np.amax(np_array)
                np_array = (maximum - np_array) * 256.0 / (maximum - minimum)
            case 'MONOCHROME2':
                np_array = pydicom.pixel_data_handlers.apply_voi_lut(ds.pixel_array, ds)
                minimum, maximum = np.amin(np_array), np.amax(np_array)
                np_array = (np_array - minimum) * 256.0 / (maximum - minimum)
            case 'YBR_FULL_422':
                np_array = util.convert_color_space(np_array, 'YBR_FULL', 'RGB')
            case _:
                pass

        im = PIL.Image.fromarray(np_array).convert('RGB')  # type: ignore

        self.query_one('#image_viewer', ImageViewer).set_image(im)
        self.query_one('#dicom_viewer', TabbedContent).active = 'tab_image'
        return


@app.command()
def view(filename: Path) -> None:
    FileViewer(filename).run()


if __name__ == "__main__":
    app()
