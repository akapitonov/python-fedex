"""
Close Service Module

This package contains classes to close shipment with documents
"""

from datetime import datetime
from ..base_service import FedexBaseService


class FedexCloseServiceRequest(FedexBaseService):
    """
    This class allows you to get the shipping charges for a particular address.
    You will need to populate the data structures in self.RequestedShipment,
    then send the request.
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        The optional keyword args detailed on L{FedexBaseService}
        apply here as well.

        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object.
        """

        self._config_obj = config_obj

        # Holds version info for the VersionId SOAP object.
        self._version_info = {"service_id": "clos", "major": "5",
                              "intermediate": "0", "minor": "0"}

        self.RequestedShipment = None
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexCloseServiceRequest, self).__init__(
            self._config_obj, "CloseService_v5.wsdl", *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        This is the data that will be used to create your close request. Create
        the data structure and get it ready for the WSDL request.
        """
        # Default to Fedex
        self.CarrierCode = "FDXE"

        self.ActionType = "CLOSE"

        self.ReprintCloseDate = datetime.now()

        close_document_specification = self.client.factory.create("CloseDocumentSpecification")
        close_document_specification.CloseDocumentTypes = "MANIFEST"
        self.CloseDocumentSpecification = close_document_specification

        manifest_reference_detail = self.client.factory.create("CloseManifestReferenceDetail")
        manifest_reference_detail.Type = "CUSTOMER_REFERENCE"
        manifest_reference_detail.Value = "string"
        self.CloseManifestReferenceDetail = manifest_reference_detail

        # This is good to review if you"d like to see what the data structure
        # looks like.
        self.logger.debug(self)

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.

        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(),
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.closeWithDocuments(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            ReprintCloseDate=self.ReprintCloseDate,
            CloseDocumentSpecification=self.CloseDocumentSpecification, )


class FedexReprintCloseDocumentsServiceRequest(FedexCloseServiceRequest):
    def _prepare_wsdl_objects(self):
        close_document_specification = self.client.factory.create("CloseDocumentSpecification")
        close_document_specification.CloseDocumentTypes = "MANIFEST"
        self.CloseDocumentSpecification = close_document_specification
        self.TrackingNumber = ""

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.

        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(),
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.reprintGroundCloseDocuments(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            TrackingNumber=self.TrackingNumber,
            CloseDocumentSpecification=self.CloseDocumentSpecification, )
