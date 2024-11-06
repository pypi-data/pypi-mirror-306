import os
import tempfile
import SimpleITK as sitk
import nibabel as nib
import numpy as np
from pydicom import dcmread


def sort_by_image_position_patient(file_names_or_datasets):
    """
    Sorts DICOM image files or datasets based on their position along the imaging axis.

    This function sorts a list of DICOM file paths or datasets based on the ImagePositionPatient
    tag and the orientation of the image (using ImageOrientationPatient).

    Parameters
    ----------
    file_names_or_datasets : list of str or list of pydicom.Dataset
        The list of DICOM file paths or datasets to sort.

    Returns
    -------
    list of str or list of pydicom.Dataset
        The sorted list of DICOM file paths or datasets.

    Notes
    -----
    This function computes the imaging axis using the ImageOrientationPatient tag
    and sorts the files based on the ImagePositionPatient tag along that axis.

    Examples
    --------
    >>> sorted_files = sort_by_image_position_patient(dicom_file_list)
    >>> print(sorted_files)
    ['file1.dcm', 'file2.dcm', 'file3.dcm']
    """

    def get_image_position_along_imaging_axis(ds):
        try:
            if isinstance(ds, str):
                ds = dcmread(ds, stop_before_pixels=True)

            image_position_patient = np.array(ds.ImagePositionPatient, dtype=float)
            image_orientation_patient = np.array(ds.ImageOrientationPatient, dtype=float)
            row_cosines = image_orientation_patient[:3]
            col_cosines = image_orientation_patient[3:]
            imaging_axis = np.cross(row_cosines, col_cosines)
            return np.dot(image_position_patient, imaging_axis)
        except Exception as e:
            print(f"Could not read dataset: {e}")
            return float("inf")

    sorted_items = sorted(file_names_or_datasets, key=get_image_position_along_imaging_axis)
    return sorted_items


def validate_dicom_path(path):
    """
    Validates whether the provided path is a valid file or directory.

    This function checks if the given path exists on the filesystem. It raises an error
    if the path does not exist or if it is neither a file nor a directory.

    Parameters
    ----------
    path : str
        The file system path to be validated.

    Raises
    ------
    IOError
        If the provided path does not exist.
    IOError
        If the provided path is neither a file nor a directory.
    """
    if not os.path.exists(path):
        raise IOError(f"Provided path does not exist: {path}")
    if not (os.path.isfile(path) or os.path.isdir(path)):
        raise IOError(f"Provided path is neither a file nor a directory: {path}")


def sitk_to_nifti(sitk_image):
    """
    Convert a SimpleITK Image to a nibabel NIfTI image by writing to a temporary file.

    Parameters:
    sitk_image (SimpleITK.Image): The SimpleITK Image object.

    Returns:
    nibabel.Nifti1Image: The converted NIfTI image object.
    """
    # Create a temporary file to hold the NIfTI image
    with tempfile.NamedTemporaryFile(suffix=".nii", delete=False) as temp_nifti_file:
        temp_nifti_file_path = temp_nifti_file.name

    try:
        # Write the SimpleITK image to the temporary NIfTI file
        sitk.WriteImage(sitk_image, temp_nifti_file_path)

        # Read the temporary NIfTI file using nibabel
        nifti_image = nib.load(temp_nifti_file_path)

        data = nifti_image.get_fdata()
        nifti_image_loaded = nib.Nifti1Image(data, nifti_image.affine, nifti_image.header)
        nifti_image_loaded.extra = {}

    finally:
        # Remove the temporary file after it has been read
        os.remove(temp_nifti_file_path)

    return nifti_image_loaded


def nifti_to_sitk(nifti_image):
    """
    Convert a nibabel NIfTI image to a SimpleITK Image by writing to a temporary file.

    Parameters:
    nifti_image (nibabel.Nifti1Image): The NIfTI image object.

    Returns:
    SimpleITK.Image: The converted SimpleITK Image object.
    """
    data = nifti_image.get_fdata()
    nifti_image_loaded = nib.Nifti1Image(data, nifti_image.affine, nifti_image.header)
    nifti_image_loaded.extra = {}

    # Create a temporary file to hold the NIfTI image
    with tempfile.NamedTemporaryFile(suffix=".nii", delete=False) as temp_nifti_file:
        temp_nifti_file_path = temp_nifti_file.name

    try:
        # Write the NIfTI image to the temporary file using nibabel
        nib.save(nifti_image, temp_nifti_file_path)

        # Read the temporary NIfTI file using SimpleITK
        sitk_image = sitk.ReadImage(temp_nifti_file_path)
    finally:
        if os.path.exists(temp_nifti_file_path):
            # Remove the temporary file
            os.remove(temp_nifti_file_path)

    return sitk_image
