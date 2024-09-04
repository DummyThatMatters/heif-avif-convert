#!/usr/bin/env python3


from pathlib import Path
from shutil import copystat
from heic_conv.static import EXT_RE, Formats, DEFAULT_EXTENSIONS, DEFAULT_QUALITY
import logging

from alive_progress import alive_it as progr
from PIL import Image
from PIL.ImageOps import exif_transpose
import pillow_heif
import click


def convert_file(in_file, out, quality, fmt):
    with Image.open(in_file) as image:
        heif = pillow_heif.from_pillow(exif_transpose(image))
        heif.save(out, quality=quality, format=fmt)


def parce_extension_list(ext_str: str):
    dedup = EXT_RE.sub(' ', ext_str)
    return {f'.{ext}' for ext in dedup.split()}


@click.command()
@click.option('--input', '-i', 'source_dir',
              type=click.Path(exists=True, file_okay=False, dir_okay=True,
                              resolve_path=True, allow_dash=False, path_type=Path),
              help='Path to folder with source images')
@click.option('--output', '-o', 'target_dir',
              type=click.Path(exists=False, file_okay=False, dir_okay=True,
                              resolve_path=True, allow_dash=False, path_type=Path),
              help='Path to folder where encoded images will be saved to')
@click.option('--quality', '-q', default=DEFAULT_QUALITY, show_default=True,
              help='Value from 1 to 100, that determines output file size/quality '
                   '(1: smallest file size, worst image quality; 100: largest file size, best image quality')
@click.option('--recursive', '-r',  is_flag=True, show_default=True, default=False,
              help='Process all files in target dir subfolders')
@click.option('--dir-tree', '-d', 'recreate_dirs', is_flag=True, show_default=True, default=False,
              help='Recreate all subfolders in output folder. Working oly in combination with "recursive" flag')
@click.option('--extensions', '-e', show_default=True, default=DEFAULT_EXTENSIONS,
              help='Process only files with these file extensions')
@click.option('--skip-stat', '-n', 'no_stat', is_flag=True, show_default=True, default=False,
              help='Do not copy original file creation/modification time')
@click.option('--avif', '-a', 'avif', is_flag=True, show_default=True, default=False,
              help='Use AVIF codec instead of HEIF')
@click.option('--silent', '-s', 'silent', is_flag=True, show_default=True, default=False,
              help='Recreate all subfolders in output folder. Working oly in combination with "recursive" flag')
def process(source_dir: Path, target_dir: Path,
            quality: int, recursive: bool, recreate_dirs: bool,
            extensions: str, no_stat: bool,
            avif: bool, silent: bool):

    logging_lvl = logging.CRITICAL if silent else logging.INFO
    logging.basicConfig(level=logging_lvl)

    codec = Formats.AVIF if avif else Formats.HEIF
    wildcard = '**/*' if recursive else '*'
    extensions = parce_extension_list(extensions)
    recreate_dirs = recursive and recreate_dirs

    filelist = [item for item in source_dir.glob(wildcard) if item.suffix in extensions]
    status = progr(filelist)
    for file in status:
        new_file_name = file.with_suffix(codec.ext).name
        status.text(f'Processing {new_file_name}')
        if recreate_dirs:
            new_path = Path(target_dir, file.parent.relative_to(source_dir)).resolve()
            new_path.mkdir(777, True, True)
        else:
            new_path = target_dir

        target_file = Path(new_path, new_file_name)

        logging.info('Output path: %s', target_file)
        try:
            convert_file(file, target_file, quality, codec.name)
            if not no_stat:
                copystat(file, target_file)
        except Exception as e:
            print('Error occurred!! Message: ', e)


if __name__ == '__main__':
    process()