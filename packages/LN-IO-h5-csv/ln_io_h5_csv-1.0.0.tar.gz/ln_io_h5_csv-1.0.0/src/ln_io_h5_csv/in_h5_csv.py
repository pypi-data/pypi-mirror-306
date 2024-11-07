import asyncio
import glob
import numpy as np
import os

from livenodes import Ports_collection

from .abstract_in_h5_csv import Abstract_in_h5_csv
from ln_ports import Port_Timeseries, Port_Number, Port_ListUnique_Str


class Ports_out(Ports_collection):
    ts: Port_Timeseries = Port_Timeseries("TimeSeries")
    channels: Port_ListUnique_Str = Port_ListUnique_Str("Channel Names")
    annot: Port_Timeseries = Port_Timeseries("Annotation")
    percent: Port_Number = Port_Number("Percent")


class In_h5_csv(Abstract_in_h5_csv):
    """Reads and sends HDF5/.h5 data and corresponding .csv annotation.

    Each batch contains the entire dataset of a file. For custom batch sizes
    and real-time simulation use the `In_playback_h5_csv` node with its
    `emit_at_once` and `sample_rate` settings instead.

    Channels sent via the Channel Names port are named by priority:
        - List of names from meta parameter if given.
        - List of names from valid JSON file if found.
        - Otherwise ascending from "0".

    If a valid annotation CSV file with the same base name is found, its
    content is sent via the Annotation port. .h5 and .csv files created via
    the `Out_h5_csv` node automatically follow this format.

    After each file is processed, the Percent port is also updated accordingly.
    One common usage example is triggering model training once all files are
    sent.

    Attributes
    ----------
    files : str
        glob pattern for files to include. Should end with ".h5" extension.
        Common examples are single files ("../data/data.h5") or all files in a
        directory ("../data/*.h5").
    meta : dict
        Dict of meta parameters.

        * 'sample_rate' : int
            Sample rate to simulate.
        * 'channel_names' : list of unique str, optional
            List of channel names for `channels` port. Overwrites default names
            or those loaded from JSON file.

    Ports Out
    ---------
    ts : Port_TimeSeries
        HDF5/.h5 data file contents as TimeSeries.
    channels : Port_ListUnique_Str, optional
        List of channel names. Can be loaded from JSON file and/or overwritten
        using the `meta` attribute.
    annot : Port_TimeSeries, single channel
        Annotation strings corresponding to data samples. Only sent if valid
        .csv annotation file found. Otherwise empty.
    percent : Port_Number
        Percentage of files sent so far. Float values from 0.0 to 1.0.

    Raises
    ------
    ValueError
        If number of channel names from meta parameter or JSON file does not
        equal actual number of channels.
    """

    ports_out = Ports_out()

    example_init = {'name': 'In h5 CSV', 'files': 'data/*.h5', 'meta': {'channels': [""]}}

    def __init__(self, name="In h5 CSV", files='data', meta={}, **kwargs):
        super().__init__(name, files, meta, **kwargs)

    async def _async_run(self):
        files = glob.glob(self.files)
        n_files = len(files)
        self.info(f'Files found: {n_files}, {os.getcwd()}')

        for i, f in enumerate(files):
            self.info(f'Processing {f}')

            ts, channels, annot = self._read_data(f)

            channels = self._overwrite_channels(channels, ts.shape[1])

            annot = np.array(annot).reshape(-1, 1)

            percent = round((i + 1) / n_files, 2)

            yield self.ret(ts=ts, channels=channels, annot=annot, percent=percent)

            await asyncio.sleep(0)  # so other tasks can run
