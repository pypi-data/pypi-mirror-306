import logging
from typing import Any
from typing import ClassVar

from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.metadata import Metadata
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.lazy_object import LazyObject
from pydantic import PrivateAttr

from amsdal_models.classes.base import BaseModel
from amsdal_models.classes.decorators.private_property import PrivateProperty
from amsdal_models.classes.utils import build_class_meta_schema_reference
from amsdal_models.classes.utils import build_class_schema_reference
from amsdal_models.classes.utils import is_partial_model

logger = logging.getLogger(__name__)


class MetadataHandler(BaseModel):
    _class_address: ClassVar[str]

    _object_id: str = PrivateAttr()
    _object_version: str = PrivateAttr()
    _metadata_lazy: LazyObject[Metadata] = PrivateAttr()

    def __init__(self, **kwargs: Any):
        metadata = kwargs.pop('_metadata', None)
        super().__init__(**kwargs)

        if metadata is not None:
            self._metadata_lazy = LazyObject(
                lambda: metadata if isinstance(metadata, Metadata) else Metadata(**metadata),
            )
        else:
            self._metadata_lazy = LazyObject(self.build_metadata)

    @PrivateProperty
    def _metadata(self) -> Metadata:
        return self._metadata_lazy.value

    @PrivateProperty
    def is_latest(self) -> bool:
        return self._metadata.is_latest

    def build_metadata(self) -> Metadata:
        """
        Builds the metadata object for this record.

        Returns:
            Metadata: The metadata object for this record.
        """
        config_manager = AmsdalConfigManager()

        class_name = self.__class__.__name__

        if is_partial_model(self.__class__) and class_name.endswith('Partial'):
            class_name = class_name[: -len('Partial')]

        address = Address(
            resource=config_manager.get_connection_name_by_model_name(self.__class__.__name__),
            class_name=class_name,
            class_version=Versions.LATEST,
            object_id=self._object_id,
            object_version=self._object_version,
        )

        return Metadata(
            address=address,
            class_schema_reference=build_class_schema_reference(self.__class__),
            class_meta_schema_reference=build_class_meta_schema_reference(self.__class__, self._object_id),
            class_schema_type=self.schema_type,
        )

    def get_metadata(self) -> Metadata:
        """
        Returns the metadata object for this record.

        Returns:
            Metadata: The metadata object for this record.
        """
        return self._metadata
