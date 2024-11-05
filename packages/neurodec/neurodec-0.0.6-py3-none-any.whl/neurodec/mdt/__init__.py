from __future__ import annotations
from enum import auto, IntEnum
import logging

import numpy as np
from numpy.typing import ArrayLike
import requests
import rich
import time
from typing import Callable, Collection, Optional, Tuple, Union

from .auth import get_credentials
from .encoding import decode_array, encode_array, hash_array, hash_array_with_sorting

logger = logging.getLogger(__name__)

_API_URL = "http://0.0.0.0:8001"

wait = True


class Status(IntEnum):
    """The status of the objects in the Neurodec Myoelectric Digital Twin"""

    NEW = 0
    PENDING = auto()
    PROCESSING = auto()
    READY = auto()
    ERROR = auto()


class TissueType(IntEnum):
    """The types of tissues inside a volume conductor."""

    SKIN = 0
    FAT = 1
    BONE = 2
    MUSCLE = 3
    ELECTRODE = 4


class ElectrodeLayouts(IntEnum):
    """Possible orderings for grids of electrodes on the skin"""
    ROW_MAJOR = 0
    COLUMN_MAJOR = auto()
    SNAKE_HORIZONTAL = auto()
    SNAKE_VERTICAL = auto()
    SPIRAL_CLOCKWISE = auto()
    SPIRAL_COUNTERCLOCKWISE = auto()


# Random seed to be used in new() calls when not explicitly given as parameter.
DEFAULT_RANDOM_SEED = 0


# Default radius to be used for fibers during generation.
DEFAULT_FIBERS_RADIUS = 4e-5


def get_version() -> Optional[str]:
    """Returns the version of the Myoelectric Digital Twin

    If a connection cannot be established with the MDT for any reason
    (ConnectionError, Timeout, HTTPError, ...) this function returns
    None.

    """

    try:
        response = requests.get(f"{_API_URL}/", timeout=5)
        return response.json()["mdt"] if response.ok else None
    except requests.exceptions.RequestException:
        return None


def get_user() -> Optional[dict]:
    """Returns the current user of the MDT

    If the credentials are not valid, returns None. If the credentials are
    valid and the MDT can be reached, returns a dictionary with the
    user information.

    """

    try:
        response = requests.get(f"{_API_URL}/users/auth", json={"credentials": get_credentials()}, timeout=5)
        return response.json() if response.ok else None
    except requests.exceptions.RequestException:
        return None


def is_connected() -> bool:
    """Returns True if we can connect to the MDT, False otherwise"""
    return get_version() is not None and get_user() is not None


def print_connection_status():
    """Pretty prints the connection status of the Myoelectric Digital Twin

    Prints a message that indicates if a connection can be established and if
    the credentials are valid. This is meant for interactive use. For programmatic
    use, see is_connected.

    """

    # If we can get the version, the MDT is online and well.
    version = get_version()
    if version is None:
        rich.print(
            f"[bold red]Error[/bold red]: Could not connect to the [blue]Myoelectric Digital Twin[/blue]. "
            f"Please check that the API URL ({_API_URL}) is correct. "
            f"If the URL is correct and the error persists, the MDT may be offline.")
        return
    else:
        rich.print(
            f"The [blue]Myoelectric Digital Twin[/blue] version {version} is online.")

    user = get_user()
    if user is None:
        rich.print(
            f"[bold red]Error[/bold red]: Could not login to the [blue]Myoelectric Digital Twin[/blue]. "
            f"Please verify that your credentials are correct.")
    else:
        rich.print(
            f"You are connected as [green]{user['email']}[/green].")


class MDTObject:
    """Base class for Neurodec Myoelectric Digital Twin classes"""

    _url_prefix: str = ""

    def __init__(self, dictionary: dict):
        """Initialize object from a mapping

        This function is not meant to be called directly by users. Use
        the `new` class method instead.

        """

        self._id = dictionary["id"]
        self._status = Status(dictionary["status"])
        self._data_json = None

    def __str__(self):
        """String representation of a surface"""
        return f"{self.__class__.__name__}({self._id}, {str(self._status)})"

    @property
    def id(self) -> int:
        """Returns the ID of the object"""
        return self._id

    @property
    def status(self) -> Status:
        """Returns the up-to-date status of the object, by performing an API request."""
        self._status = self._get_metadata(self._id)._status
        return self._status

    @classmethod
    def _get_metadata(cls, id: int):
        response = requests.get(f"{_API_URL}/{cls._url_prefix}/{id}/metadata", json={"credentials": get_credentials()})
        if not response.ok:
            raise ValueError("The metadata could not be retrieved.")

        return cls(response.json())

    @classmethod
    def _new_request(cls, json=None, url_suffix=None):
        if json is None:
            json = {}
        json.update({"credentials": get_credentials()})
        request_url = f"{_API_URL}/{cls._url_prefix}"
        if url_suffix is not None:
            request_url += "/" + url_suffix
        response = requests.post(request_url, json=json)
        if not response.ok:
            if not is_connected():
                print_connection_status()
            raise ValueError(f"The {cls.__name__} could not be created.")

        # Wait the status to be READY if requested.
        obj = cls(response.json())
        if wait:
            obj.wait()

        return obj

    @classmethod
    def _search_from_hash(cls, json: dict):
        # Add authentication data.
        json.update({"credentials": get_credentials()})

        # Check if the object exists, using hashes instead of arrays to speed-up data transmission.
        response = requests.get(f"{_API_URL}/{cls._url_prefix}/search_from_hash", json=json)
        if not response.ok:
            if not is_connected():
                print_connection_status()
            raise ValueError(f"Failed to perform hash-based search for {cls.__name__} object.")

        # Send back None if the object was not found, or the MDTObject if it was in the database.
        metadata_dict = response.json()["metadata"]
        return None if metadata_dict is None else cls(metadata_dict)

    def wait(self):
        """Wait for the object to be ready"""

        while True:
            if self.status is Status.READY:
                break
            elif self.status is Status.ERROR:
                raise RuntimeError("An error occurred during the simulation.")

            time.sleep(1.0)

    def _retrieve_data(self):
        """Retrieve the data of this object.

        In this context, the term "data" refers to whatever is calculated by the API services that makes the object
        change its status from PENDING to READY.
        """
        # Get the raw data if we don't already have it.
        if self._data_json is None:
            # Wait for the data to be ready.
            self.wait()

            response = requests.get(f"{_API_URL}/{self._url_prefix}/{self.id}/data",
                                    json={"credentials": get_credentials()})
            if not response.ok:
                raise RuntimeError("The data of this object could not be retrieved.")
            self._data_json = response.json()

    @staticmethod
    def monitor_status(objects: Collection["MDTObject"], polling_interval: float = 5.0,
                       event_handler: Optional[Callable[["MDTObject", Status, Status], None]] = None,
                       print_function: Optional[Callable[[str], None]] = None):
        """Monitor the status of a set of objects until they are all ready.

        The function polls the API periodically until all monitored objects reach either the READY or ERROR state. In
        addition, when an object changes its state, the user is informed of the event by a message.

        Args:
            objects: A list of MDTObject instances to be monitored.
            polling_interval: Time to wait (in seconds) between subsequent API requests.
            event_handler: A function object to handle status changes. It should accept the object that just changed
                its status, the old status and the new status. If not given, a default handler is used, which creates
                a message every time an object changes its status to READY or to ERROR. The message is then passed to
                the function "print_function".
            print_function: Function to be called when an object changes its state and therefore the user need to be
                notified. The function should accept a string (the message to be shown to the user). By default, the
                'print' function is used. You can instead pass, eg, the "info" method of a logger instance, or a
                function that sends a notification to your phone to let you know that the resource is ready. This
                parameter is ignored if a custom event_handler is used instead.
        """
        for i, obj in enumerate(objects):
            if not isinstance(obj, MDTObject):
                raise ValueError(f"Object at index {i} is not of type MDTObject (type: {type(obj).__name__}).")

        # Make a copy of the array, so that we can modify it as needed.
        objects = [o for o in objects]

        # Get the last known status of each object.
        statuses = [o._status for o in objects]

        # States that make the resource drop from the list of objects of interest.
        exit_states = [Status.READY, Status.ERROR]

        # If the event handler is not given, create a default one.
        if event_handler is None:
            # If the print function is not given, fall back to console printing.
            if print_function is None:
                print_function = print

            def event_handler(obj, old_status, new_status):
                # A human-readable string that identifies the resource.
                source = f"{type(obj).__name__}[id={obj.id}]"

                # If the object is now ready or if there was an error, send a message to the user.
                if new_status == Status.READY:
                    msg = f"\a{source} was processed and is now ready!"
                elif new_status == Status.ERROR:
                    msg = f"\aThere was an error while processing {source}."
                else:
                    msg = None

                # If needed, notify the user.
                if msg is not None:
                    print_function(msg)

        while len(objects) > 0:
            # Wait for some time to reduce the traffic.
            time.sleep(polling_interval)

            # For each object, check it they have changed status. If so, handle the change.
            for obj, status in zip(objects, statuses):
                if obj.status != status:
                    event_handler(obj, Status(status), Status(obj._status))

            # Update the list of monitored objects and their states.
            objects = [o for o in objects if o._status not in exit_states]
            statuses = [o._status for o in objects]


