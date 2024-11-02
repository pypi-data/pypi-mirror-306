"""Generate synthetic level 2 data.

PTM - PUNCH Level-2 Polarized (MZP) Mosaic
"""
import glob
import os

import astropy.time
import astropy.units as u
import numpy as np
import solpolpy
from astropy.table import QTable
from astropy.wcs import WCS
from ndcube import NDCollection, NDCube
from photutils.datasets import make_gaussian_sources_image, make_noise_image
from prefect import flow, task
from prefect.futures import wait
from prefect_dask import DaskTaskRunner
from punchbowl.data import (NormalizedMetadata, get_base_file_name,
                            load_ndcube_from_fits, write_ndcube_to_fits)
from punchbowl.data.wcs import calculate_celestial_wcs_from_helio
from tqdm import tqdm

from simpunch.stars import (filter_for_visible_stars, find_catalog_in_image,
                            load_raw_hipparcos_catalog)
from simpunch.util import update_spacecraft_location


def get_fcorona_parameters(date_obs: astropy.time.Time) -> dict[str, float]:
    """Get time dependent F corona model parameters."""
    phase = date_obs.decimalyear - int(date_obs.decimalyear)

    tilt_angle = 3 * u.deg * np.sin(phase * 2 * np.pi)
    b = 300. + 50 * np.cos(phase * 2 * np.pi)

    return {"tilt_angle": tilt_angle,
            "b": b}


def generate_fcorona(shape: (int, int),
                     tilt_angle: float = 3*u.deg,
                     a: float = 600.,
                     b: float = 300.,
                     tilt_offset: tuple[float] = (0,0)) -> np.ndarray:
    """Generate an F corona model."""
    fcorona = np.zeros(shape)

    if len(shape) > 2:  # noqa: PLR2004
        xdim = 1
        ydim = 2
    else:
        xdim = 0
        ydim = 1

    x, y = np.meshgrid(np.arange(shape[xdim]), np.arange(shape[ydim]))
    x_center, y_center = shape[xdim] // 2 + tilt_offset[0], shape[ydim] // 2 + tilt_offset[1]

    x_rotated = (x - x_center) * np.cos(tilt_angle) + (y - y_center) * np.sin(tilt_angle) + x_center
    y_rotated = -(x - x_center) * np.sin(tilt_angle) + (y - y_center) * np.cos(tilt_angle) + y_center

    distance = np.sqrt(((x_rotated - x_center) / a) ** 2 + ((y_rotated - y_center) / b) ** 2)

    max_radius = np.sqrt((shape[xdim] / 2) ** 2 + (shape[ydim] / 2) ** 2)
    min_n = 1.54
    max_n = 1.65

    n = min_n + (max_n - min_n) * (distance / max_radius)

    superellipse = (np.abs((x_rotated - x_center) / a) ** n +
                    np.abs((y_rotated - y_center) / b) ** n) ** (1 / n) / (2 ** (1 / n))

    max_distance = 1
    fcorona_profile = np.exp(-superellipse ** 2 / (2 * max_distance ** 2))

    fcorona_profile = fcorona_profile / fcorona_profile.max() * 1e-12

    if len(shape) > 2:  # noqa: PLR2004
        for i in np.arange(fcorona.shape[0]):
            fcorona[i, :, :] = fcorona_profile[:, :]
    else:
        fcorona[:,:] = fcorona_profile[:,:]

    return fcorona


def add_fcorona(input_data: NDCube) -> NDCube:
    """Add synthetic f-corona model."""
    fcorona_parameters = get_fcorona_parameters(input_data.meta.astropy_time)

    fcorona = generate_fcorona(input_data.data.shape, **fcorona_parameters)

    fcorona = fcorona * (input_data.data != 0)

    input_data.data[...] = input_data.data[...] + fcorona

    return input_data


