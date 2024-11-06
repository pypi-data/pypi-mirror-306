from yta_general_utils.file.filename import ensure_file_extension, file_has_extension
from yta_general_utils.temp import create_temp_filename
from typing import Union


def handle_output_filename(output_filename: Union[None, str], expected_extension: Union[None, str]):
    """
    Handle the provided 'output_filename' to ensure that it is the
    expected for our system. We could want to write a file or to not
    write it, and we need to make sure the extension is the expected
    one.

    This method should be called within any method that is capable
    to write (mandatory or optional) a filename locally.

    This method will return None when no file writting expected or
    the expected filename when you do want to write.
    """
    # TODO: Maybe change the 'expected_extension' to a Enum that
    # can handle FileType or FileExtension, so we can tell the
    # method that the 'output_filename' is expected to be an image
    # so if '.jpg' provided, we don't force it to be '.png' if 
    # FileType.IMAGE provided, so we can use it in a better way
    # because the 'output_filename' could be 'jpg', 'png', 'bmp'
    # and if I use the current 'expected_extension' I will be 
    # forcing it to the one I want and this is not ok
    if not expected_extension and not output_filename:
        return None

    if output_filename is not None and not isinstance(output_filename, str):
        raise Exception(f'The provided "output_filename" parameter "{str(output_filename)}" is not a string.')
    
    if expected_extension is not None and not isinstance(expected_extension, str):
        raise Exception(f'The provided "expected_extension" parameter "{str(expected_extension)}" is not None but also it is not a string.')
    
    # We don't accept 'output_filename' without extension
    if not expected_extension and not file_has_extension(output_filename):
        raise Exception(f'The provided "output_filename" parameter "{str(output_filename)}" has no valid extension and there is no "expected_extension" parameter provided.')
    
    if expected_extension:
        # TODO: Maybe validate that 'expected_extension' is a valid extension (?)
        expected_extension = expected_extension.replace('.', '')
        if not output_filename:
            output_filename = create_temp_filename(f'tmp_filename.{expected_extension}')
        else:
            output_filename = ensure_file_extension(output_filename, expected_extension)

    return output_filename