class Surface(MDTObject):
    """A surface of an anatomical model"""

    _url_prefix: str = "surfaces"

    def __init__(self, dictionary: dict):
        """Initialize surface from a mapping

        This function is not meant to be called directly by users. Use
        Surface.new instead.

        """

        super().__init__(dictionary)
        self._type = TissueType(dictionary["type"])
        self._label = None
        self._vertices = None
        self._triangles = None
        self._image_label = None

    def __str__(self):
        """String representation of a surface"""
        return f"Surface({self._id}, {str(self._status)}, {str(self._type)})"

    @property
    def type(self) -> TissueType:
        """Returns the type of the surface"""
        return self._type

    @classmethod
    def new(cls, vertices: ArrayLike, triangles: ArrayLike, tissue_type: TissueType, label: Optional[str] = None,
            force_computation: bool = False) -> Surface:
        """Create a new surface

        Creates a new surface from raw data. This will initiate a call to the
        Neurodec Myoelectric Digital Twin (MDT) API that will save the surface,
        preprocess it, and return its metadata in the form of a dict.

        Args:
            vertices: A numpy array of float with a shape of (N, 3) that
                contains the location of the vertices.
            triangles: A numpy array of unsigned integers with a shape of
                (M, 3) that contains the indices of the vertices for each
                triangle.
            tissue_type: The tissue enclosed by this surface, see neurodec.mdt.TissueType.
            label: A human-readable name to easily identify the surface. If not given, the label will be autogenerated
                from the surface type. Note that this label exists only locally and not in the database. This means that
                if two Surface objects are created with different labels but with same vertices, triangles and types,
                the result will be two instances that share the same id and status, despite having different labels.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The new surface. If another surfaces with the same parameters already exits, that one will be returned
            instead of creating a new surface.
        """

        # Make sure the vertices can be converted to a numpy array of (N, 3).
        vertices = np.array(vertices, dtype=np.float64)
        if vertices.ndim != 2 or vertices.shape[1] != 3:
            raise ValueError(
                "The vertices must be a 2D array of floats with a shape of (N, 3), not"
                f" {vertices.shape}."
            )

        # Same thing for the triangles.
        triangles = np.array(triangles, dtype=np.uint64)
        if triangles.ndim != 2 or triangles.shape[1] != 3:
            raise ValueError(
                "The triangles must be a 2D array of unsigned integers with a shape of"
                f" (M, 3), not {triangles.shape}."
            )

        # Avoid unused vertices and out of bounds triangle indices.
        indices = np.unique(triangles)
        if indices.max() >= len(vertices):
            raise ValueError(
                "The triangle indices is equal to or exceed the number of vertices"
                f" ({indices.max()} vs {len(vertices)})."
            )

        # Check if the surface exists already, by transmitting a hash instead of the surface data - which may take a
        # while depending on the size of the vertices and triangles.
        surface = cls._search_from_hash({"surface_hash": hash_array_with_sorting(vertices), "type": tissue_type.value})

        # If the surface does not exist, we need to upload the vertices and triangles to create the metadata as usual.
        if surface is None:
            surface_data = {"type": tissue_type.value}
            surface_data.update(encode_array(vertices, "vertices"))
            surface_data.update(encode_array(triangles, "triangles"))
            data = {
                "surface": surface_data,
                "force_computation": force_computation,
            }
            surface = cls._new_request(json=data)

        # Assign all properties and return the surface object.
        surface._vertices = vertices
        surface._triangles = triangles
        surface._label = label if label is not None else f"{tissue_type.name.lower()}_{surface.id}"
        return surface

    @property
    def vertices(self):
        """Retrieve the vertices of this Surface.

        Return:
            A NumPy array of float with a shape of (N, 3) that contains the location of the vertices.
        """
        if self._vertices is None:
            self._retrieve_data()
            self._vertices = decode_array(self._data_json, "vertices")
        return self._vertices.copy()

    @property
    def triangles(self):
        """Retrieve the triangles of this Surface.

        Return:
            A NumPy array of unsigned integers with a shape of (M, 3) that contains the indices of the vertices for each
            triangle.
        """
        if self._triangles is None:
            self._retrieve_data()
            self._triangles = decode_array(self._data_json, "triangles")
        return self._triangles.copy()

    @property
    def label(self) -> str:
        """Returns the human-readable label of this Surface.

        This is the human-readable label (a string) that was passed to Surface.new(). Do not confuse it with the
        image_label property.

        Returns:
            The human-readable label of this Surface, if one was given during the Surface.new() call. If the surface was
            extracted from a Tetrahedra instance, the label will be None.
        """
        return self._label

    @property
    def image_label(self) -> Optional[int]:
        """Returns the image label of this Surface.

        Returns:
            If this Surface was extracted from an Image, the label that identified it is returned. If this surface was
            created using Surface.new(), then its image_label will be None.
        """
        return self._image_label


