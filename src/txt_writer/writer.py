import os
from types import TracebackType


class TxtWriter:
    """
    A class for writing text files.

    Attributes:
    ----------
    output_path: str
        The path to the output file.
    is_reset_enabled: bool
        Whether to reset the file.
    file: file
        The text file object.
    flush_counter: int
        The counter to flush the file.
    flush_frequency: int
        The frequency to flush the file.
    """
    def __init__(
        self, 
        output_path: str, 
        is_reset_enabled: bool = False,
        flush_frequency: int = 1000
        ):
        """
        Initialize the TxtWriter.
        
        Parameters:
        ----------
        output_path: str
            The path to the output file.
        is_reset_enabled: bool
            Whether to reset the file.
        flush_frequency: int
            The frequency to flush the file.
        """
        if flush_frequency <= 0:
            raise ValueError("flush_frequency must be greater than 0")
        dir_ = os.path.dirname(output_path)
        if dir_ and not os.path.exists(dir_):
            os.makedirs(dir_, exist_ok=True)
        self.output_path = output_path
        if is_reset_enabled:
            self.file = open(output_path, "w")
        else:
            self.file = open(output_path, "a")
        self.flush_counter = 0
        self.flush_frequency = flush_frequency

    def write(
        self, 
        txt: str, 
        is_new_line: bool = False
        ) -> None:
        """
        Write a string to the file.

        Parameters:
        ----------
        txt: str
            The string to write.
        is_new_line: bool
            Whether to add a new line.
        """

        if is_new_line and not txt.endswith("\n"):
            txt += "\n"
        self.file.write(txt)
        self.flush_counter = (self.flush_counter + 1) % self.flush_frequency
        if self.flush_counter == 0:
            self.file.flush()

    def close(self) -> None:
        file = getattr(self, "file", None)
        if file is not None and not file.closed:
            file.close()

    def __str__(self) -> str:
        return f"TxtWriter(output_path={self.output_path})"
    
    def __del__(self):
        self.close()
    
    def __enter__(self):
        return self
    
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()