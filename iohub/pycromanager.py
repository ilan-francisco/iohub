import numpy as np
import zarr
from waveorder.io.reader_base import ReaderBase
from pycromanager import Dataset


class PycromanagerReader(ReaderBase):

    def __init__(self, data_path: str):
        """

        """

        self.dataset = Dataset(data_path)
        self._axes = self.dataset.axes

        self.frames = len(self._axes['time']) if 'time' in self._axes.keys() else 1
        self.channels = len(self._axes['channel']) if 'channel' in self._axes.keys() else 1
        self.slices = len(self._axes['z']) if 'z' in self._axes.keys() else 1
        self.height = self.dataset.image_height
        self.width = self.dataset.image_width
        self.mm_meta = self.dataset.summary_metadata

        self.channel_names = list(self.dataset.get_channel_names())

    def get_num_positions(self) -> int:
        return self.len(self._axes['position']) if 'position' in self._axes.keys() else 1

    def get_image(self, p, t, c, z) -> np.ndarray:
        image = None

        if self.dataset.has_image(position=p, time=t, channel=c, z=z):
            image = self.dataset.read_image(position=p, time=t, channel=c, z=z)

        return image

    def get_zarr(self, position: int) -> zarr.array:
        # data is a Dask array
        data = self.dataset.as_array(axes=['position', 'time', 'channel', 'z'], position=position)

        return data.to_zarr()

    def get_array(self, position: int) -> np.ndarray:
        return np.asarray(self.get_zarr(position))