class Image(MDTObject):
    """A 3D image containing tissue information."""

    _url_prefix: str = "images"

    @classmethod
    def new(
            cls,
            image: ArrayLike,
            voxel_sizes: Union[Tuple[float, float, float], ArrayLike],
            labels: dict,
            ignore_labels: Optional[Collection[int]] = None,
            skin_thickness: float = 2e-3,
            force_computation: bool = False
    ) -> Image:
        """Create a new 3D image.

        Create a new 3D image. Once received on the server, it is processed so that its spatial resolution is as uniform
        as possible.

        Args:
            image: A NumPy array of integers with a shape of (A, B, C) that contains voxels whose values represent
                labelled tissues. Each label should correspond to a specific component of the arm. See the argument
                'labels' for more details.
            voxel_sizes: A tuple or NumPy array that represents the spatial resolution of the image in the X, Y and Z
                directions. This is used to associate the voxel at coordinates (i, j, k) to the point in space with
                Cartesian coordinates (i*voxel_sizes[0], j*voxel_sizes[1], k*voxel_sizes[2]). If two of the values are
                equal and the remaining one is larger, then the image is pre-processed to increase the resolution in the
                coarsest direction.
                .. Important:: The resolution has to be given in meters.
            labels: Dictionary that specifies what each label in the image corresponds to, in terms of tissues. More
                precisely, in each image one label should be used to identify skin, one for fat, a couple for the bones
                (most likely, radius and ulna), several labels to identify the different muscles. Optionally, one or
                more labels can be given to identify electrodes. Note that if electrodes are not part of an image, they
                can still be added later using the Electrode class. Labels should be given as a dictionary with the
                following keys and values:
                - TissueType.SKIN: the label for the skin, as a positive integer;
                - TissueType.FAT: the label for the fat, as a positive integer;
                - TissueType.BONE: the labels for the bones, as a list of positive integers (can be empty);
                - TissueType.MUSCLE: the labels for the muscles, as a list of positive integers;
                - TissueType.ELECTRODE: the labels for the electrodes, as a list of positive integers (can be empty).
                Labels must be unique. As an example, it is an error to have the label '42' both as skin label and as
                part of the list of muscle labels. The label '0' is a special value that is used to represent empty
                space and therefore cannot be used. Note that not all labels in the image need to be associated to a
                tissue. As an example, while creating an MRI, some markers may have been placed on the skin to identify
                reference locations. These markers are not part of the volume conductor and therefore their label can be
                ignored while extracting the tetrahedral mesh. In practice, all voxels in the image whose label does not
                appear in the `labels` variables are ignored and treated as if they represented void space (label '0').
                For each of these, a warning is issued to prevent issues related to forgotten labels, unless they are
                explicitly included in the `ignore_labels` variable.
            ignore_labels: List of labels that appear in the image, but not in `labels`, and that can be safely ignored
                without issuing a warning. By default, this list is empty, meaning that a warning is issued for every
                missing label.
            skin_thickness: After increasing the resolution of the image, the skin is re-computed so that it wraps
                around the arm with the specified thickness (2mm by default).
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The new image. If another image with the same parameters already exits, that one will be returned instead
            of creating a new image.
        """

        # Make sure that the inputs are interpreted as NumPy arrays.
        image = np.asarray(image, dtype=int)
        voxel_sizes = np.asarray(voxel_sizes)

        # Check that the input is a 3D image.
        if image.ndim != 3:
            raise ValueError(f"Input 'image' must be an array of integers with 3 dimensions. It has {image.ndim} "
                             f"dimension(s) instead.")

        # Check that the voxel is a NumPy array with 3 elements.
        if voxel_sizes.shape != (3, ):
            raise ValueError(f"Input 'voxel_sizes' must be an array with shape (3,) (single dimension of length 3). "
                             f"It has instead the shape {voxel_sizes.shape}.")

        largest_resolution = np.max(voxel_sizes)
        if largest_resolution >= 1e-2:
            logger.warning(f"The largest image resolution is {largest_resolution}, which appears to be quite large for "
                           f"an anatomical image. Remember that lengths are all in meters, meaning that the larges "
                           f"resolution is interpreted as {largest_resolution}m. If the intended unit was different and"
                           f" you meant for example {largest_resolution}mm, consider rescaling 'voxel_sizes' by the "
                           f"appropriate factor.")

        # Initialize 'ignore_labels' if it was not given by the user.
        if ignore_labels is None:
            ignore_labels = []

        # Check that all mandatory labels are present.
        mandatory_tissues = [TissueType.SKIN, TissueType.FAT, TissueType.BONE, TissueType.MUSCLE]
        for tissue in mandatory_tissues:
            if tissue not in labels:
                raise ValueError(f"Missing tissue '{tissue.name}' in 'labels'.")

        # Complete the labels with optional ones.
        non_list_tissues = [TissueType.SKIN, TissueType.FAT]
        list_tissues = [TissueType.BONE, TissueType.MUSCLE, TissueType.ELECTRODE]
        tissues = non_list_tissues + list_tissues
        labels = {tissue: labels.get(tissue, []) for tissue in tissues}
        labels_lists = [[labels[t]] for t in non_list_tissues] + [labels[t] for t in list_tissues]

        for i in range(len(tissues) - 1):
            # Make sure that labels are all positive integers.
            for label in labels_lists[i]:
                if not isinstance(label, (int, np.integer)) or label < 1:
                    raise ValueError(
                        f"Label for '{tissues[i].name}' tissue is invalid: expected positive integer, got "
                        f"'{label}'.")

            # Make sure there are no label repetitions.
            if len(set(labels_lists[i])) != len(labels_lists[i]):
                raise ValueError(f"Invalid labels for tissue '{tissues[i].name}': all values must be unique. Got: "
                                 f"{labels_lists[i]}")
            for j in range(i + 1, len(tissues)):
                if any(label in labels_lists[j] for label in labels_lists[i]):
                    raise ValueError(
                        f"Invalid labels: '{tissues[i].name}' and '{tissues[j].name}' share at least one "
                        f"label. {tissues[i].name}: {labels_lists[i]}, {tissues[j].name}: "
                        f"{labels_lists[j]}.")

        # Check that all values in the image are associated with a label. If not, issue warnings as needed.
        all_labels = sum(labels_lists, [0])
        unique_labels = np.unique(image)
        for image_label in unique_labels:
            if image_label not in all_labels and image_label not in ignore_labels:
                logger.warning(
                    f"Image label '{image_label}' does not has not been given tissue information. If this is"
                    f" intentional, consider adding '{image_label}' to the argument 'ignore_labels'.")

        # Also, make sure that the labels to ignore are valid, meaning that they all exist in the image and none of them
        # appear in the 'labels' dictionary.
        non_existing_labels = [label for label in ignore_labels if label not in unique_labels]
        if len(non_existing_labels) > 0:
            raise ValueError(
                f"The labels {non_existing_labels} were part of 'ignore_labels', but they are not present "
                f"in the original image.")

        non_ignorable_labels = [label for label in ignore_labels if label in all_labels]
        if len(non_ignorable_labels) > 0:
            raise ValueError(
                f"The labels {non_ignorable_labels} were part of 'ignore_labels', but they are present in "
                f"the 'labels' dictionary.")

        # Check if the image exists already, by transmitting a hash instead of the image data - which may take a while
        # depending on the size of the array.
        search_data = {
            "image_hash": hash_array(image),
            "labels": labels,
            "skin_thickness": skin_thickness,
        }
        search_data.update(encode_array(voxel_sizes, "voxel_sizes"))
        image_metadata = cls._search_from_hash(search_data)

        # If the image does not exist, we need to upload the image and create the metadata as usual.
        if image_metadata is None:
            data = {
                "force_computation": force_computation,
                "labels": labels,
                "skin_thickness": skin_thickness,
            }
            data.update(encode_array(image, "image"))
            data.update(encode_array(voxel_sizes, "voxel_sizes"))
            image_metadata = cls._new_request(json=data)

        # Finally, send back the result.
        return image_metadata


