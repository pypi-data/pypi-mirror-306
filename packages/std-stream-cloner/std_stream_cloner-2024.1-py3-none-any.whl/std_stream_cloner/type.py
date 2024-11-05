"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2020
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import os as opsy
import sys as sstm
import tempfile as tmpf
import typing as h
from pathlib import Path as path_t

AUTO_STREAM_FILE = "auto"

tmp_file_t = tmpf._TemporaryFileWrapper

stream_names_h = h.Literal["out", "err", "both"]
operation_h = h.Literal["pause", "resume"]
where_h = h.Literal["stream", "log"]


@d.dataclass(slots=True, repr=False, eq=False)
class _clone_t:

    name: str
    path: str | path_t
    accessor: h.TextIO | None = None
    #
    original: h.TextIO = d.field(init=False)
    PrintToStreamOnly: h.Callable[[str], int] = d.field(init=False)
    #
    _keep_alive: tmp_file_t = d.field(init=False)
    _latest_newline_position: int | None = d.field(init=False, default=None)

    def __post_init__(self) -> None:
        """"""
        if self.name == "out":
            self.original = sstm.stdout
        else:
            self.original = sstm.stderr
        self.PrintToStreamOnly = self.original.write

        if self.path == AUTO_STREAM_FILE:
            self._keep_alive = tmpf.NamedTemporaryFile(
                mode="w+", prefix="stream-clone_", suffix=".log", delete=False
            )
            self.accessor = self._keep_alive.file
            self.path = path_t(self._keep_alive.name)
        elif self.accessor is None:
            self.path = path_t(self.path)
            if self.path.exists() and not self.path.is_file():
                raise ValueError(
                    f'Path "{self.path}" exists and is not a regular file.'
                )

            if self.path.exists():
                mode = "a+"
            else:
                mode = "w+"
            self.accessor = open(self.path, mode)

        self.ResumeCloning()

    def PauseCloning(self) -> None:
        """"""
        if self.name == "out":
            sstm.stdout = self.original
        else:
            sstm.stderr = self.original

    def ResumeCloning(self) -> None:
        """"""
        # To start cloning with an empty stream.
        self.flush()

        if self.name == "out":
            sstm.stdout = self
        else:
            sstm.stderr = self

    def PrintToLogOnly(self, text: str, /) -> int:
        """"""
        text = text.replace("\a", "")
        for move in ("\f", "\v"):
            if move in text:
                text = text.replace(move, "\n")

        if text.startswith("\r"):
            text = text[1:]
            if self._latest_newline_position is not None:
                self.accessor.seek(
                    self._latest_newline_position + 1,
                    opsy.SEEK_SET,
                )
        elif text.startswith("\b"):
            length_before = text.__len__()
            text = text.lstrip("\b")
            length_after = text.__len__()
            self.accessor.seek(length_after - length_before, opsy.SEEK_CUR)

        set_position = False
        rewind_length = 0
        if text.endswith("\b"):
            length_before = text.__len__()
            text = text.rstrip("\b")
            length_after = text.__len__()
            rewind_length = length_after - length_before
        elif text.endswith("\r"):
            text = text[:-1]
            set_position = True

        output = text.__len__()
        if output > 0:
            for unwanted, replacement in zip(("\r", "\b"), ("⇦", "←")):
                if unwanted in text:  # Should not happen
                    text = text.replace(unwanted, replacement)
            self._UpdateLatestNewlinePosition(text)
            self.accessor.write(text)

        if rewind_length < 0:
            self.accessor.seek(rewind_length, opsy.SEEK_CUR)
        elif set_position and (self._latest_newline_position is not None):
            self.accessor.seek(self._latest_newline_position + 1, opsy.SEEK_SET)

        return output

    def _UpdateLatestNewlinePosition(self, text: str, /) -> None:
        """
        Must be called before writing to log file so that file descriptor has not moved
        yet.
        """
        newline_position = text.rfind("\n")
        if newline_position != -1:
            current_position = self.accessor.seek(0, opsy.SEEK_CUR)
            self._latest_newline_position = current_position + newline_position

    def write(self, text: str, /) -> int:
        """"""
        output = self.original.write(text)
        _ = self.PrintToLogOnly(text)

        return output

    def flush(self) -> None:
        """"""
        self.original.flush()
        self.accessor.flush()


