import os
import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tqdm import tqdm
from pydicom import dcmread
from io import BytesIO
from rosamllib.readers import (
    DICOMImageReader,
    RTStructReader,
    RTDoseReader,
    REGReader,
    DICOMRawReader,
    RTPlanReader,
    RTRecordReader,
)
from rosamllib.readers.dicom_nodes import (
    DatasetNode,
    PatientNode,
    StudyNode,
    SeriesNode,
    InstanceNode,
)
from rosamllib.utils import validate_dicom_path
from concurrent.futures import ThreadPoolExecutor


class DICOMLoader:
    """
    A class for loading, organizing, and managing DICOM files in a hierarchical structure.

    The `DICOMLoader` class provides methods to load DICOM files from a specified path, organize
    them into a hierarchical structure of patients, studies, series, and instances, and retrieve
    information at each level. Additionally, it offers functionalities to summarize, visualize, and
    read DICOM data based on specific modalities. It is designed to handle large datasets and
    supports the extraction of metadata as well as the reading and visualization of DICOM series.

    Parameters
    ----------
    path : str
        The directory or file path where DICOM files are located.

    Attributes
    ----------
    path : str
        The directory or file path provided during initialization, used to locate DICOM files.
    dicom_files : dict
        A dictionary that stores DICOM files grouped by PatientID and SeriesInstanceUID.
    dataset : DatasetNode
        The top-level node containing all patients, organized into a dataset structure.

    Methods
    -------
    load()
        Loads DICOM files from the specified path and organizes them into a structured dataset.
    load_from_directory(path)
        Recursively loads all DICOM files in the given directory.
    get_summary()
        Provides a summary count of patients, studies, series, and instances.
    get_patient_summary(patient_id)
        Retrieves a detailed summary of all studies and series for a given patient.
    get_study_summary(study_uid)
        Retrieves a summary of series and instances within a specified study.
    get_series_summary(series_uid)
        Retrieves detailed information about a series, including instance paths.
    get_modality_distribution()
        Returns the distribution of modalities present in the dataset.
    get_patient_ids()
        Returns a list of all PatientIDs within the dataset.
    get_study_uids(patient_id)
        Returns a list of StudyInstanceUIDs for a specified patient.
    get_series_uids(study_uid)
        Returns a list of SeriesInstanceUIDs for a specified study.
    get_series_paths(patient_id, series_uid)
        Retrieves file paths for all instances within a specific series.
    get_patient(patient_id)
        Retrieves a PatientNode by its PatientID.
    get_study(study_uid)
        Retrieves a StudyNode by its StudyInstanceUID.
    get_series(series_uid)
        Retrieves a SeriesNode by its SeriesInstanceUID.
    get_instance(sop_instance_uid)
        Retrieves an InstanceNode by its SOPInstanceUID.
    read_series(series_uid)
        Reads and returns data for a series based on its SeriesInstanceUID.
    read_instance(sop_instance_uid)
        Reads and returns data for a specific instance based on its SOPInstanceUID.
    visualize_series_references(patient_id, output_file, view, per_patient, exclude_modalities,
                                exclude_series, include_uid, rankdir)
        Visualizes the series-level associations for all or specific patients using Graphviz.

    Examples
    --------
    >>> loader = DICOMLoader("/path/to/dicom/files")
    >>> loader.load()
    >>> summary = loader.get_summary()
    >>> print(summary)
    {'total_patients': 10, 'total_studies': 50, 'total_series': 200, 'total_instances': 5000}

    >>> patient_summary = loader.get_patient_summary("12345")
    >>> print(patient_summary)
    {'patient_id': '12345', 'patient_name': 'John Doe', 'studies': [{'study_uid': '1.2.3', ...}]}

    >>> series_paths = loader.get_series_paths("12345", "1.2.3.4.5")
    >>> print(series_paths)
    ['/path/to/file1.dcm', '/path/to/file2.dcm']
    """

    def __init__(self, path):
        """
        Initializes the DICOMLoader with the specified path.

        Parameters
        ----------
        path : str
            The directory or file path where DICOM files are located.
        """
        self.path = path
        self.dicom_files = {}
        self.dataset = None

    def load(self):
        """
        Loads the DICOM files from the specified path.

        This method validates the provided path, reads the DICOM files, and organizes them
        by patient and series. The method also associates referenced DICOMs using SOPInstanceUID
        and SeriesInstanceUID.

        Raises
        ------
        Exception
            If there is an error loading or processing the DICOM files.

        Examples
        --------
        >>> loader = DICOMLoader("/path/to/dicom/files")
        >>> loader.load()
        """
        validate_dicom_path(self.path)
        try:
            if os.path.isdir(self.path):
                self.dicom_files = DICOMLoader.load_from_directory(self.path)

            else:
                self.dicom_files = DICOMLoader.load_file(self.path)
            self._build_hierarchical_structure()

        except Exception as e:
            print(f"Error loading DICOM files: {e}")

    @staticmethod
    def load_from_directory(path):
        """
        Loads all DICOM files from a directory, including subdirectories.

        This method recursively searches the specified directory for DICOM files,
        reads their metadata, and organizes them by patient and series.

        Parameters
        ----------
        path : str
            The directory path to load DICOM files from.

        Returns
        -------
        dict
            A dictionary where the keys are PatientIDs and the values are dictionaries
            of Series objects indexed by SeriesInstanceUID.

        Raises
        ------
        Exception
            If there is an error reading DICOM files.

        Examples
        --------
        >>> dicom_files = DICOMLoader.load_from_directory("/path/to/dicom/files")
        """
        validate_dicom_path(path)
        all_files = []
        for root, dirs, files in tqdm(os.walk(path), desc="Scanning directories"):
            for file in files:
                all_files.append(os.path.join(root, file))
        print(f"Found {len(all_files)} files.")
        return DICOMLoader._load_files(all_files)

    @staticmethod
    def load_file(path):
        """
        Loads a single DICOM file and returns the Series object it belongs to.

        Parameters
        ----------
        path : str
            The file path to the DICOM file.

        Returns
        -------
        dict
            A dictionary containing the DICOM data organized by PatientID and SeriesInstanceUID.

        Raises
        ------
        Exception
            If there is an error reading the DICOM file.

        Examples
        --------
        >>> dicom_file = DICOMLoader.load_file("/path/to/file.dcm")
        """
        validate_dicom_path(path)
        return DICOMLoader._load_files([path])

    @staticmethod
    def _load_files(files):
        """
        Loads and processes a list of DICOM file paths with parallel processing.

        Parameters
        ----------
        files : list of str
            A list of DICOM file paths.

        Returns
        -------
        dict
            A dictionary where the keys are PatientIDs and the values are dictionaries
            of Series objects indexed by SeriesInstanceUID.

        Raises
        ------
        Exception
            If there is an error reading or processing a DICOM file.
        """
        dicom_files = {}

        def process_file(filepath):
            try:
                ds = dcmread(filepath, stop_before_pixels=True)
                modality = getattr(ds, "Modality", None)

                if modality in ["CT", "MR", "PT", "RTSTRUCT", "RTPLAN", "RTDOSE", "RTRECORD"]:
                    DICOMLoader._process_standard_dicom(ds, filepath, dicom_files)
                elif modality == "REG":
                    DICOMLoader._process_reg_file(filepath, dicom_files)
                elif modality == "RAW":
                    DICOMLoader._process_raw_files(filepath, dicom_files)
            except Exception:
                pass  # Log exception if needed

        # Use ThreadPoolExecutor to process files in parallel
        with ThreadPoolExecutor() as executor:
            list(
                tqdm(executor.map(process_file, files), desc="Processing DICOM files", unit="file")
            )

        DICOMLoader._associate_dicoms(dicom_files)
        return dicom_files

    @staticmethod
    def _process_standard_dicom(ds, filepath, dicom_files):
        """
        Processes standard DICOM files (e.g., CT, MR, RTPLAN, etc.).

        This method reads and processes standard DICOM files, extracting metadata such as
        PatientID, SeriesInstanceUID, Modality, and SeriesDescription, and stores them in
        a Series object.

        Parameters
        ----------
        ds : pydicom.Dataset
            The DICOM dataset object representing the file.
        filepath : str
            The file path of the DICOM file.
        dicom_files : dict
            A dictionary where the processed DICOM data is stored, indexed by PatientID and
            SeriesInstanceUID.

        Examples
        --------
        >>> DICOMLoader._process_standard_dicom(ds, "/path/to/file.dcm", dicom_files)
        """
        patient_id = getattr(ds, "PatientID", None)
        series_uid = getattr(ds, "SeriesInstanceUID", None)
        modality = getattr(ds, "Modality", None)
        sop_instance_uid = getattr(ds, "SOPInstanceUID", None)

        if patient_id not in dicom_files:
            dicom_files[patient_id] = {}

        if series_uid not in dicom_files[patient_id]:
            series = SeriesNode(series_uid)
            dicom_files[patient_id][series_uid] = series
        series = dicom_files[patient_id][series_uid]
        series.PatientID = patient_id
        series.Modality = modality
        series.PatientName = getattr(ds, "PatientName", None)
        series.StudyInstanceUID = getattr(ds, "StudyInstanceUID", None)
        series.StudyDescription = getattr(ds, "StudyDescription", "")
        series.SeriesDescription = getattr(ds, "SeriesDescription", "")
        series.FrameOfReferenceUID = getattr(ds, "FrameOfReferenceUID", None)
        series.SOPInstances.append(sop_instance_uid)
        series.instance_paths.append(filepath)

        # Create InstanceNode
        instance_node = InstanceNode(
            sop_instance_uid, filepath, modality=modality, parent_series=series
        )
        if modality in ["RTSTRUCT", "RTPLAN", "RTDOSE", "RTRECORD"]:
            # handle RT files
            instance_node.referenced_sop_instance_uids = (
                DICOMLoader._get_referenced_sop_instance_uids(ds)
            )

        series.add_instance(instance_node)

    @staticmethod
    def _get_referenced_sop_instance_uids(ds):
        """
        Extracts referenced SOPInstanceUIDs from RTSTRUCT, RTPLAN, and RTDOSE DICOM files.

        This method scans the DICOM dataset for references to other DICOM instances and returns
        the list of referenced SOPInstanceUIDs.

        Parameters
        ----------
        ds : pydicom.Dataset
            The DICOM dataset to extract references from.

        Returns
        -------
        list of str
            A list of referenced SOPInstanceUIDs from the DICOM dataset.

        Examples
        --------
        >>> uids = DICOMLoader._get_referenced_sop_instance_uids(ds)
        >>> print(uids)
        ['1.2.3.4.5.6.7', '1.2.3.4.5.6.8']
        """
        referenced_uids = set()
        if ds.Modality == "RTSTRUCT":
            if hasattr(ds, "ReferencedFrameOfReferenceSequence"):
                for item in ds.ReferencedFrameOfReferenceSequence:
                    if hasattr(item, "RTReferencedStudySequence"):
                        for study_item in item.RTReferencedStudySequence:
                            if hasattr(study_item, "RTReferencedSeriesSequence"):
                                for series_item in study_item.RTReferencedSeriesSequence:
                                    if hasattr(series_item, "ContourImageSequence"):
                                        for contour_item in series_item.ContourImageSequence:
                                            referenced_uids.add(
                                                contour_item.ReferencedSOPInstanceUID
                                            )
            if hasattr(ds, "ROIContourSequence"):
                for roi_item in ds.ROIContourSequence:
                    if hasattr(roi_item, "ContourSequence"):
                        for contour_seq in roi_item.ContourSequence:
                            if hasattr(contour_seq, "ContourImageSequence"):
                                for image_seq in contour_seq.ContourImageSequence:
                                    referenced_uids.add(image_seq.ReferencedSOPInstanceUID)

        else:
            if hasattr(ds, "ReferencedStructureSetSequence"):
                for item in ds.ReferencedStructureSetSequence:
                    if hasattr(item, "ReferencedSOPInstanceUID"):
                        referenced_uids.add(item.ReferencedSOPInstanceUID)

            if hasattr(ds, "ReferencedDoseSequence"):
                for item in ds.ReferencedDoseSequence:
                    if hasattr(item, "ReferencedSOPInstanceUID"):
                        referenced_uids.add(item.ReferencedSOPInstanceUID)

            if hasattr(ds, "ReferencedRTPlanSequence"):
                for item in ds.ReferencedRTPlanSequence:
                    if hasattr(item, "ReferencedSOPInstanceUID"):
                        referenced_uids.add(item.ReferencedSOPInstanceUID)

        return list(referenced_uids)

    @staticmethod
    def _process_reg_file(filepath, dicom_files):
        """
        Processes DICOM registration (REG) files and stores the relevant metadata.

        This method processes DICOM registration files and extracts relevant information
        including PatientID, SeriesInstanceUID, and other metadata. It also associates
        referenced series and images with the registration.

        Parameters
        ----------
        filepath : str
            The file path to the REG file.
        dicom_files : dict
            A dictionary where the processed REG data is stored, indexed by PatientID and
            SeriesInstanceUID.

        Examples
        --------
        >>> DICOMLoader._process_reg_file("/path/to/regfile.dcm", dicom_files)
        """
        reg = REGReader(filepath).read()

        patient_id = getattr(reg, "PatientID", None)
        series_uid = getattr(reg, "SeriesInstanceUID", None)
        modality = getattr(reg, "Modality", None)
        sop_instance_uid = getattr(reg, "SOPInstanceUID", None)
        series = None

        if patient_id not in dicom_files:
            dicom_files[patient_id] = {}

        if series_uid not in dicom_files[patient_id]:
            series = SeriesNode(series_uid)
            dicom_files[patient_id][series_uid] = series
        series = dicom_files[patient_id][series_uid]
        series.PatientID = patient_id
        series.Modality = modality
        series.PatientName = getattr(reg, "PatientName", None)
        series.StudyInstanceUID = getattr(reg, "StudyInstanceUID", None)
        series.StudyDescription = getattr(reg, "StudyDescription", "")
        series.SeriesDescription = getattr(reg, "SeriesDescription", "")
        series.FrameOfReferenceUID = getattr(reg, "FrameOfReferenceUID", None)

        # Create InstanceNode
        instance_node = InstanceNode(sop_instance_uid, filepath, modality, parent_series=series)
        instance_node.referenced_sids.append(reg.get_fixed_image_info()["SeriesInstanceUID"])
        instance_node.other_referenced_sids.append(
            reg.get_moving_image_info()["SeriesInstanceUID"]
        )

        series.SOPInstances.append(sop_instance_uid)
        series.instance_paths.append(filepath)
        series.add_instance(instance_node)

    @staticmethod
    def _process_raw_files(filepath, dicom_files):
        """
        Processes DICOM RAW files and stores the relevant metadata.

        This method processes DICOM RAW files, extracting metadata such as PatientID and
        SeriesInstanceUID, and associates referenced series and images.

        Parameters
        ----------
        filepath : str
            The file path to the RAW file.
        dicom_files : dict
            A dictionary where the processed RAW data is stored, indexed by PatientID and
            SeriesInstanceUID.

        Examples
        --------
        >>> DICOMLoader._process_raw_files("/path/to/rawfile.dcm", dicom_files)
        """
        raw_reader = DICOMRawReader(filepath)
        raw_reader.read()
        ds = raw_reader.dataset

        patient_id = getattr(ds, "PatientID", None)
        series_uid = getattr(ds, "SeriesInstanceUID", None)
        modality = getattr(ds, "Modality", None)
        sop_instance_uid = getattr(ds, "SOPInstanceUID", None)

        if patient_id not in dicom_files:
            dicom_files[patient_id] = {}

        if series_uid not in dicom_files[patient_id]:
            series = SeriesNode(series_uid)
            dicom_files[patient_id][series_uid] = series
        series = dicom_files[patient_id][series_uid]
        series.PatientID = patient_id
        series.Modality = modality
        series.PatientName = getattr(ds, "PatientName", None)
        series.StudyInstanceUID = getattr(ds, "StudyInstanceUID", None)
        series.StudyDescription = getattr(ds, "StudyDescription", "")
        series.SeriesDescription = getattr(ds, "SeriesDescription", "")
        series.FrameOfReferenceUID = getattr(ds, "FrameOfReferenceUID", None)

        series.SOPInstances.append(sop_instance_uid)
        series.instance_paths.append(filepath)

        # Create InstanceNode for the RAW file
        instance_node = InstanceNode(sop_instance_uid, filepath, modality, parent_series=series)
        instance_node.referenced_sids(raw_reader.referenced_series_uid)
        series.add_instance(instance_node)

        # now process the embedded datasets (if any)
        try:
            embedded_datasets = raw_reader.get_embedded_datasets()

            # create Series objects for each embedded dataset
            for embedded_ds in embedded_datasets:
                embedded_series_uid = getattr(embedded_ds, "SeriesInstanceUID", None)
                embedded_sop_instance_uid = getattr(embedded_ds, "SOPInstanceUID", None)
                embedded_modality = getattr(embedded_ds, "Modality", None)

                if embedded_series_uid:
                    # create or retrieve the series for the embedded dataset
                    if embedded_series_uid not in dicom_files[patient_id]:
                        embedded_series = SeriesNode(embedded_series_uid)
                        dicom_files[patient_id][embedded_series_uid] = embedded_series

                    embedded_series = dicom_files[patient_id][embedded_series_uid]
                    # set the embedded series metadata
                    embedded_series.PatientID = patient_id
                    embedded_series.PatientName = series.PatientName
                    embedded_series.Modality = embedded_modality
                    embedded_series.StudyInstanceUID = getattr(
                        embedded_ds, "StudyInstanceUID", None
                    )
                    embedded_series.StudyDescription = getattr(embedded_ds, "StudyDescription", "")
                    embedded_series.SeriesDescription = getattr(
                        embedded_ds, "SeriesDescription", ""
                    )
                    embedded_series.FrameOfReferenceUID = getattr(
                        embedded_ds, "FrameOfReferenceUID", None
                    )
                    embedded_series.SOPInstances.append(
                        getattr(embedded_ds, "SOPInstanceUID", None)
                    )

                    # indicate that the embedded series is inside a RAW file
                    embedded_series.is_embedded_in_raw = True
                    embedded_series.raw_series_reference = series

                    # Create InstanceNode for the embedded instance
                    embedded_instance_node = InstanceNode(
                        embedded_sop_instance_uid,
                        filepath,
                        modality=embedded_modality,
                        parent_series=embedded_series,
                    )

                    # add references based on modality
                    if embedded_modality in ["RTSTRUCT", "RTPLAN", "RTDOSE", "RTRECORD"]:
                        # handle RT files
                        embedded_instance_node.referenced_sop_instance_uids = (
                            DICOMLoader._get_referenced_sop_instance_uids(embedded_ds)
                        )

                    elif embedded_modality == "REG":
                        embedded_reg = REGReader(embedded_ds).read()
                        embedded_instance_node.referenced_sids.append(
                            embedded_reg.get_fixed_image_info()["SeriesInstanceUID"]
                        )
                        embedded_instance_node.other_referenced_sids.append(
                            embedded_reg.get_moving_image_info()["SeriesInstanceUID"]
                        )

                    embedded_series.add_instance(embedded_instance_node)

        except Exception:
            pass

    @staticmethod
    def _associate_dicoms(dicom_files):
        """
        Associates DICOM files based on referenced SOPInstanceUIDs and SeriesInstanceUIDs.

        This method builds lookup tables for SOPInstanceUIDs and SeriesInstanceUIDs and
        associates referenced DICOM instances and series by establishing connections between
        related DICOMs.

        Parameters
        ----------
        dicom_files : dict
            A dictionary where the processed DICOM data is stored, indexed by PatientID and
            SeriesInstanceUID.

        Examples
        --------
        >>> DICOMLoader._associate_dicoms(dicom_files)
        """
        # Create a lookup table for all SOPInstanceUIDs and SeriesInstanceUIDs across all patients
        sop_instance_uid_map = {}
        series_uid_map = {}
        frame_of_reference_uid_map = {}

        # Build the lookup maps
        for patient_id, series_dict in dicom_files.items():
            for series_uid, series in series_dict.items():
                series_uid_map[series_uid] = series
                for sop_instance_uid, instance_node in series.instances.items():
                    sop_instance_uid_map[sop_instance_uid] = instance_node

                # Map each FrameOfReferenceUID to a list of series sharing the same
                # FrameOfReferenceUID
                if series.FrameOfReferenceUID:
                    if series.FrameOfReferenceUID not in frame_of_reference_uid_map:
                        frame_of_reference_uid_map[series.FrameOfReferenceUID] = []
                    frame_of_reference_uid_map[series.FrameOfReferenceUID].append(series)

        # Now, associate instances based on their references
        for patient_id, series_dict in dicom_files.items():
            for series_uid, series in series_dict.items():
                for sop_uid, instance in series.instances.items():
                    modality = instance.Modality

                    # Initialize referenced_instances list
                    instance.referenced_instances = []

                    # General handling for referenced SOPInstanceUIDs
                    for ref_sop_uid in instance.referenced_sop_instance_uids:
                        ref_instance = sop_instance_uid_map.get(ref_sop_uid)
                        if ref_instance:
                            instance.referenced_instances.append(ref_instance)
                            ref_instance.referencing_instances.append(instance)
                        else:
                            # Reference to an instance not in dataset
                            pass

                    # Modality-specific associations
                    if modality in ["RTSTRUCT", "RTPLAN", "RTDOSE", "RTRECORD"]:
                        # RTSTRUCT references images via referenced_sop_instance_uids
                        referenced_series_uids = set()

                        for ref_instance in instance.referenced_instances:
                            ref_series_uid = ref_instance.parent_series.SeriesInstanceUID
                            referenced_series_uids.add(ref_series_uid)

                        for ref_sid in referenced_series_uids:
                            instance.referenced_sids.append(ref_sid)
                            ref_series = series_uid_map.get(ref_sid)
                            if ref_series:
                                instance.referenced_series.append(ref_series)

                    elif modality == "REG":
                        # REG references fixed image (referenced_sids) and
                        # moving image (other_referenced_sids)
                        ref_sids = instance.referenced_sids
                        other_ref_sids = instance.other_referenced_sids

                        if ref_sids:
                            for ref_sid in ref_sids:
                                ref_series = series_uid_map.get(ref_sid)
                                if ref_series:
                                    instance.referenced_series.append(ref_series)
                                else:
                                    pass

                        if other_ref_sids:
                            for other_ref_sid in other_ref_sids:
                                other_ref_series = series_uid_map.get(other_ref_sid)
                                if other_ref_series:
                                    instance.other_referenced_series.append(other_ref_series)
                                else:
                                    pass

                # Associate by FrameOfReferenceUID
                if series.FrameOfReferenceUID:
                    # Get all series sharing the same FrameOfReferenceUID
                    frame_of_reference_series = frame_of_reference_uid_map.get(
                        series.FrameOfReferenceUID, []
                    )
                    series.frame_of_reference_registered = [
                        s
                        for s in frame_of_reference_series
                        if s.SeriesInstanceUID != series.SeriesInstanceUID
                    ]

    def _build_hierarchical_structure(self):
        """
        Builds a hierarchical structure of DatasetNode, PatientNode, StudyNode, SeriesNode,
        and InstanceNode from the existing self.dicom_files.

        This method populates self.dataset with a DatasetNode instance containing PatientNode
        instances, and subsequently, the entire hierarchical structure.

        Returns
        -------
        None
        """
        # Initialize the DatasetNode as the root of the hierarchy
        dataset_id = "DICOM_Dataset"
        dataset_name = "DICOM Collection"
        self.dataset = DatasetNode(dataset_id, dataset_name)

        for patient_id, series_dict in self.dicom_files.items():
            # Create or get the PatientNode and add it to the DatasetNode
            if not self.dataset.get_patient(patient_id):
                any_series = next(iter(series_dict.values()))
                patient_name = any_series.PatientName
                patient_node = PatientNode(patient_id, patient_name, parent_dataset=self.dataset)
                self.dataset.add_patient(patient_node)

            if patient_id not in self.dataset.patients:
                # Assuming that PatientName is stored in one of the SeriesNodes
                any_series = next(iter(series_dict.values()))
                patient_name = any_series.PatientName
                patient_node = PatientNode(patient_id, patient_name, parent_dataset=self.dataset)
                self.dataset.add_patient(patient_node)
            else:
                patient_node = self.dataset.get_patient(patient_id)

            for series_uid, series_node in series_dict.items():
                # Retrieve StudyInstanceUID and StudyDescription from SeriesNode
                study_uid = series_node.StudyInstanceUID
                study_description = series_node.StudyDescription

                # Create or get the StudyNode and add it to the PatientNode
                if not patient_node.get_study(study_uid):
                    study_node = StudyNode(
                        study_uid, study_description, parent_patient=patient_node
                    )
                    patient_node.add_study(study_node)
                else:
                    study_node = patient_node.get_study(study_uid)

                # Add the SeriesNode to the StudyNode
                study_node.add_series(series_node)

                # Update SeriesNode attributes if necessary
                series_node.PatientID = patient_id
                series_node.PatientName = patient_node.PatientName
                series_node.StudyInstanceUID = study_uid
                series_node.StudyDescription = study_description

                # Link SeriesNode to the parent study node
                series_node.parent_study = study_node

    def get_summary(self):
        """
        Returns a summary of the entire DICOM dataset.

        Returns
        -------
        dict
            A dictionary containing the total counts of patients, studies, series, and instances.
        """
        if not self.dataset:
            return {
                "total_patients": 0,
                "total_studies": 0,
                "total_series": 0,
                "total_instances": 0,
            }

        num_patients = len(self.dataset)
        num_studies = 0
        num_series = 0
        num_instances = 0

        for patient_node in self.dataset:
            num_studies += len(patient_node.studies)
            for study_node in patient_node.studies.values():
                num_series += len(study_node.series)
                for series_node in study_node.series.values():
                    num_instances += len(series_node)

        summary = {
            "total_patients": num_patients,
            "total_studies": num_studies,
            "total_series": num_series,
            "total_instances": num_instances,
        }

        return summary

    def get_patient_summary(self, patient_id):
        """
        Returns a summary of all studies and series for the specified patient.

        Parameters
        ----------
        patient_id : str
            The PatientID of the patient to summarize.

        Returns
        -------
        dict or None
            A dictionary containing the patient's studies and series information,
            or None if the patient_id is not found.
        """
        if not self.dataset or patient_id not in self.dataset.patients:
            return None

        patient_node = self.dataset.get_patient(patient_id)
        patient_summary = {
            "patient_id": patient_node.PatientID,
            "patient_name": patient_node.PatientName,
            "studies": [],
        }

        for study_node in patient_node:
            # Use get_study_summary to get detailed study information
            study_summary = self.get_study_summary(study_node.StudyInstanceUID)
            if study_summary:
                patient_summary["studies"].append(study_summary)

        return patient_summary

    def get_study_summary(self, study_uid):
        """
        Returns a summary of all series and instances within the specified study.

        Parameters
        ----------
        study_uid : str
            The StudyInstanceUID of the study to summarize.

        Returns
        -------
        dict or None
            A dictionary containing the study's series and instances information,
            or None if the study_uid is not found.
        """
        for patient_node in self.dataset:
            if study_uid in patient_node.studies:
                study_node = patient_node.get_study(study_uid)
                study_summary = {
                    "patient_id": patient_node.PatientID,
                    "patient_name": patient_node.PatientName,
                    "study_uid": study_node.StudyInstanceUID,
                    "study_description": study_node.StudyDescription,
                    "series": [],
                }

                for series_node in study_node:
                    # Use get_series_summary to get detailed series information
                    series_summary = self.get_series_summary(series_node.SeriesInstanceUID)
                    if series_summary:
                        study_summary["series"].append(series_summary)

                return study_summary

        return None

    def get_series_summary(self, series_uid):
        """
        Returns detailed information about the specified series, including its instances.

        Parameters
        ----------
        series_uid : str
            The SeriesInstanceUID of the series to summarize.

        Returns
        -------
        dict or None
            A dictionary containing the series information and its instances,
            or None if the series_uid is not found.
        """
        for patient_node in self.dataset:
            for study_node in patient_node:
                if series_uid in study_node.series:
                    series_node = study_node.get_series(series_uid)
                    series_summary = {
                        "patient_id": patient_node.PatientID,
                        "patient_name": patient_node.PatientName,
                        "study_uid": study_node.StudyInstanceUID,
                        "study_description": study_node.StudyDescription,
                        "series_uid": series_node.SeriesInstanceUID,
                        "series_description": series_node.SeriesDescription,
                        "modality": series_node.Modality,
                        "num_instances": len(series_node),
                        "instances": [],
                    }

                    for instance_node in series_node:
                        instance_info = {
                            "sop_instance_uid": instance_node.SOPInstanceUID,
                            "modality": instance_node.Modality,
                            "filepath": instance_node.filepath,
                        }
                        series_summary["instances"].append(instance_info)

                    return series_summary

        return None

    def get_modality_distribution(self):
        """
        Returns the distribution of modalities in the dataset.

        Returns
        -------
        dict
            A dictionary where keys are modalities and values are counts of series.
        """
        modality_counts = {}

        for patient_node in self.dataset:
            for study_node in patient_node:
                for series_node in study_node:
                    modality = series_node.Modality or "Unknown"
                    modality_counts[modality] = modality_counts.get(modality, 0) + 1

        return modality_counts

    def get_patient_ids(self):
        """
        Returns a list of all PatientIDs in the dataset.

        Returns
        -------
        list of str
            A list of PatientIDs.
        """
        return list(self.dataset.patients.keys())

    def get_study_uids(self, patient_id):
        """
        Returns a list of StudyInstanceUIDs for the specified patient.

        Parameters
        ----------
        patient_id : str
            The PatientID of the patient.

        Returns
        -------
        list of str
            A list of StudyInstanceUIDs, or an empty list if the patient is not found.
        """
        patient_node = self.dataset.get_patient(patient_id)
        if patient_node is None:
            return []
        return list(patient_node.studies.keys())

    def get_series_uids(self, study_uid):
        """
        Returns a list of SeriesInstanceUIDs for the specified study.

        Parameters
        ----------
        study_uid : str
            The StudyInstanceUID of the study.

        Returns
        -------
        list of str
            A list of SeriesInstanceUIDs, or an empty list if the study is not found.
        """
        for patient_node in self.dataset:
            study_node = patient_node.get_study(study_uid)
            if study_node:
                return list(study_node.series.keys())
        return []

    def get_series_paths(self, patient_id, series_uid):
        """
        Returns the file paths for all instances in a specific series.

        Parameters
        ----------
        patient_id : str
            The PatientID of the series to retrieve.
        series_uid : str
            The SeriesInstanceUID of the series to retrieve.

        Returns
        -------
        list of str
            A list of file paths for the specified series.

        Raises
        ------
        ValueError
            If the specified series is not found for the given patient.
        """
        patient_node = self.dataset.get_patient(patient_id)
        if patient_node is None:
            raise ValueError(f"Patient {patient_id} not found.")

        for study_node in patient_node:
            series_node = study_node.get_series(series_uid)
            if series_node:
                return series_node.instance_paths

        raise ValueError(f"Series {series_uid} for Patient {patient_id} not found.")

    def get_patient(self, patient_id):
        """
        Retrieves a PatientNode by its PatientID.

        Parameters
        ----------
        patient_id : str
            The PatientID of the patient to retrieve.

        Returns
        -------
        PatientNode or None
            The `PatientNode` associated with the given patient_id, or None if not found.
        """
        return self.dataset.get_patient(patient_id) if self.dataset else None

    def get_study(self, study_uid):
        """
        Retrieves a StudyNode by its StudyInstanceUID.

        Parameters
        ----------
        study_uid : str
            The StudyInstanceUID of the study to retrieve.

        Returns
        -------
        StudyNode or None
            The `StudyNode` associated with the given study_uid, or None if not found.
        """
        for patient_node in self.dataset:
            study_node = patient_node.get_study(study_uid)
            if study_node:
                return study_node
        return None

    def get_series(self, series_uid):
        """
        Retrieves a SeriesNode by its SeriesInstanceUID.

        Parameters
        ----------
        series_uid : str
            The SeriesInstanceUID of the series to retrieve.

        Returns
        -------
        SeriesNode or None
            The `SeriesNode` associated with the given series_uid, or None if not found.
        """
        for patient_node in self.dataset:
            for study_node in patient_node:
                series_node = study_node.get_series(series_uid)
                if series_node:
                    return series_node
        return None

    def get_instance(self, sop_instance_uid):
        """
        Retrieves an InstanceNode by its SOPInstanceUID.

        Parameters
        ----------
        sop_instance_uid : str
            The SOPInstanceUID of the instance to retrieve.

        Returns
        -------
        InstanceNode or None
            The `InstanceNode` associated with the given sop_instance_uid, or None if not found.
        """
        for patient_node in self.dataset:
            for study_node in patient_node:
                for series_node in study_node:
                    instance_node = series_node.get_instance(sop_instance_uid)
                    if instance_node:
                        return instance_node
        return None

    def read_series(self, series_uid):
        """
        Reads a DICOM series based on its SeriesInstanceUID and returns an appropriate
        representation of the series using modality-specific readers.

        This method first searches for the series with the given SeriesInstanceUID in the
        loaded DICOM data within the dataset graph. It then selects the appropriate reader
        based on the modality of the series and reads the data accordingly. If the series
        is embedded in a RAW file, it extracts the embedded datasets and reads them.

        Parameters
        ----------
        series_uid : str
            The unique SeriesInstanceUID of the series to be read.

        Returns
        -------
        list
            A list of objects representing the series. For DICOM-RT modalities
            (e.g., RTSTRUCT, RTDOSE), each instance is read separately, and the
            results are returned as a list of objects. For embedded series in RAW files,
            the embedded datasets are extracted and returned as a list. If the series has
            only one instance, a list containing one object is returned.

        Raises
        ------
        ValueError
            If no series with the given SeriesInstanceUID is found in the loaded DICOM files.
        NotImplementedError
            If a reader for this modality type is not implemented yet.

        Examples
        --------
        >>> loader = DICOMLoader("/path/to/dicom/files")
        >>> loader.load()
        >>> dicom_image = loader.read_series("1.2.840.113619.2.55.3")[0]
        >>> rtstruct = loader.read_series("1.2.840.113619.2.55.4")[0]
        """
        # TODO:
        # Use get_series method
        found_series = None
        for patient in self.dataset:
            for study in patient.studies.values():
                found_series = study.get_series(series_uid)
                if found_series:
                    break
            if found_series:
                break

        if found_series is None:
            raise ValueError(f"Series with SeriesInstanceUID '{series_uid}' not found.")

        # Determine the modality and handle accordingly
        modality = found_series.Modality

        if found_series.is_embedded_in_raw:
            raw_series_reference = found_series.raw_series_reference
            embedded_datasets = (
                DICOMRawReader(raw_series_reference.SOPInstances[0]).read().get_embedded_datasets()
            )
            embedded_series = [
                self._read_embedded(dataset)
                for dataset in embedded_datasets
                if dataset.SeriesInstanceUID == series_uid
            ]
            return embedded_series

        if modality in ["CT", "MR", "PT"]:
            return [DICOMImageReader(found_series.instance_paths).read()]

        elif modality == "RTSTRUCT":
            return [
                RTStructReader(instance_path).read()
                for instance_path in found_series.instance_paths
            ]

        elif modality == "RTDOSE":
            return [
                RTDoseReader(instance_path).read() for instance_path in found_series.instance_paths
            ]

        elif modality == "REG":
            return [
                REGReader(instance_path).read() for instance_path in found_series.instance_paths
            ]

        elif modality == "RTPLAN":
            return [
                RTPlanReader(instance_path).read() for instance_path in found_series.instance_paths
            ]

        elif modality == "RTRECORD":
            return [
                RTRecordReader(instance_path).read()
                for instance_path in found_series.instance_paths
            ]

        else:
            raise NotImplementedError(f"A reader for {modality} type is not implemented yet.")

    def read_instance(self, sop_instance_uid):
        """
        Reads a single DICOM instance based on its SOPInstanceUID and returns an appropriate
        representation of the instance using modality-specific readers.

        This method searches within the dataset graph to locate the instance with the given
        SOPInstanceUID. It then selects the appropriate reader based on the modality of the
        series to which the instance belongs and reads the data accordingly.

        Parameters
        ----------
        sop_instance_uid : str
            The unique SOPInstanceUID of the instance to be read.

        Returns
        -------
        object
            An object representing the instance. This object type depends on the modality of
            the instance (e.g., RTStruct, RTDose, DICOMImage).



        Raises
        ------
        ValueError
            If no instance with the given SOPInstanceUID is found in the loaded DICOM files.
        NotImplementedError
            If a reader for this modality type is not implemented yet.

        Examples
        --------
        >>> loader = DICOMLoader("/path/to/dicom/files")
        >>> loader.load()
        >>> instance = loader.read_instance("1.2.840.113619.2.55.3.1234")
        >>> print(instance)
        """
        # TODO:
        # use get_instance method
        # Search for the instance in self.dataset
        found_instance = None
        for patient in self.dataset:
            for study in patient.studies.values():
                for series in study.series.values():
                    found_instance = series.instances.get(sop_instance_uid)
                    if found_instance:
                        break
                if found_instance:
                    break
            if found_instance:
                break

        if found_instance is None:
            raise ValueError(f"Instance with SOPInstanceUID '{sop_instance_uid}' not found.")

        # Determine the modality and use the appropriate reader
        modality = found_instance.Modality
        filepath = found_instance.filepath

        if modality in ["CT", "MR", "PT"]:
            return DICOMImageReader(filepath).read()

        elif modality == "RTSTRUCT":
            return RTStructReader(filepath).read()

        elif modality == "RTDOSE":
            return RTDoseReader(filepath).read()

        elif modality == "REG":
            return REGReader(filepath).read()

        elif modality == "RTPLAN":
            return RTPlanReader(filepath).read()

        elif modality == "RTRECORD":
            return RTRecordReader(filepath).read()

        else:
            raise NotImplementedError(f"A reader for {modality} type is not implemented yet.")

    def _read_embedded(self, dataset):
        """
        Reads an embedded DICOM dataset from a RAW file based on its modality and returns
        the appropriate object using modality-specific readers.

        This method is used internally to handle embedded datasets in RAW files. It selects
        the appropriate reader based on the modality of the embedded dataset and reads the
        data accordingly.

        Parameters
        ----------
        dataset : pydicom.Dataset
            The embedded DICOM dataset to be read. This dataset is typically extracted
            from a RAW file.

        Returns
        -------
        object
            The appropriate representation of the embedded dataset based on its modality.
            For example, if the dataset represents a CT image, it returns a `DICOMImage`
            object. If the dataset represents an RTSTRUCT, it returns an `RTStruct` object.
        """
        if dataset.Modality in ["CT", "MR", "PT"]:
            return DICOMImageReader(dataset).read()
        elif dataset.Modality == "RTSTRUCT":
            return RTStructReader(dataset).read()
        elif dataset.Modality == "RTDOSE":
            return RTDoseReader(dataset).read()
        elif dataset.Modality == "REG":
            return REGReader(dataset)
        elif dataset.Modality == "RTPLAN":
            return RTPlanReader(dataset)
        elif dataset.Modality == "RTRECORD":
            return RTRecordReader(dataset)

    def visualize_series_references(
        self,
        patient_id=None,
        output_file=None,
        view=True,
        per_patient=False,
        exclude_modalities=None,
        exclude_series=[],
        include_uid=False,
        rankdir="BT",
    ):
        """
        Visualizes the series-level associations for all patients or a specific patient using
        Graphviz. Each series is represented as a box, and an edge is drawn from a series to its
        referenced series. The patient ID will be the top node, followed by root series (e.g., CT)
        and referenced series (e.g., RTDOSE).

        Parameters
        ----------
        patient_id : str or None, optional
            If provided, only generates the graph for the specified patient. This takes priority
            over `per_patient`.
        output_file : str or None, optional
            The name of the output file for the graph visualization. If None, the graph will not
            be saved. If `per_patient=True`, this will serve as a prefix for the patient-specific
            files.
        view : bool, optional
            Whether to automatically view the graph after it's generated using `matplotlib` or
            another viewer.
        per_patient : bool, optional
            Whether to create separate graphs for each patient. If False, all patients are
            visualized in one graph.
        exclude_modalities : list of str, optional
            A list of modalities to exclude from the visualization. If None, all modalities are
            included.
        exclude_series : list of str, optional
            A list of SeriesInstanceUIDs to exclude from the graph. If None or empty, no series
            are excluded.
        include_uid : bool, optional
            Whether to include the (SOP/Series)InstanceUID in the label for each node.
        rankdir : str, optional
            The direction of the graph layout. Must be one of ['RL', 'LR', 'BT', 'TB'].


        Returns
        -------
        None
        """
        if rankdir not in ["RL", "LR", "BT", "TB"]:
            raise ValueError(f"{rankdir} is not a valid option for rankdir")

        # define color mappings based on modality
        modality_colors = {
            "CT": "lightsteelblue",
            "MR": "lightseagreen",
            "PT": "lightcoral",
            "RTSTRUCT": "navajowhite",
            "RTPLAN": "lightgoldenrodyellow",
            "RTDOSE": "lightpink",
            "RTRECORD": "lavender",
            "REG": "thistle",
            "DEFAULT": "lightgray",
        }
        patient_color = "dodgerblue"
        raw_subgraph_color = "lightcyan"

        def get_modality_color(modality):
            """
            Helper function to get the background color based on the modality.
            """
            return modality_colors.get(modality, modality_colors["DEFAULT"])

        def get_referenced_series(series):
            referenced_series = set()
            for sop_uid, instance in series.instances.items():
                if instance.referenced_series:
                    for ref_series in instance.referenced_series:
                        referenced_series.add(ref_series)

            return referenced_series

        def get_other_referenced_series(series):
            referenced_series = set()
            for sop_uid, instance in series.instances.items():
                if instance.other_referenced_series:
                    for ref_series in instance.other_referenced_series:
                        referenced_series.add(ref_series)

            return referenced_series

        def exclude_referenced(
            series, exclude_modalities=exclude_modalities, exclude_series=exclude_series
        ):
            if exclude_modalities and series.Modality in exclude_modalities:
                return True
            if exclude_series and series.SeriesInstanceUID in exclude_series:
                return True
            return False

        def create_graph(patient_id, series_dict, graph):
            """
            Helper function to create a graph for a specific patient.
            """
            # Add patient ID as the top node for each patient's graph
            graph.node(
                patient_id,
                label=(
                    f"Patient ID: {patient_id}\n"
                    f"{series_dict[list(series_dict.keys())[0]].PatientName}"
                ),
                fillcolor=patient_color,
                style="filled",
            )

            all_nodes_set = set()
            referencing_nodes_set = set()

            # Add nodes and edges for each series
            for series_uid, series in series_dict.items():
                # Exclude modalities if specified
                if exclude_modalities and series.Modality in exclude_modalities:
                    continue

                if series.SeriesInstanceUID in exclude_series:
                    continue

                if series.Modality == "RAW":
                    continue

                if exclude_modalities and "RAW" in exclude_modalities:
                    if series.is_embedded_in_raw:
                        continue

                # get the color based on modality
                node_color = get_modality_color(series.Modality)

                # handle embedded series in RAW
                if series.is_embedded_in_raw:
                    # create a subgraph for the embedded series within the RAW series
                    with graph.subgraph(
                        name=f"cluster_{series.raw_series_reference.SeriesInstanceUID}"
                    ) as subgraph:
                        if include_uid:
                            label_r = (
                                f"MIM Session: {series.raw_series_reference.SeriesDescription}"
                                "\nSeriesInstanceUID: "
                                f"{series.raw_series_reference.SeriesInstanceUID}"
                            )
                        else:
                            label_r = (
                                f"MIM Session: {series.raw_series_reference.SeriesDescription}"
                            )
                        subgraph.attr(
                            label=label_r,
                            color="black",
                            style="filled",
                            fillcolor=raw_subgraph_color,
                        )

                        # italicize the embedded series
                        if include_uid:
                            label = (
                                f"{series.Modality}: {series.SeriesDescription}"
                                f"\n{series.SeriesInstanceUID}"
                            )
                        else:
                            label = f"{series.Modality}: {series.SeriesDescription}"
                        subgraph.node(
                            series.SeriesInstanceUID,
                            label=label,
                            shape="box",
                            style="filled",
                            fontcolor="black",
                            fontname="Times-Italic",
                            fillcolor=node_color,
                        )
                        all_nodes_set.add(series.SeriesInstanceUID)
                else:
                    if series.Modality in ["RTSTRUCT", "RTPLAN", "RTDOSE", "RTRECORD"]:
                        # Add each instance separately as a node
                        for sop_uid, instance in series.instances.items():
                            if include_uid:
                                label = (
                                    f"{series.Modality}: {series.SeriesDescription}"
                                    f"\nSOPInstanceUID: {sop_uid}"
                                )
                            else:
                                label = f"{series.Modality}: {series.SeriesDescription}"
                            node_color = get_modality_color(series.Modality)
                            graph.node(
                                sop_uid,
                                label=label,
                                style="filled",
                                fillcolor=node_color,
                            )
                            all_nodes_set.add(sop_uid)

                            # Check for direct references to other nodes
                            if series.Modality == "RTSTRUCT":
                                referenced_series_list = instance.referenced_series
                                if referenced_series_list:
                                    for referenced_series in referenced_series_list:
                                        if not exclude_referenced(referenced_series):
                                            referencing_nodes_set.add(instance.SOPInstanceUID)

                                            # Draw an edge pointing *upwards* from the referenced
                                            # node to the referencing node
                                            graph.edge(
                                                instance.SOPInstanceUID,
                                                referenced_series.SeriesInstanceUID,
                                            )

                                else:
                                    # Check for FrameOfReference registeration
                                    if series.frame_of_reference_registered:
                                        for (
                                            frame_of_ref_series
                                        ) in series.frame_of_reference_registered:
                                            if frame_of_ref_series.Modality in ["CT", "MR", "PT"]:
                                                if not exclude_referenced(frame_of_ref_series):
                                                    referencing_nodes_set.add(
                                                        instance.SOPInstanceUID
                                                    )

                                                    graph.edge(
                                                        instance.SOPInstanceUID,
                                                        frame_of_ref_series.SeriesInstanceUID,
                                                        style="dashed",
                                                    )
                                                    break
                            else:
                                referenced_instances_list = instance.referenced_instances
                                if referenced_instances_list:
                                    for referenced_instance in referenced_instances_list:
                                        if not exclude_referenced(
                                            referenced_instance.parent_series
                                        ):
                                            referencing_nodes_set.add(instance.SOPInstanceUID)

                                            # Draw an edge pointing *upwards* from the referenced
                                            # node to the referencing node
                                            graph.edge(
                                                instance.SOPInstanceUID,
                                                referenced_instance.SOPInstanceUID,
                                            )

                                else:
                                    # Check if FrameOfReference registration
                                    if series.frame_of_reference_registered:
                                        for (
                                            frame_of_ref_series
                                        ) in series.frame_of_reference_registered:
                                            if frame_of_ref_series.Modality in ["CT", "MR", "PT"]:
                                                if not exclude_referenced(frame_of_ref_series):
                                                    referencing_nodes_set.add(
                                                        instance.SOPInstanceUID
                                                    )
                                                    graph.edge(
                                                        instance.SOPInstanceUID,
                                                        frame_of_ref_series.SeriesInstanceUID,
                                                        style="dashed",
                                                    )
                                                    break
                    else:
                        # Add each series as a node (box)
                        if include_uid:
                            label = (
                                f"{series.Modality}: {series.SeriesDescription}"
                                f"\nSeriesInstanceUID: {series.SeriesInstanceUID}"
                            )
                        else:
                            label = f"{series.Modality}: {series.SeriesDescription}"
                        node_color = get_modality_color(series.Modality)
                        graph.node(
                            series.SeriesInstanceUID,
                            label=label,
                            style="filled",
                            fillcolor=node_color,
                        )
                        all_nodes_set.add(series.SeriesInstanceUID)

                        # Check if the series references another series directly
                        referenced_series_set = get_referenced_series(series)
                        if referenced_series_set:
                            referenced_series = referenced_series_set.pop()
                            if not exclude_referenced(referenced_series):
                                referenced_series_uid = referenced_series.SeriesInstanceUID
                                referencing_nodes_set.add(series.SeriesInstanceUID)

                                # Draw an edge pointing *upwards* from the referenced series to the
                                # referencing series
                                graph.edge(
                                    series.SeriesInstanceUID,
                                    referenced_series_uid,
                                )

                        # Check for REG modality and moving image reference (other_referenced_sid)
                        if series.Modality == "REG":
                            other_referenced_series_set = get_other_referenced_series(series)
                            if other_referenced_series_set:
                                other_referenced_series = other_referenced_series_set.pop()
                                if not exclude_referenced(other_referenced_series):
                                    referencing_nodes_set.add(series.SeriesInstanceUID)
                                    # Draw a dashed blue edge for the REG moving image reference
                                    graph.edge(
                                        series.SeriesInstanceUID,
                                        other_referenced_series.SeriesInstanceUID,
                                        style="dotted",
                                    )

            # Root nodes are those that don't reference other series
            root_nodes = all_nodes_set - referencing_nodes_set

            # Connect the patient node to the root series nodes
            for root in root_nodes:
                graph.edge(root, patient_id)  # Root points to the patient (arrows go up)

            return graph

        def display_graph_with_matplotlib(dot_source, dpi=1000):
            """
            Displays the Graphviz graph using matplotlib, by converting SVG to PNG.
            """
            # Generate the PNG in memory
            graph_svg = graphviz.Source(dot_source)
            png_data = graph_svg.pipe(format="png")

            # Load the PNG into a Matplotlib plot
            img = mpimg.imread(BytesIO(png_data), format="png")

            # Display the PNG using matplotlib
            plt.figure(figsize=(12, 12), dpi=dpi)  # Adjust figure size for large graphs
            plt.imshow(img)
            plt.axis("off")
            plt.show()

        def display_graph_in_jupyter(dot_source):
            """
            Displays the graph inline in a Jupyter notebook using IPython's display and SVG.
            """
            from IPython.display import display, SVG

            graph_svg = graphviz.Source(dot_source)
            svg = graph_svg.pipe(format="svg").decode("utf-8")
            display(SVG(svg))

            # display(SVG(graphviz.Source(dot_source).pipe(format="svg")))

        def in_jupyter():
            try:
                from IPython import get_ipython

                if "IPKernelApp" in get_ipython().config:
                    return True
                else:
                    return False
            except Exception:
                return False

        is_jupyter = in_jupyter()

        # if patient_id is specified, only generate for that patient
        if patient_id:
            series_dict = self.dicom_files.get(patient_id, {})
            if not series_dict:
                print(f"No data found for patient {patient_id}")
                return
            graph = graphviz.Digraph(comment=f"DICOM Series Associations for {patient_id}")
            graph.attr("node", shape="box", style="filled", fillcolor="lightgray", color="black")
            graph.attr(rankdir=rankdir)

            # Create a graph for the specified patient
            graph = create_graph(patient_id, series_dict, graph)

            # Render and view the graph for the specified patient
            if output_file:
                graph.render(f"{output_file}_{patient_id}", format="svg")

            if view:
                if is_jupyter:
                    display_graph_in_jupyter(graph.source)
                else:
                    display_graph_with_matplotlib(graph.source)

        elif per_patient:
            # Create separate graphs for each patient
            for patient_id, series_dict in self.dicom_files.items():
                graph = graphviz.Digraph(comment=f"DICOM Series Associations for {patient_id}")
                graph.attr(
                    "node", shape="box", style="filled", fillcolor="lightgray", color="black"
                )

                graph.attr(rankdir=rankdir)

                # Create a graph for each patient
                graph = create_graph(patient_id, series_dict, graph)

                # Render and view each patient's graph
                if output_file:
                    patient_output_file = f"{output_file}_{patient_id}.svg"
                    graph.render(patient_output_file, format="svg")

                if view:
                    if is_jupyter:
                        display_graph_in_jupyter(graph.source)
                    else:
                        display_graph_with_matplotlib(graph.source)

        else:
            # Create a combined graph for all patients
            graph = graphviz.Digraph(comment="DICOM Series Associations")
            graph.attr("node", shape="box", style="filled", fillcolor="lightgray", color="black")

            graph.attr(rankdir=rankdir)

            # Loop through all patients and their series
            for patient_id, series_dict in self.dicom_files.items():
                # Add each patient's series to the combined graph
                graph = create_graph(patient_id, series_dict, graph)

            # Render and view the combined graph
            if output_file:
                graph.render(output_file, format="svg")

            if view:
                if is_jupyter:
                    display_graph_in_jupyter(graph.source)
                else:
                    display_graph_with_matplotlib(graph.source)

    def __iter__(self):
        """
        Iterates over all loaded patients in the dataset.

        This method allows the DICOMLoader to be iterated over, yielding `PatientNode` instances.
        Each `PatientNode` contains studies (`StudyNode`s), which in turn contain series
        (`SeriesNode`s) and instances (`InstanceNode`s).

        Yields
        ------
        PatientNode
            The next `PatientNode` instance in the dataset.

        Examples
        --------
        >>> loader = DICOMLoader("/path/to/dicom/files")
        >>> loader.load()
        >>> for patient in loader:
        ...     print(patient.PatientName, patient.PatientID)
        'John Doe', 12345
        'Jane Smith', 67890
        """
        if self.dataset:
            yield from self.dataset

    def __repr__(self):
        """
        Returns a string representation of the `DICOMLoader` instance, including the dataset path,
        dataset ID, and the number of patients in the dataset.

        Returns
        -------
        str
            A string representation of the `DICOMLoader` object.
        """
        dataset_id = self.dataset.dataset_id if self.dataset else "None"
        num_patients = len(self.dataset) if self.dataset else 0
        return (
            f"DICOMLoader(path='{self.path}', "
            f"dataset_id='{dataset_id}', "
            f"NumPatients={num_patients})"
        )