class Tetrahedra(MDTObject):
    """A labelled tetrahedral mesh."""

    _url_prefix: str = "tetrahedra"
    _surfaces: Optional[Collection[Surface]] = None

    @classmethod
    def from_image(
            cls,
            image: Image,
            sizes: float = 1e-3,
            distance: float = 1e-3,
            force_computation: bool = False
    ) -> Tetrahedra:
        """Create a labelled tetrahedral mesh from a set of voxels.

        Args:
            image: The labelled 3D image from which the tetrahedral mesh should be extracted.
            sizes: This parameter controls the size of surface facets. Each surface facet has a surface Delaunay ball
                which is a ball circumscribing the surface facet and centered on the surface patch.
            distance: This parameter controls the approximation error of boundary and subdivision surfaces. It provides
                an upper bound for the distance between the circumcenter of a surface facet and the center of a surface
                Delaunay ball of this facet.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
        Returns:
            The metadata of the new tetrahedra. If another object with the same parameters already exits, that one will
            be returned instead of building a new one.
        """
        data = {
            "force_computation": force_computation,
            "image_id": image.id,
            "sizes": sizes,
            "distance": distance,
        }
        return cls._new_request(json=data, url_suffix="from_image")

    @classmethod
    def from_surfaces(
            cls,
            surfaces: Collection[Surface],
            sizes: float = 1e-3,
            distance: float = 1e-3,
            force_computation: bool = False
    ) -> Tetrahedra:
        """Create a labelled tetrahedral mesh from a set of surfaces.

        Args:
            surfaces: The surface meshes from which the tetrahedral mesh should be built. There must be exactly one
                surface of type TissueType.SKIN, one of type TissueType.SKIN and at least one of type TissueType.MUSCLE.
            sizes: This parameter controls the size of surface facets. Each surface facet has a surface Delaunay ball
                which is a ball circumscribing the surface facet and centered on the surface patch.
            distance: This parameter controls the approximation error of boundary and subdivision surfaces. It provides
                an upper bound for the distance between the circumcenter of a surface facet and the center of a surface
                Delaunay ball of this facet.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
        Returns:
            The metadata of the new tetrahedra. If another object with the same parameters already exits, that one will
            be returned instead of building a new one.
        """
        data = {
            "force_computation": force_computation,
            "surfaces": [s.id for s in surfaces],
            "sizes": sizes,
            "distance": distance,
        }
        return cls._new_request(json=data, url_suffix="from_surfaces")

    @property
    def surfaces(self):
        if self._surfaces is None:
            self._retrieve_data()
            self._surfaces = []
            for id, label in self._data_json["surfaces_data"]:
                s = Surface._get_metadata(id)
                s._image_label = label
                self._surfaces.append(s)

        return self._surfaces

    def _surfaces_of_type(self, tissue_type):
        surfaces = [s for s in self.surfaces if s.type == tissue_type]
        if len(surfaces) == 0:
            logger.warning(f"Could not find any surface of type '{tissue_type.name}' associated to this Tetrahedra "
                           f"instance.")
        return surfaces

    @property
    def skin(self):
        """Retrieve the skin surface of this mesh.

        Returns:
            A Surface object representing the skin of the mesh. If this Tetrahedra object was created from an Image, the
            surface is extracted from the mesh once the image is processed. If the object was created from a set of
            surfaces, this surface is the same that was given as input.
        """
        skins = self._surfaces_of_type(TissueType.SKIN)
        if len(skins) != 1:
            raise RuntimeError(f"Every Tetrahedra instance must have exactly one skin surface, however {len(skins)} "
                               f"were found.")
        return skins[0]

    @property
    def muscles(self):
        """Retrieve the muscle surfaces of this mesh.

        Returns:
            A list of Surface objects representing the muscles of the mesh. If this Tetrahedra object was created from
            an Image, the surfaces are extracted from the mesh once the image is processed. If the object was created
            from a set of surfaces, these surfaces are the same that were given as input.
        """
        return self._surfaces_of_type(TissueType.MUSCLE)