def generate_starfield(wcs: WCS,
                       img_shape: (int, int),
                       fwhm: float,
                       wcs_mode: str = "all",
                       mag_set: float = 0,
                       flux_set: float = 500_000,
                       noise_mean: float | None = 25.0,
                       noise_std: float | None = 5.0,
                       dimmest_magnitude: float = 8) -> (np.ndarray, QTable):
    """Generate a realistic starfield."""
    sigma = fwhm / 2.355

    catalog = load_raw_hipparcos_catalog()
    filtered_catalog = filter_for_visible_stars(catalog,
                                                dimmest_magnitude=dimmest_magnitude)
    stars = find_catalog_in_image(filtered_catalog,
                                  wcs,
                                  img_shape,
                                  mode=wcs_mode)
    star_mags = stars["Vmag"]

    sources = QTable()
    sources["x_mean"] = stars["x_pix"]
    sources["y_mean"] = stars["y_pix"]
    sources["x_stddev"] = np.ones(len(stars)) * sigma
    sources["y_stddev"] = np.ones(len(stars)) * sigma
    sources["flux"] = flux_set * np.power(10, -0.4 * (star_mags - mag_set))
    sources["theta"] = np.zeros(len(stars))

    fake_image = make_gaussian_sources_image(img_shape, sources)
    if noise_mean is not None and noise_std is not None:  # we only add noise if it's specified
        fake_image += make_noise_image(img_shape, "gaussian", mean=noise_mean, stddev=noise_std)

    return fake_image, sources


def add_starfield_polarized(input_data: NDCube) -> NDCube:
    """Add synthetic starfield."""
    wcs_stellar_input = calculate_celestial_wcs_from_helio(input_data.wcs,
                                                           input_data.meta.astropy_time,
                                                           input_data.data.shape)

    starfield, stars = generate_starfield(wcs_stellar_input, input_data.data[0, :, :].shape, flux_set=2.0384547E-9,
                                          fwhm=3, dimmest_magnitude=12, noise_mean=0, noise_std=0)

    starfield_data = np.zeros(input_data.data.shape)
    for i in range(starfield_data.shape[0]):
        starfield_data[i, :, :] = starfield * (np.logical_not(np.isclose(input_data.data[i, :, :], 0, atol=1E-18)))

    input_data.data[...] = input_data.data[...] + starfield_data

    return input_data


def add_starfield_clear(input_data: NDCube) -> NDCube:
    """Add synthetic starfield."""
    wcs_stellar_input = calculate_celestial_wcs_from_helio(input_data.wcs,
                                                           input_data.meta.astropy_time,
                                                           input_data.data.shape)

    starfield, stars = generate_starfield(wcs_stellar_input, input_data.data[:, :].shape, flux_set=2.0384547E-9,
                                          fwhm=3, dimmest_magnitude=12, noise_mean=0, noise_std=0)

    starfield_data = np.zeros(input_data.data.shape)
    starfield_data[:, :] = starfield * (np.logical_not(np.isclose(input_data.data[:, :], 0, atol=1E-18)))

    input_data.data[...] = input_data.data[...] + starfield_data

    return input_data


def remix_polarization(input_data: NDCube) -> NDCube:
    """Remix polarization from (B, pB) to (M,Z,P) using solpolpy."""
    # Unpack data into a NDCollection object
    data_collection = NDCollection(
        [("B", NDCube(data=input_data.data[0], wcs=input_data.wcs)),
         ("pB", NDCube(data=input_data.data[1], wcs=input_data.wcs))],
        aligned_axes="all")

    resolved_data_collection = solpolpy.resolve(data_collection, "MZP", imax_effect=False)

    # Repack data
    data_list = []
    wcs_list = []
    uncertainty_list = []
    for key in resolved_data_collection:
        data_list.append(resolved_data_collection[key].data)
        wcs_list.append(resolved_data_collection[key].wcs)
        uncertainty_list.append(resolved_data_collection[key].uncertainty)

    # Remove alpha channel
    data_list.pop()
    wcs_list.pop()
    uncertainty_list.pop()

    # Repack into a PUNCHData object
    new_data = np.stack(data_list, axis=0)
    if uncertainty_list[0] is not None:  # noqa: SIM108
        new_uncertainty = np.stack(uncertainty_list, axis=0)
    else:
        new_uncertainty = None

    new_wcs = input_data.wcs.copy()

    return NDCube(data=new_data, wcs=new_wcs, uncertainty=new_uncertainty, meta=input_data.meta)