@d.dataclass(slots=True, repr=False, eq=False)
class stream_cloner_t:

    clone_out: _clone_t | None = None
    clone_err: _clone_t | None = None

    def Start(
        self,
        *,
        out: str | path_t | None = None,
        err: str | path_t | None = None,
        both: str | path_t | None = AUTO_STREAM_FILE,
    ) -> None:
        """"""
        if (out is None) and (err is None) and (both is None):
            raise ValueError("No stream specified.")
        if (both is not None) and not ((out is None) and (err is None)):
            raise ValueError('Stream(s) specified individually and with "both".')

        if out is not None:
            self.clone_out = _clone_t("out", out)
        if err is not None:
            if err == out:
                raise ValueError("Output and error streams have identical paths.")
            self.clone_err = _clone_t("err", err)
        if both is not None:
            self.clone_out = _clone_t("out", both)
            self.clone_err = _clone_t(
                "err", self.clone_out.path, accessor=self.clone_out.accessor
            )

    def Pause(self, which: stream_names_h | None = None) -> None:
        """"""
        self._PauseOrResume(which, "pause")

    def Resume(self, which: stream_names_h | None = None) -> None:
        """"""
        self._PauseOrResume(which, "resume")

    def PrintToStreamOnly(
        self, text: str, /, *, which: stream_names_h | None = None
    ) -> int:
        """"""
        return self._PrintToEither(text, which, "stream")

    def PrintToLogOnly(
        self, text: str, /, *, which: stream_names_h | None = None
    ) -> int:
        """"""
        return self._PrintToEither(text, which, "log")

    def _PauseOrResume(
        self, which: stream_names_h | None, operation: operation_h, /
    ) -> None:
        """"""
        if operation == "pause":
            method = "PauseCloning"
        else:
            method = "ResumeCloning"

        if which is None:
            if self.clone_out is not None:
                getattr(self.clone_out, method)()
            if self.clone_err is not None:
                getattr(self.clone_err, method)()
            return

        if which in ("out", "both"):
            if self.clone_out is None:
                raise ValueError("Requesting resuming of un-cloned output stream.")
            getattr(self.clone_out, method)()
        if which in ("err", "both"):
            if self.clone_err is None:
                raise ValueError("Requesting resuming of un-cloned error stream.")
            getattr(self.clone_err, method)()

    def _PrintToEither(
        self,
        text: str,
        which: stream_names_h | None,
        where: where_h,
        /,
    ) -> int:
        """"""
        if where == "stream":
            method = "PrintToStreamOnly"
        else:
            method = "PrintToLogOnly"

        output = 0

        if which is None:
            if self.clone_out is not None:
                output = getattr(self.clone_out, method)(text)
            if self.clone_err is not None:
                output = getattr(self.clone_err, method)(text)
            return output

        if which in ("out", "both"):
            if self.clone_out is None:
                raise ValueError("Requesting resuming of un-cloned output stream.")
            output = getattr(self.clone_out, method)(text)
        if which in ("err", "both"):
            if self.clone_err is None:
                raise ValueError("Requesting resuming of un-cloned error stream.")
            output = getattr(self.clone_err, method)(text)

        return output

    def __del__(self) -> None:
        """"""
        if self.clone_out is None:
            path_out = None
        else:
            self.clone_out.PauseCloning()
            path_out = self.clone_out.path
        if self.clone_err is None:
            path_err = None
        else:
            self.clone_err.PauseCloning()
            path_err = self.clone_err.path

        if (path_out == path_err) and (path_out is not None):
            print(f"Stdout and stderr clones at {path_out}")
        else:
            if path_out is not None:
                print(f"Stdout clone at {path_out}")
            if path_err is not None:
                print(f"Stderr clone at {path_err}")


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