def default_conductivities() -> dict[TissueType, ArrayLike]:
    """Create a dictionary containing default conductivities for each tissue type.

    Returns:
        A dictionary in the form {tissue: conductivity} where tissue is one of the values of the TissueType
        enumeration, and conductivity is either a scalar (isotropic tissue) or the principal components (anisotropic
        tissue).
    """
    return {
        TissueType.SKIN: 0.17,
        TissueType.FAT: 5.73e-2,
        TissueType.BONE: 8.2e-2,
        TissueType.MUSCLE: [0.5, 0.1, 0.1],
        TissueType.ELECTRODE: 2.0
    }


class Conductor(MDTObject):
    """A volume conductor"""

    _url_prefix: str = "conductor"

    @classmethod
    def new(
        cls,
        tetrahedra: Tetrahedra,
        skin_conductivity: float = 0.17,
        fat_conductivity: float = 5.73e-2,
        bone_conductivity: float = 8.2e-2,
        muscle_conductivity: Optional[Union[float, ArrayLike]] = None,
        electrode_conductivity: float = 2.0,
        force_computation: bool = False
    ) -> Conductor:
        """Create a new volume conductor

        Creates a new volume conductor from surfaces. This will initiate a call
        to the Neurodec Myoelectric Digital Twin (MDT) API that will build
        the conductor and return its metadata in the form of a dict.

        Args:
            tetrahedra: The labelled tetrahedral mesh used to define the volume conductor.
            skin_conductivity: Conductivity of skin tissue. This tissue is assumed to be isotropic and therefore only
                one value is required to define the conductivity tensor.
            fat_conductivity: Conductivity of fat tissue. This tissue is assumed to be isotropic and therefore only one
                value is required to define the conductivity tensor.
            bone_conductivity: Conductivity of bone tissue. This tissue is assumed to be isotropic and therefore only
                one value is required to define the conductivity tensor.
            muscle_conductivity: Principal conductivity components of muscle tissue. This tissue is assumed to be
                anisotropic in general, with the principal components being (C1, C2, C2). More precisely, the
                conductivity C1 is the one associated with the local direction of the fibers. The parameter
                muscle_conductivity can be:
                - A scalar Cm. In this case, it is assumed that the conductivity is isotropic, and the vector of
                  principal components is created as (Cm, Cm, Cm).
                - A 2-dimensional vector in the form (C1, C2). In this case, a third value is added to complete the
                  principal components as (C1, C2, C2).
                - A 3-dimensional vector in the form (C1, C2, C3). The vector is passed as-is to the API. However, a
                  warning is issued if C2 != C3.
                - None: the default values (0.5, 0.1, 0.1) are used for the principal components.
            electrode_conductivity: Conductivity of electrode material. This material is assumed to be isotropic and
                therefore only one value is required to define the conductivity tensor.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new conductor. If another conductor with the
            same parameters already exits, that one will be returned instead of
            building a new one.
        """
        # If muscle conductivities are not given, use the default ones. If they are given, make sure they become a list
        # in the form [c1, c2, c3].
        if muscle_conductivity is None:
            muscle_conductivity = [0.5, 0.1, 0.1]
        elif np.isscalar(muscle_conductivity):
            muscle_conductivity = [muscle_conductivity] * 3
        else:
            muscle_conductivity = np.asarray(muscle_conductivity)
            if muscle_conductivity.shape == (2,):
                c1, c2 = muscle_conductivity
                muscle_conductivity = [c1, c2, c2]
            elif muscle_conductivity.shape == (3,):
                c1, c2, c3 = muscle_conductivity
                if not np.allclose(c2, c3):
                    logger.warning(f"Received 3 muscle conductivities, with c2 != c3. {c2=}, {c3=}.")
                muscle_conductivity = [c1, c2, c3]
            else:
                raise RuntimeError(f"Principal conductivity components for a muscle must be given as either a scalar or"
                                   f" an array with 2 or 3 components. An array with shape {muscle_conductivity.shape} "
                                   f"was received.")

        # Encode the input data.
        json = {
            "force_computation": force_computation,
            "tetrahedra": tetrahedra.id,
            "conductivities": {
                TissueType.SKIN: skin_conductivity,
                TissueType.FAT: fat_conductivity,
                TissueType.BONE: bone_conductivity,
                TissueType.MUSCLE: muscle_conductivity,
                TissueType.ELECTRODE: electrode_conductivity
            }
        }

        return cls._new_request(json=json)


class Electrode(MDTObject):
    """An electrode"""

    _url_prefix: str = "electrodes"

    def __init__(self, dictionary: dict):
        """Initialize surface from a mapping

        This function is not meant to be called directly by users. Use
        Surface.new instead.

        """

        super().__init__(dictionary)
        self._radius = dictionary["radius"]
        self._location = np.array(dictionary["location"])
        self._impedance = dictionary["impedance"]

    @classmethod
    def new(
            cls,
            location: ArrayLike,
            radius: float,
            impedance: float,
            force_computation: bool = False
    ) -> Electrode:
        """Create a circular electrode.

        Args:
            location: NumPy array with shape (3,) containing the 3D coordinates of the electrode.
            radius: Radius of the electrode.
            impedance: Impedance of the electrode-skin interface (in ohms).
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new electrode. If another electrode with the same parameters already exists, it will be
            returned instead of building a new one.
        """
        # Encode the parameters.
        json = {
            "force_computation": force_computation,
            "radius": radius,
            "impedance": impedance,
        }
        json.update(encode_array(location, "location"))

        # Send the request.
        return cls._new_request(json=json)

    @property
    def radius(self):
        return self._radius

    @property
    def location(self):
        return self._location.copy()


class ElectrodeCollection(MDTObject):
    _electrodes: Optional[Collection[Electrode]] = None
    _radius: Optional[float] = None
    _impedance: Optional[float] = None

    @classmethod
    def _send_request_and_set_electrode_properties(cls, json, radius, impedance):
        # Send the request, then set the radius & impedance and then return the metadata instance.
        metadata = cls._new_request(json=json)
        metadata._radius = radius
        metadata._impedance = impedance
        return metadata

    @property
    def electrodes(self):
        if self._electrodes is None:
            self._retrieve_data()
            electrode_locations = decode_array(self._data_json, "electrode_locations")
            self._electrodes = [
                Electrode.new(location, self._radius, self._impedance) for location in electrode_locations
            ]

        return self._electrodes