@task
def generate_l2_ptm(input_file: str, path_output: str) -> None:
    """Generate level 2 PTM synthetic data."""
    # Read in the input data
    input_pdata = load_ndcube_from_fits(input_file)

    # Define the output data product
    product_code = "PTM"
    product_level = "2"
    output_meta = NormalizedMetadata.load_template(product_code, product_level)
    output_meta["DATE-OBS"] = input_pdata.meta["DATE-OBS"].value
    output_wcs = input_pdata.wcs

    # Synchronize overlapping metadata keys
    output_header = output_meta.to_fits_header(output_wcs)
    for key in output_header:
        if (key in input_pdata.meta) and output_header[key] == "" and key not in  ("COMMENT", "HISTORY"):
            output_meta[key].value = input_pdata.meta[key].value

    output_data = remix_polarization(input_pdata)
    output_data = add_fcorona(output_data)

    # Package into a PUNCHdata object
    output_pdata = NDCube(data=output_data.data.astype(np.float32), wcs=output_wcs, meta=output_meta)
    output_pdata = update_spacecraft_location(output_pdata, input_pdata.meta.astropy_time)

    # Write out
    write_ndcube_to_fits(output_pdata, path_output + get_base_file_name(output_pdata) + ".fits")


@task
def generate_l2_ctm(input_file: str, path_output: str) -> None:
    """Generate level 2 CTM synthetic data."""
    # Read in the input data
    input_pdata = load_ndcube_from_fits(input_file)

    # Define the output data product
    product_code = "CTM"
    product_level = "2"
    output_meta = NormalizedMetadata.load_template(product_code, product_level)
    output_meta["DATE-OBS"] = input_pdata.meta["DATE-OBS"].value
    output_wcs = input_pdata.wcs

    # Synchronize overlapping metadata keys
    output_header = output_meta.to_fits_header(output_wcs)
    for key in output_header:
        if (key in input_pdata.meta) and output_header[key] == "" and key not in ("COMMENT", "HISTORY"):
            output_meta[key].value = input_pdata.meta[key].value

    output_data = add_fcorona(input_pdata)

    # Package into a PUNCHdata object
    output_pdata = NDCube(data=output_data.data.astype(np.float32), wcs=output_wcs, meta=output_meta)
    output_pdata = update_spacecraft_location(output_pdata, input_pdata.meta.astropy_time)

    # Write out
    write_ndcube_to_fits(output_pdata, path_output + get_base_file_name(output_pdata) + ".fits")


@flow(log_prints=True, task_runner=DaskTaskRunner(
    cluster_kwargs={"n_workers": 8, "threads_per_worker": 2},
))
def generate_l2_all(datadir: str) -> None:
    """Generate all level 2 synthetic data.

    L2_PTM <- f-corona subtraction <- starfield subtraction <- remix polarization <- L3_PTM
    """
    # Set file output path
    print(f"Running from {datadir}")
    outdir = os.path.join(datadir, "synthetic_l2/")
    os.makedirs(outdir, exist_ok=True)
    print(f"Outputting to {outdir}")

    # Parse list of level 3 model data
    files_ptm = glob.glob(datadir + "/synthetic_l3/*PTM*.fits")
    files_ctm = glob.glob(datadir + "/synthetic_l3/*CTM*.fits")
    print(f"Generating based on {len(files_ptm)} PTM files.")
    print(f"Generating based on {len(files_ctm)} CTM files.")
    files_ptm.sort()

    futures = []
    # Run individual generators
    for file_ptm in tqdm(files_ptm):
        futures.append(generate_l2_ptm.submit(file_ptm, outdir))  # noqa: PERF401

    for file_ctm in tqdm(files_ctm):
        futures.append(generate_l2_ctm.submit(file_ctm, outdir))  # noqa: PERF401

    wait(futures)
