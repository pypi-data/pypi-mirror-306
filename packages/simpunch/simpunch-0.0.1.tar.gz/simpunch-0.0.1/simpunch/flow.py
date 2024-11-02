"""Run the entire pipeline backward."""
import glob
import os
import shutil
from datetime import datetime

from prefect import flow

from simpunch.level0 import generate_l0_all
from simpunch.level1 import generate_l1_all
from simpunch.level2 import generate_l2_all
from simpunch.level3 import generate_l3_all


@flow(log_prints=True)
def generate_flow(gamera_directory: str,
                  output_directory: str,
                  psf_model_path: str,
                  wfi_vignetting_model_path: str,
                  nfi_vignetting_model_path: str,
                  num_repeats: int = 1,
                  start_time: datetime | None = None,
                  transient_probability: float = 0.03,
                  update_database: bool = True) -> None:
    """Generate all the products in the reverse pipeline."""
    if start_time is None:
        start_time = datetime.now()  # noqa: DTZ005

    generate_l3_all(gamera_directory, start_time, num_repeats=num_repeats)
    generate_l2_all(gamera_directory)
    generate_l1_all(gamera_directory)
    generate_l0_all(gamera_directory, psf_model_path, wfi_vignetting_model_path, nfi_vignetting_model_path,
                    transient_probability=transient_probability)

    if update_database:
        from punchpipe import __version__
        from punchpipe.controlsegment.db import File
        from punchpipe.controlsegment.util import get_database_session
        db_session = get_database_session()
        for file_path in sorted(glob.glob(os.path.join(gamera_directory, "synthetic_l0/*v[0-9].fits")),
                                key=lambda s: os.path.basename(s)[13:27]):
            file_name = os.path.basename(file_path)
            level = "0"
            file_type = file_name[9:11]
            observatory = file_name[11]
            year = file_name[13:17]
            month = file_name[17:19]
            day = file_name[19:21]
            hour = file_name[21:23]
            minute = file_name[23:25]
            second = file_name[25:27]
            dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
            version = file_name.split(".fits")[0].split("_")[-1][1:]

            output_dir = os.path.join(output_directory, level, file_type+observatory, year, month, day)
            os.makedirs(output_dir, exist_ok=True)
            shutil.copy(file_path, os.path.join(output_dir, file_name))

            db_entry = File(
                level=0,
                file_type=file_type,
                observatory=observatory,
                file_version=version,
                software_version=__version__,
                date_obs=dt,
                polarization=file_type[1],
                state="created",
            )
            db_session.add(db_entry)
            db_session.commit()