class ElectrodeBracelet(ElectrodeCollection):
    _url_prefix = "electrode_bracelets"

    @classmethod
    def new(
            cls,
            skin: Surface,
            radius: float,
            impedance: float,
            first_electrode_location: ArrayLike,
            rings_normal: ArrayLike,
            n_rings: int,
            distance_between_rings: float,
            n_electrodes_per_ring: int,
            distance_between_electrodes: Optional[float] = None,
            force_computation: bool = False
    ) -> ElectrodeBracelet:
        """Generate a bracelet of electrodes on the given surface.

        A bracelet is a series of electrodes arranged in multiple rings that should wrap around the given surface.

        Args:
            skin: A Surface object with type SKIN where the electrodes will be placed.
            radius: Radius of an electrode. The same value is used for all electrodes in the bracelet.
            impedance: Impedance of an electrode. The same value is used for all electrodes in the bracelet.
            first_electrode_location: A numpy array containing 3D coordinates of the first electrode of the first ring.
                Does not have to be precisely on the skin mesh - the point will be projected onto it.
            rings_normal: A numpy array containing the direction of the normal vector defining the bracelet section planes.
                Note, that all the rings have the same normal vector.
            n_rings: The number of electrode rings in the bracelet. If larger than 1, the initial bracelet plan is shifted
                in the direction of the normal vector for a distance distance_between_rings.
            distance_between_rings: Distance between electrode rings in the bracelet, in meters. Note, that all the rings
                are equidistant.
            n_electrodes_per_ring: The number of electrodes in rings. The electrodes are ordered in a clockwise direction
                with respect to the rings_normal. If the distance_between_rings parameter is 0, all the rings will have the
                same number of electrodes uniformly covering the corresponding section circumferences. It will likely
                result in different inter electrode distances for different rings.
            distance_between_electrodes: The distance between electrodes in a ring, in meters. If not None, will generate
                equidistant in a clockwise direction starting from the first_electrode_location.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
        """
        # Encode the parameters.
        json = {
            "surface_id": skin.id,
            "n_rings": n_rings,
            "distance_between_rings": distance_between_rings,
            "n_electrodes_per_ring": n_electrodes_per_ring,
            "distance_between_electrodes": distance_between_electrodes,
            "force_computation": force_computation,
        }
        json.update(encode_array(first_electrode_location, "first_electrode_location"))
        json.update(encode_array(rings_normal, "rings_normal"))
        return cls._send_request_and_set_electrode_properties(json, radius, impedance)


class ElectrodeGrid(ElectrodeCollection):
    _url_prefix = "electrode_grids"

    @classmethod
    def new(
            cls,
            skin: Surface,
            radius: float,
            impedance: float,
            corners: ArrayLike,
            shape: Tuple[int, int],
            layout: ElectrodeLayouts,
            smooth_surface: bool = True,
            force_computation: bool = False
    ) -> ElectrodeGrid:
        """Generate a grid of electrodes on the given surface.

        Args:
            skin: A Surface object with type SKIN where the electrodes will be placed.
            radius: Radius of an electrode. The same value is used for all electrodes in the bracelet.
            impedance: Impedance of an electrode. The same value is used for all electrodes in the bracelet.
            corners: A NumPy array with shape (4, 3) representing the 3D corners of a rectangular patch of skin that
                should contain a grid of electrodes. The four corners are to be given in the order top-left (grid[0]),
                top-right (grid[1]), bottom-left (grid[2]), bottom-right (grid[3]). The points do not need to define an
                actual rectangle, but rather an approximation of it. In addition, they do not have to be precisely on
                the skin mesh.
            shape: A NumPy array with shape (2,), containing the rows and columns (respectively as first and second
                element) of the grid of electrodes.
            layout: Ordering of the electrodes. The final result - accessible via the `electrodes` property - is a list
                of electrodes and it is therefore necessary to specify how to order them. The allowed values have the
                following meanings:
                - ROW_MAJOR: electrodes are rearranged row-by-row.
                - COLUMN_MAJOR: electrodes are rearranged column-by-column.
                - SNAKE_HORIZONTAL: like ROW_MAJOR, but every odd-numbered row is reversed.
                - SNAKE_VERTICAL: like COLUMN_MAJOR, but every odd-numbered column is reversed.
                - SPIRAL_CLOCKWISE: creates a spiral path starting with the first row of the grid and proceeding in
                    clockwise order.
                - SPIRAL_COUNTERCLOCKWISE: creates a spiral path starting with the first column of the grid and proceeding
                    in counterclockwise order.
            smooth_surface: If True (default), use a smoothed version of the skin surface during the evaluation of the
                grid. This generally provides more regular grids. The final grid is still projected on the original
                surface mesh.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
        """
        # Check that parameters are correctly set.
        corners = np.asarray(corners)
        if corners.shape != (4, 3):
            raise ValueError(f"Argument 'corners' has shape {corners.shape}. Expected: (4, 3).")

        # Encode the parameters.
        json = {
            "surface_id": skin.id,
            "rows": shape[0],
            "cols": shape[1],
            "layout": layout.value,
            "smooth_surface": smooth_surface,
            "force_computation": force_computation,
        }
        json.update(encode_array(corners.reshape(-1), "grid_corners"))
        return cls._send_request_and_set_electrode_properties(json, radius, impedance)


class ForwardSolution(MDTObject):
    """A forward solution"""

    _url_prefix: str = "forward"

    @classmethod
    def new(
            cls,
            conductor: Conductor,
            electrodes: Collection[Electrode],
            use_impedance: bool = True,
            force_computation: bool = False
    ) -> ForwardSolution:
        """Create a new forward solution

        Creates a new forward solution from a volume conductor and electrodes. This
        will initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API that
        will build the forward solution and return its metadata.

        Args:
            conductor: The conductor for which we compute the forward solution.
            electrodes: The electrodes used to record EMGs.
            use_impedance: If True, use the impedance provided by the electrodes. If False, the impedance will be
                ignored (which roughly corresponds to a conductor model with infinite-impedance electrodes).
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new forward solution. If another forward solution with
            the same parameters already exits, that one will be returned instead of
            building a new one.
        """
        json = {
            "force_computation": force_computation,
            "conductor_id": conductor.id,
            "electrode_ids": [e.id for e in electrodes],
            "use_impedance": use_impedance,
        }

        return cls._new_request(json=json)


class Fibers(MDTObject):
    """The fibers of a muscle"""

    _url_prefix: str = "fibers"

    def __init__(self, dictionary: dict):
        """Initialize fibers from a mapping

        This function is not meant to be called directly by users. Use Fibers.new() instead.
        """
        super().__init__(dictionary)
        self._random_seed = dictionary["random_seed"]
        self._fibers_3d = None

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(
            cls,
            surface: Surface,
            plane_origins: ArrayLike,
            plane_normals: ArrayLike,
            n_fibers: Optional[int] = None,
            fibers_radius: Optional[float] = None,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
    ) -> Fibers:
        f"""Create new fibers for a muscle

        Creates new fibers from a surface. This will initiate a call
        to the Neurodec Myoelectric Digital Twin (MDT) API that will generate
        fibers and return their metadata.

        Args:
            surface: The surface for which the fibers are generated.
            plane_origins: A numpy array with a shape of (2, 3) that defines
                the origins of the planes where fibers start and end.
            plane_normals: A numpy array with a shape of (2, 3) that defines
                the normals of the planes where fibers start and end.
            n_fibers: number of fibers to be generated in the muscle. It cannot
                be given if fibers_radius is given as well.
            fibers_radius: radius of the fibers. If n_fibers is None, the
                number of fibers is calculated from this parameter. If both
                n_fibers and fibers_radius are None, a default radius of
                {DEFAULT_FIBERS_RADIUS * 1e6:.1f} micrometers is used.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.
        Returns:
            The metadata of the new fibers. If another set of fibers with the
            same parameters already exits, those will be returned instead of
            building new ones.
        """
        # Convert the planes to numpy arrays and verify the shape.
        plane_origins = np.array(plane_origins, dtype=np.float32)
        if plane_origins.shape != (2, 3):
            raise ValueError(
                "The plane origins must be a 2D array of floats with a shape of (2, 3),"
                f" not {plane_origins.shape}."
            )
        plane_normals = np.array(plane_normals, dtype=np.float32)
        if plane_normals.shape != (2, 3):
            raise ValueError(
                "The plane normals must be a 2D array of floats with a shape of (2, 3),"
                f" not {plane_normals.shape}."
            )

        json = {
            "force_computation": force_computation,
            "surface_id": surface.id,
            "plane_origins": plane_origins.ravel().tolist(),
            "plane_normals": plane_normals.ravel().tolist(),
            "random_seed": random_seed,
        }

        # Make sure only one parameter is given between n_fibers and fibers_radius.
        if n_fibers is not None and fibers_radius is not None:
            raise ValueError(f"Only one argument between 'n_fibers' and 'fibers_radius' can be different from None. "
                             f"Got {n_fibers=} and {fibers_radius=} instead.")

        # Add to the JSON the number of fibers OR the fiber radius.
        if n_fibers is not None:
            json["n_fibers"] = n_fibers
        else:
            json["fibers_radius"] = fibers_radius if fibers_radius is not None else DEFAULT_FIBERS_RADIUS

        return cls._new_request(json=json)

    @property
    def vertices(self):
        """Retrieve the fibers generated inside the muscle.

        Return:
            A NumPy array with shape (n_fibers, n_sections, 3) containing the coordinates of the fiber nodes.
        """
        if self._fibers_3d is None:
            self._retrieve_data()
            self._fibers_3d = decode_array(self._data_json, "fibers_3d")
        return self._fibers_3d


class FiberProperties(MDTObject):
    """Properties of individual fibers"""

    _url_prefix: str = "fiber_properties"

    def __init__(self, dictionary: dict):
        """Initialize fiber properties from a mapping

        This function is not meant to be called directly by users. Use FiberProperties.new() instead.
        """
        super().__init__(dictionary)
        self._random_seed = dictionary["random_seed"]

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(cls,
            fibers: Fibers,
            neuromuscular_junction_min: float = 0.5,
            neuromuscular_junction_max: float = 0.5,
            tendon_1_ratio_min: float = 0.,
            tendon_1_ratio_max: float = 0.,
            tendon_2_ratio_min: float = 0.,
            tendon_2_ratio_max: float = 0.,
            velocity_min: float = 3.,
            velocity_max: float = 3.,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
            ) -> FiberProperties:
        """Create new fiber properties for individual fibers

        Creates new fiber properties from each fiber of a muscle. This will
        initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate fiber properties and return their metadata.

        The input values define lower and upper bounds for each of the fiber parameters. Individual fiber properties
        will be then randomly sampled from a uniform distribution within corresponding ranges.

        Args:
            fibers: The fibers for which to generate the individual properties.
            neuromuscular_junction_min: the lower bound for the neuromuscular junction location ratio (between 0 and 1).
            neuromuscular_junction_max: the upper bound for the neuromuscular junction location ratio (between 0 and 1).
            tendon_1_ratio_min: the lower bound for the tendon 1 ratio (between 0 and 1).
            tendon_1_ratio_max: the upper bound for the tendon 1 ratio (between 0 and 1).
            tendon_2_ratio_min: the lower bound for the tendon 2 ratio (between 0 and 1).
            tendon_2_ratio_max: the upper bound for the tendon 2 ratio (between 0 and 1).
            velocity_min: the lower bound for the action potential propagation velocity, in m/s.
            velocity_max: the upper bound for the action potential propagation velocity, in m/s.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.

        Returns:
            The metadata of the new fiber properties. If another set of fiber
            properties with the same parameters already exits, those will be returned
            instead of building new ones.

        """

        json = {
            "neuromuscular_junction_min": neuromuscular_junction_min,
            "neuromuscular_junction_max": neuromuscular_junction_max,
            "tendon_1_ratio_min": tendon_1_ratio_min,
            "tendon_1_ratio_max": tendon_1_ratio_max,
            "tendon_2_ratio_min": tendon_2_ratio_min,
            "tendon_2_ratio_max": tendon_2_ratio_max,
            "velocity_min": velocity_min,
            "velocity_max": velocity_max,
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "random_seed": random_seed,
        }

        return cls._new_request(json=json)


class FiberBasis(MDTObject):
    """Basis (leadfields/transfer function) for the fibers of a single muscle"""

    _url_prefix: str = "fiber_basis"

    @classmethod
    def new(cls, fibers: Fibers, forward_solution: ForwardSolution, force_computation: bool = False) -> FiberBasis:
        """Create new fiber basis for a single muscle

        Creates new fiber basis for the fibers of a muscle. This will
        initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate the fiber basis and return their metadata.

        Args:
            fibers: The fibers for which to generate the motor units.
            forward_solution: The forward solution of the volume conductor
                where the fibers live.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new fiber basis. If another fiber basis
            with the same parameters already exits, it will be returned
            instead of building a new one.

        """

        json = {
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "forward_solution_id": forward_solution.id,
        }

        return cls._new_request(json=json)


class MotorUnits(MDTObject):
    """Motor units of a single muscle"""

    _url_prefix: str = "motor_units"

    def __init__(self, dictionary: dict):
        """Initialize motor units from a mapping

        This function is not meant to be called directly by users. Use MotorUnits.new() instead.
        """
        super().__init__(dictionary)
        self._sizes = None
        self._random_seed = dictionary["random_seed"]

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(
            cls,
            fibers: Fibers,
            n_motor_units: int,
            area_min: float = 0.1,
            area_max: float = 0.7,
            distribution_radius: float = 0.95,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
    ) -> MotorUnits:
        """Create new motor units for a single muscle

        Creates new motor units by grouping the fibers of a muscle. This will
        initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate motor units and return their metadata.

        Args:
            fibers: The fibers for which to generate the motor units.
            n_motor_units: The number of motor units to generate.
            area_min: The minimum area of motor units.
            area_max: The maximum area of the motor units.
            distribution_radius: The maximum radius inside a unit circle at which the motor unit centers can be created.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.

        Returns:
            The metadata of the new motor units. If another set of motor
            units with the same parameters already exits, those will be returned
            instead of building new ones.

        """

        json = {
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "n_motor_units": n_motor_units,
            "distribution_radius": distribution_radius,
            "area_min": area_min,
            "area_max": area_max,
            "random_seed": random_seed,
        }

        return cls._new_request(json=json)

    @property
    def sizes(self) -> ArrayLike:
        """Returns the sizes of the MUs

        Returns:
            A NumPy array of length N (total number of motor units). The i-th entry corresponds to the number of fibers
            associated to the i-th motor unit.
        """
        if self._sizes is None:
            self._retrieve_data()
            self._sizes = np.array([len(decode_array(p, "partition")) for p in self._data_json["partition"]],
                                   dtype=int)
        return self._sizes


class MotorUnitsActionPotentials(MDTObject):
    """The action potentials for all motor units of a single muscle"""

    _data: Optional[ArrayLike] = None
    _url_prefix: str = "muap"

    @classmethod
    def new(
            cls,
            fibers: Fibers,
            fiber_basis: FiberBasis,
            fiber_properties: FiberProperties,
            motor_units: MotorUnits,
            sampling_frequency: float,
            force_computation: bool = False
    ) -> MotorUnitsActionPotentials:
        """Create new motor units action potentials for a single muscle

        Creates new motor units action potentials (MUAPs) for the fibers of a muscle.
        This will initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate MUAPs and return their metadata.

        Args:
            fibers: The fibers for which to generate the MUAPs.
            fiber_basis: The fiber basis for which to generate the MUAPs.
            fiber_properties: The fiber properties for which to generate the MUAPs.
            motor_units: The motor units for which to generate the MUAPs.
            sampling_frequency: The sampling frequency of the output MUAPs, in Hertz.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new MUAPs. If another set of MUAPs with the same
            parameters already exits, those will be returned instead of generating a
            new ones.

        """

        json = {
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "fiber_basis_id": fiber_basis.id,
            "fiber_properties_id": fiber_properties.id,
            "motor_units_id": motor_units.id,
            "sampling_frequency": sampling_frequency,
        }

        return cls._new_request(json=json)

    @property
    def data(self) -> ArrayLike:
        """Returns the data associated with this MUAP"""
        if self._data is None:
            self._retrieve_data()
            self._data = decode_array(self._data_json, "muap")
        return self._data


class ImpulseTrains(MDTObject):
    """The impulse trains of the motor units of a single muscle"""

    _url_prefix: str = "impulse_trains"

    def __init__(self, dictionary: dict):
        """Initialize impulse trains from a mapping

        This function is not meant to be called directly by users. Use ImpulseTrains.new() instead.
        """
        super().__init__(dictionary)
        self._data = None
        self._random_seed = dictionary["random_seed"]

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(
            cls,
            muaps: MotorUnitsActionPotentials,
            activation: ArrayLike,
            recruitment_rate: float = 75.0,
            excitation_frequency_min: float = 8.0,
            excitation_frequency_max: float = 32.0,
            inter_impulse_variance: float = 0.2,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
    ) -> ImpulseTrains:
        """Create new impulse trains for the motor units of a single muscle

        Creates new impulse trains for the motor units of a muscle.  This will initiate
        a call to the Neurodec Myoelectric Digital Twin (MDT) API that will generate
        impulse trains and return their metadata.

        Args:
            muaps: The MUAPs of the motor units for which the impulse trains are
                generated.
            activation: The % of muscle contraction in time.
            recruitment_rate: The recruitment rate of the motor units.
            excitation_frequency_min: The minimum excitation frequency of the motor
                units.
            excitation_frequency_max: The maximum excitation frequency of the motor
                units.
            inter_impulse_variance: The inter impulse variance.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.

        Returns:
            The metadata of the new impulse trains. If another set of impulse trains
            with the same parameters already exits, those will be returned instead of
            generating new ones.

        """

        json = {
            "force_computation": force_computation,
            "muap_id": muaps.id,
            "recruitment_rate": recruitment_rate,
            "excitation_frequency_min": excitation_frequency_min,
            "excitation_frequency_max": excitation_frequency_max,
            "inter_impulse_variance": inter_impulse_variance,
            "random_seed": random_seed,
        }
        json.update(encode_array(activation, "activation"))

        return cls._new_request(json=json)

    @property
    def data(self) -> ArrayLike:
        """Returns the data associated with this impulse train"""
        if self._data is None:
            self._retrieve_data()
            self._data = decode_array(self._data_json, "impulse_trains")
        return self._data


class Electromyography(MDTObject):
    """The electromyography of a single muscle"""

    _url_prefix: str = "emg"

    def __init__(self, dictionary: dict):
        """Initialize object from a mapping

        This function is not meant to be called directly by users. Use
        the `new` class method instead.

        """

        super().__init__(dictionary)
        self._data = None

    @property
    def data(self) -> ArrayLike:
        """Returns the EMG data"""

        # Get the data if we don't already have it.
        if self._data is None:
            # Wait for the data to be ready.
            self.wait()

            response = requests.get(f"{_API_URL}/{self._url_prefix}/{self.id}/data",
                                    json={"credentials": get_credentials()})
            if not response.ok:
                raise ValueError("The EMG data could not be retrieved.")
            self._data = np.array(response.json()["data"], dtype=np.float32)

        return self._data

    @classmethod
    def new(cls, impulse_trains: ImpulseTrains, force_computation: bool = False) -> Electromyography:
        """Create a new electromyography (EMG) recording of a single muscle

        Creates a new EMG recording of a muscle.  This will initiate a call to the
        Neurodec Myoelectric Digital Twin (MDT) API that will generate a new EMG
        recording and return its metadata.

        Args:
            impulse_trains: The impulse trains of the muscle.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new electromyography recording. If another EMG
            recording with the same parameters already exits, it will be returned
            instead of generating a new one.

        """

        json = {
            "force_computation": force_computation,
            "impulse_trains_id": impulse_trains.id,
        }

        return cls._new_request(json=json)
