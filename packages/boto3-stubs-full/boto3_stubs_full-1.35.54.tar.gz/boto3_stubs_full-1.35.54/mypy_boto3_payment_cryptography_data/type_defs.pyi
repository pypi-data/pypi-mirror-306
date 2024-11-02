"""
Type annotations for payment-cryptography-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_payment_cryptography_data.type_defs import CurrentPinAttributesTypeDef

    data: CurrentPinAttributesTypeDef = ...
    ```
"""

import sys
from typing import Any, Dict, Mapping

from .literals import (
    DukptDerivationTypeType,
    DukptEncryptionModeType,
    DukptKeyVariantType,
    EmvEncryptionModeType,
    EmvMajorKeyDerivationModeType,
    EncryptionModeType,
    KeyCheckValueAlgorithmType,
    KeyDerivationFunctionType,
    KeyDerivationHashAlgorithmType,
    MacAlgorithmType,
    MajorKeyDerivationModeType,
    PaddingTypeType,
    PinBlockFormatForEmvPinChangeType,
    PinBlockFormatForPinDataType,
    PinBlockLengthPositionType,
    PinBlockPaddingTypeType,
    SessionKeyDerivationModeType,
    SymmetricKeyAlgorithmType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CurrentPinAttributesTypeDef",
    "AmexCardSecurityCodeVersion1TypeDef",
    "AmexCardSecurityCodeVersion2TypeDef",
    "AsymmetricEncryptionAttributesTypeDef",
    "CardHolderVerificationValueTypeDef",
    "CardVerificationValue1TypeDef",
    "CardVerificationValue2TypeDef",
    "DynamicCardVerificationCodeTypeDef",
    "DynamicCardVerificationValueTypeDef",
    "DiscoverDynamicCardVerificationCodeTypeDef",
    "CryptogramVerificationArpcMethod1TypeDef",
    "CryptogramVerificationArpcMethod2TypeDef",
    "ResponseMetadataTypeDef",
    "Emv2000AttributesTypeDef",
    "EmvCommonAttributesTypeDef",
    "MasterCardAttributesTypeDef",
    "DukptAttributesTypeDef",
    "DukptDerivationAttributesTypeDef",
    "DukptEncryptionAttributesTypeDef",
    "EcdhDerivationAttributesTypeDef",
    "EmvEncryptionAttributesTypeDef",
    "SymmetricEncryptionAttributesTypeDef",
    "VisaAmexDerivationOutputsTypeDef",
    "PinDataTypeDef",
    "Ibm3624NaturalPinTypeDef",
    "Ibm3624PinFromOffsetTypeDef",
    "Ibm3624PinOffsetTypeDef",
    "Ibm3624PinVerificationTypeDef",
    "Ibm3624RandomPinTypeDef",
    "MacAlgorithmDukptTypeDef",
    "SessionKeyDerivationValueTypeDef",
    "VisaPinTypeDef",
    "VisaPinVerificationValueTypeDef",
    "VisaPinVerificationTypeDef",
    "SessionKeyAmexTypeDef",
    "SessionKeyEmv2000TypeDef",
    "SessionKeyEmvCommonTypeDef",
    "SessionKeyMastercardTypeDef",
    "SessionKeyVisaTypeDef",
    "TranslationPinDataIsoFormat034TypeDef",
    "AmexAttributesTypeDef",
    "VisaAttributesTypeDef",
    "CardGenerationAttributesTypeDef",
    "CardVerificationAttributesTypeDef",
    "CryptogramAuthResponseTypeDef",
    "DecryptDataOutputTypeDef",
    "EncryptDataOutputTypeDef",
    "GenerateCardValidationDataOutputTypeDef",
    "GenerateMacOutputTypeDef",
    "ReEncryptDataOutputTypeDef",
    "TranslatePinDataOutputTypeDef",
    "VerifyAuthRequestCryptogramOutputTypeDef",
    "VerifyCardValidationDataOutputTypeDef",
    "VerifyMacOutputTypeDef",
    "VerifyPinDataOutputTypeDef",
    "WrappedKeyMaterialTypeDef",
    "EncryptionDecryptionAttributesTypeDef",
    "ReEncryptionAttributesTypeDef",
    "GenerateMacEmvPinChangeOutputTypeDef",
    "GeneratePinDataOutputTypeDef",
    "MacAlgorithmEmvTypeDef",
    "PinGenerationAttributesTypeDef",
    "PinVerificationAttributesTypeDef",
    "SessionKeyDerivationTypeDef",
    "TranslationIsoFormatsTypeDef",
    "DerivationMethodAttributesTypeDef",
    "GenerateCardValidationDataInputRequestTypeDef",
    "VerifyCardValidationDataInputRequestTypeDef",
    "WrappedKeyTypeDef",
    "MacAttributesTypeDef",
    "VerifyAuthRequestCryptogramInputRequestTypeDef",
    "GenerateMacEmvPinChangeInputRequestTypeDef",
    "DecryptDataInputRequestTypeDef",
    "EncryptDataInputRequestTypeDef",
    "GeneratePinDataInputRequestTypeDef",
    "ReEncryptDataInputRequestTypeDef",
    "TranslatePinDataInputRequestTypeDef",
    "VerifyPinDataInputRequestTypeDef",
    "GenerateMacInputRequestTypeDef",
    "VerifyMacInputRequestTypeDef",
)

CurrentPinAttributesTypeDef = TypedDict(
    "CurrentPinAttributesTypeDef",
    {
        "CurrentPinPekIdentifier": str,
        "CurrentEncryptedPinBlock": str,
    },
)
AmexCardSecurityCodeVersion1TypeDef = TypedDict(
    "AmexCardSecurityCodeVersion1TypeDef",
    {
        "CardExpiryDate": str,
    },
)
AmexCardSecurityCodeVersion2TypeDef = TypedDict(
    "AmexCardSecurityCodeVersion2TypeDef",
    {
        "CardExpiryDate": str,
        "ServiceCode": str,
    },
)
AsymmetricEncryptionAttributesTypeDef = TypedDict(
    "AsymmetricEncryptionAttributesTypeDef",
    {
        "PaddingType": NotRequired[PaddingTypeType],
    },
)
CardHolderVerificationValueTypeDef = TypedDict(
    "CardHolderVerificationValueTypeDef",
    {
        "UnpredictableNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
    },
)
CardVerificationValue1TypeDef = TypedDict(
    "CardVerificationValue1TypeDef",
    {
        "CardExpiryDate": str,
        "ServiceCode": str,
    },
)
CardVerificationValue2TypeDef = TypedDict(
    "CardVerificationValue2TypeDef",
    {
        "CardExpiryDate": str,
    },
)
DynamicCardVerificationCodeTypeDef = TypedDict(
    "DynamicCardVerificationCodeTypeDef",
    {
        "UnpredictableNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
        "TrackData": str,
    },
)
DynamicCardVerificationValueTypeDef = TypedDict(
    "DynamicCardVerificationValueTypeDef",
    {
        "PanSequenceNumber": str,
        "CardExpiryDate": str,
        "ServiceCode": str,
        "ApplicationTransactionCounter": str,
    },
)
DiscoverDynamicCardVerificationCodeTypeDef = TypedDict(
    "DiscoverDynamicCardVerificationCodeTypeDef",
    {
        "CardExpiryDate": str,
        "UnpredictableNumber": str,
        "ApplicationTransactionCounter": str,
    },
)
CryptogramVerificationArpcMethod1TypeDef = TypedDict(
    "CryptogramVerificationArpcMethod1TypeDef",
    {
        "AuthResponseCode": str,
    },
)
CryptogramVerificationArpcMethod2TypeDef = TypedDict(
    "CryptogramVerificationArpcMethod2TypeDef",
    {
        "CardStatusUpdate": str,
        "ProprietaryAuthenticationData": NotRequired[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
Emv2000AttributesTypeDef = TypedDict(
    "Emv2000AttributesTypeDef",
    {
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
    },
)
EmvCommonAttributesTypeDef = TypedDict(
    "EmvCommonAttributesTypeDef",
    {
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationCryptogram": str,
        "Mode": EmvEncryptionModeType,
        "PinBlockPaddingType": PinBlockPaddingTypeType,
        "PinBlockLengthPosition": PinBlockLengthPositionType,
    },
)
MasterCardAttributesTypeDef = TypedDict(
    "MasterCardAttributesTypeDef",
    {
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationCryptogram": str,
    },
)
DukptAttributesTypeDef = TypedDict(
    "DukptAttributesTypeDef",
    {
        "KeySerialNumber": str,
        "DukptDerivationType": DukptDerivationTypeType,
    },
)
DukptDerivationAttributesTypeDef = TypedDict(
    "DukptDerivationAttributesTypeDef",
    {
        "KeySerialNumber": str,
        "DukptKeyDerivationType": NotRequired[DukptDerivationTypeType],
        "DukptKeyVariant": NotRequired[DukptKeyVariantType],
    },
)
DukptEncryptionAttributesTypeDef = TypedDict(
    "DukptEncryptionAttributesTypeDef",
    {
        "KeySerialNumber": str,
        "Mode": NotRequired[DukptEncryptionModeType],
        "DukptKeyDerivationType": NotRequired[DukptDerivationTypeType],
        "DukptKeyVariant": NotRequired[DukptKeyVariantType],
        "InitializationVector": NotRequired[str],
    },
)
EcdhDerivationAttributesTypeDef = TypedDict(
    "EcdhDerivationAttributesTypeDef",
    {
        "CertificateAuthorityPublicKeyIdentifier": str,
        "PublicKeyCertificate": str,
        "KeyAlgorithm": SymmetricKeyAlgorithmType,
        "KeyDerivationFunction": KeyDerivationFunctionType,
        "KeyDerivationHashAlgorithm": KeyDerivationHashAlgorithmType,
        "SharedInformation": str,
    },
)
EmvEncryptionAttributesTypeDef = TypedDict(
    "EmvEncryptionAttributesTypeDef",
    {
        "MajorKeyDerivationMode": EmvMajorKeyDerivationModeType,
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "SessionDerivationData": str,
        "Mode": NotRequired[EmvEncryptionModeType],
        "InitializationVector": NotRequired[str],
    },
)
SymmetricEncryptionAttributesTypeDef = TypedDict(
    "SymmetricEncryptionAttributesTypeDef",
    {
        "Mode": EncryptionModeType,
        "InitializationVector": NotRequired[str],
        "PaddingType": NotRequired[PaddingTypeType],
    },
)
VisaAmexDerivationOutputsTypeDef = TypedDict(
    "VisaAmexDerivationOutputsTypeDef",
    {
        "AuthorizationRequestKeyArn": str,
        "AuthorizationRequestKeyCheckValue": str,
        "CurrentPinPekArn": NotRequired[str],
        "CurrentPinPekKeyCheckValue": NotRequired[str],
    },
)
PinDataTypeDef = TypedDict(
    "PinDataTypeDef",
    {
        "PinOffset": NotRequired[str],
        "VerificationValue": NotRequired[str],
    },
)
Ibm3624NaturalPinTypeDef = TypedDict(
    "Ibm3624NaturalPinTypeDef",
    {
        "DecimalizationTable": str,
        "PinValidationDataPadCharacter": str,
        "PinValidationData": str,
    },
)
Ibm3624PinFromOffsetTypeDef = TypedDict(
    "Ibm3624PinFromOffsetTypeDef",
    {
        "DecimalizationTable": str,
        "PinValidationDataPadCharacter": str,
        "PinValidationData": str,
        "PinOffset": str,
    },
)
Ibm3624PinOffsetTypeDef = TypedDict(
    "Ibm3624PinOffsetTypeDef",
    {
        "EncryptedPinBlock": str,
        "DecimalizationTable": str,
        "PinValidationDataPadCharacter": str,
        "PinValidationData": str,
    },
)
Ibm3624PinVerificationTypeDef = TypedDict(
    "Ibm3624PinVerificationTypeDef",
    {
        "DecimalizationTable": str,
        "PinValidationDataPadCharacter": str,
        "PinValidationData": str,
        "PinOffset": str,
    },
)
Ibm3624RandomPinTypeDef = TypedDict(
    "Ibm3624RandomPinTypeDef",
    {
        "DecimalizationTable": str,
        "PinValidationDataPadCharacter": str,
        "PinValidationData": str,
    },
)
MacAlgorithmDukptTypeDef = TypedDict(
    "MacAlgorithmDukptTypeDef",
    {
        "KeySerialNumber": str,
        "DukptKeyVariant": DukptKeyVariantType,
        "DukptDerivationType": NotRequired[DukptDerivationTypeType],
    },
)
SessionKeyDerivationValueTypeDef = TypedDict(
    "SessionKeyDerivationValueTypeDef",
    {
        "ApplicationCryptogram": NotRequired[str],
        "ApplicationTransactionCounter": NotRequired[str],
    },
)
VisaPinTypeDef = TypedDict(
    "VisaPinTypeDef",
    {
        "PinVerificationKeyIndex": int,
    },
)
VisaPinVerificationValueTypeDef = TypedDict(
    "VisaPinVerificationValueTypeDef",
    {
        "EncryptedPinBlock": str,
        "PinVerificationKeyIndex": int,
    },
)
VisaPinVerificationTypeDef = TypedDict(
    "VisaPinVerificationTypeDef",
    {
        "PinVerificationKeyIndex": int,
        "VerificationValue": str,
    },
)
SessionKeyAmexTypeDef = TypedDict(
    "SessionKeyAmexTypeDef",
    {
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
    },
)
SessionKeyEmv2000TypeDef = TypedDict(
    "SessionKeyEmv2000TypeDef",
    {
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
    },
)
SessionKeyEmvCommonTypeDef = TypedDict(
    "SessionKeyEmvCommonTypeDef",
    {
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
    },
)
SessionKeyMastercardTypeDef = TypedDict(
    "SessionKeyMastercardTypeDef",
    {
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
        "UnpredictableNumber": str,
    },
)
SessionKeyVisaTypeDef = TypedDict(
    "SessionKeyVisaTypeDef",
    {
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
    },
)
TranslationPinDataIsoFormat034TypeDef = TypedDict(
    "TranslationPinDataIsoFormat034TypeDef",
    {
        "PrimaryAccountNumber": str,
    },
)
AmexAttributesTypeDef = TypedDict(
    "AmexAttributesTypeDef",
    {
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
        "AuthorizationRequestKeyIdentifier": str,
        "CurrentPinAttributes": NotRequired[CurrentPinAttributesTypeDef],
    },
)
VisaAttributesTypeDef = TypedDict(
    "VisaAttributesTypeDef",
    {
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "ApplicationTransactionCounter": str,
        "AuthorizationRequestKeyIdentifier": str,
        "CurrentPinAttributes": NotRequired[CurrentPinAttributesTypeDef],
    },
)
CardGenerationAttributesTypeDef = TypedDict(
    "CardGenerationAttributesTypeDef",
    {
        "AmexCardSecurityCodeVersion1": NotRequired[AmexCardSecurityCodeVersion1TypeDef],
        "AmexCardSecurityCodeVersion2": NotRequired[AmexCardSecurityCodeVersion2TypeDef],
        "CardVerificationValue1": NotRequired[CardVerificationValue1TypeDef],
        "CardVerificationValue2": NotRequired[CardVerificationValue2TypeDef],
        "CardHolderVerificationValue": NotRequired[CardHolderVerificationValueTypeDef],
        "DynamicCardVerificationCode": NotRequired[DynamicCardVerificationCodeTypeDef],
        "DynamicCardVerificationValue": NotRequired[DynamicCardVerificationValueTypeDef],
    },
)
CardVerificationAttributesTypeDef = TypedDict(
    "CardVerificationAttributesTypeDef",
    {
        "AmexCardSecurityCodeVersion1": NotRequired[AmexCardSecurityCodeVersion1TypeDef],
        "AmexCardSecurityCodeVersion2": NotRequired[AmexCardSecurityCodeVersion2TypeDef],
        "CardVerificationValue1": NotRequired[CardVerificationValue1TypeDef],
        "CardVerificationValue2": NotRequired[CardVerificationValue2TypeDef],
        "CardHolderVerificationValue": NotRequired[CardHolderVerificationValueTypeDef],
        "DynamicCardVerificationCode": NotRequired[DynamicCardVerificationCodeTypeDef],
        "DynamicCardVerificationValue": NotRequired[DynamicCardVerificationValueTypeDef],
        "DiscoverDynamicCardVerificationCode": NotRequired[
            DiscoverDynamicCardVerificationCodeTypeDef
        ],
    },
)
CryptogramAuthResponseTypeDef = TypedDict(
    "CryptogramAuthResponseTypeDef",
    {
        "ArpcMethod1": NotRequired[CryptogramVerificationArpcMethod1TypeDef],
        "ArpcMethod2": NotRequired[CryptogramVerificationArpcMethod2TypeDef],
    },
)
DecryptDataOutputTypeDef = TypedDict(
    "DecryptDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "PlainText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EncryptDataOutputTypeDef = TypedDict(
    "EncryptDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "CipherText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GenerateCardValidationDataOutputTypeDef = TypedDict(
    "GenerateCardValidationDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "ValidationData": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GenerateMacOutputTypeDef = TypedDict(
    "GenerateMacOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "Mac": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ReEncryptDataOutputTypeDef = TypedDict(
    "ReEncryptDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "CipherText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
TranslatePinDataOutputTypeDef = TypedDict(
    "TranslatePinDataOutputTypeDef",
    {
        "PinBlock": str,
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
VerifyAuthRequestCryptogramOutputTypeDef = TypedDict(
    "VerifyAuthRequestCryptogramOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "AuthResponseValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
VerifyCardValidationDataOutputTypeDef = TypedDict(
    "VerifyCardValidationDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
VerifyMacOutputTypeDef = TypedDict(
    "VerifyMacOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
VerifyPinDataOutputTypeDef = TypedDict(
    "VerifyPinDataOutputTypeDef",
    {
        "VerificationKeyArn": str,
        "VerificationKeyCheckValue": str,
        "EncryptionKeyArn": str,
        "EncryptionKeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
WrappedKeyMaterialTypeDef = TypedDict(
    "WrappedKeyMaterialTypeDef",
    {
        "Tr31KeyBlock": NotRequired[str],
        "DiffieHellmanSymmetricKey": NotRequired[EcdhDerivationAttributesTypeDef],
    },
)
EncryptionDecryptionAttributesTypeDef = TypedDict(
    "EncryptionDecryptionAttributesTypeDef",
    {
        "Symmetric": NotRequired[SymmetricEncryptionAttributesTypeDef],
        "Asymmetric": NotRequired[AsymmetricEncryptionAttributesTypeDef],
        "Dukpt": NotRequired[DukptEncryptionAttributesTypeDef],
        "Emv": NotRequired[EmvEncryptionAttributesTypeDef],
    },
)
ReEncryptionAttributesTypeDef = TypedDict(
    "ReEncryptionAttributesTypeDef",
    {
        "Symmetric": NotRequired[SymmetricEncryptionAttributesTypeDef],
        "Dukpt": NotRequired[DukptEncryptionAttributesTypeDef],
    },
)
GenerateMacEmvPinChangeOutputTypeDef = TypedDict(
    "GenerateMacEmvPinChangeOutputTypeDef",
    {
        "NewPinPekArn": str,
        "SecureMessagingIntegrityKeyArn": str,
        "SecureMessagingConfidentialityKeyArn": str,
        "Mac": str,
        "EncryptedPinBlock": str,
        "NewPinPekKeyCheckValue": str,
        "SecureMessagingIntegrityKeyCheckValue": str,
        "SecureMessagingConfidentialityKeyCheckValue": str,
        "VisaAmexDerivationOutputs": VisaAmexDerivationOutputsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GeneratePinDataOutputTypeDef = TypedDict(
    "GeneratePinDataOutputTypeDef",
    {
        "GenerationKeyArn": str,
        "GenerationKeyCheckValue": str,
        "EncryptionKeyArn": str,
        "EncryptionKeyCheckValue": str,
        "EncryptedPinBlock": str,
        "PinData": PinDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MacAlgorithmEmvTypeDef = TypedDict(
    "MacAlgorithmEmvTypeDef",
    {
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "PrimaryAccountNumber": str,
        "PanSequenceNumber": str,
        "SessionKeyDerivationMode": SessionKeyDerivationModeType,
        "SessionKeyDerivationValue": SessionKeyDerivationValueTypeDef,
    },
)
PinGenerationAttributesTypeDef = TypedDict(
    "PinGenerationAttributesTypeDef",
    {
        "VisaPin": NotRequired[VisaPinTypeDef],
        "VisaPinVerificationValue": NotRequired[VisaPinVerificationValueTypeDef],
        "Ibm3624PinOffset": NotRequired[Ibm3624PinOffsetTypeDef],
        "Ibm3624NaturalPin": NotRequired[Ibm3624NaturalPinTypeDef],
        "Ibm3624RandomPin": NotRequired[Ibm3624RandomPinTypeDef],
        "Ibm3624PinFromOffset": NotRequired[Ibm3624PinFromOffsetTypeDef],
    },
)
PinVerificationAttributesTypeDef = TypedDict(
    "PinVerificationAttributesTypeDef",
    {
        "VisaPin": NotRequired[VisaPinVerificationTypeDef],
        "Ibm3624Pin": NotRequired[Ibm3624PinVerificationTypeDef],
    },
)
SessionKeyDerivationTypeDef = TypedDict(
    "SessionKeyDerivationTypeDef",
    {
        "EmvCommon": NotRequired[SessionKeyEmvCommonTypeDef],
        "Mastercard": NotRequired[SessionKeyMastercardTypeDef],
        "Emv2000": NotRequired[SessionKeyEmv2000TypeDef],
        "Amex": NotRequired[SessionKeyAmexTypeDef],
        "Visa": NotRequired[SessionKeyVisaTypeDef],
    },
)
TranslationIsoFormatsTypeDef = TypedDict(
    "TranslationIsoFormatsTypeDef",
    {
        "IsoFormat0": NotRequired[TranslationPinDataIsoFormat034TypeDef],
        "IsoFormat1": NotRequired[Mapping[str, Any]],
        "IsoFormat3": NotRequired[TranslationPinDataIsoFormat034TypeDef],
        "IsoFormat4": NotRequired[TranslationPinDataIsoFormat034TypeDef],
    },
)
DerivationMethodAttributesTypeDef = TypedDict(
    "DerivationMethodAttributesTypeDef",
    {
        "EmvCommon": NotRequired[EmvCommonAttributesTypeDef],
        "Amex": NotRequired[AmexAttributesTypeDef],
        "Visa": NotRequired[VisaAttributesTypeDef],
        "Emv2000": NotRequired[Emv2000AttributesTypeDef],
        "Mastercard": NotRequired[MasterCardAttributesTypeDef],
    },
)
GenerateCardValidationDataInputRequestTypeDef = TypedDict(
    "GenerateCardValidationDataInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "PrimaryAccountNumber": str,
        "GenerationAttributes": CardGenerationAttributesTypeDef,
        "ValidationDataLength": NotRequired[int],
    },
)
VerifyCardValidationDataInputRequestTypeDef = TypedDict(
    "VerifyCardValidationDataInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "PrimaryAccountNumber": str,
        "VerificationAttributes": CardVerificationAttributesTypeDef,
        "ValidationData": str,
    },
)
WrappedKeyTypeDef = TypedDict(
    "WrappedKeyTypeDef",
    {
        "WrappedKeyMaterial": WrappedKeyMaterialTypeDef,
        "KeyCheckValueAlgorithm": NotRequired[KeyCheckValueAlgorithmType],
    },
)
MacAttributesTypeDef = TypedDict(
    "MacAttributesTypeDef",
    {
        "Algorithm": NotRequired[MacAlgorithmType],
        "EmvMac": NotRequired[MacAlgorithmEmvTypeDef],
        "DukptIso9797Algorithm1": NotRequired[MacAlgorithmDukptTypeDef],
        "DukptIso9797Algorithm3": NotRequired[MacAlgorithmDukptTypeDef],
        "DukptCmac": NotRequired[MacAlgorithmDukptTypeDef],
    },
)
VerifyAuthRequestCryptogramInputRequestTypeDef = TypedDict(
    "VerifyAuthRequestCryptogramInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "TransactionData": str,
        "AuthRequestCryptogram": str,
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "SessionKeyDerivationAttributes": SessionKeyDerivationTypeDef,
        "AuthResponseAttributes": NotRequired[CryptogramAuthResponseTypeDef],
    },
)
GenerateMacEmvPinChangeInputRequestTypeDef = TypedDict(
    "GenerateMacEmvPinChangeInputRequestTypeDef",
    {
        "NewPinPekIdentifier": str,
        "NewEncryptedPinBlock": str,
        "PinBlockFormat": PinBlockFormatForEmvPinChangeType,
        "SecureMessagingIntegrityKeyIdentifier": str,
        "SecureMessagingConfidentialityKeyIdentifier": str,
        "MessageData": str,
        "DerivationMethodAttributes": DerivationMethodAttributesTypeDef,
    },
)
DecryptDataInputRequestTypeDef = TypedDict(
    "DecryptDataInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "CipherText": str,
        "DecryptionAttributes": EncryptionDecryptionAttributesTypeDef,
        "WrappedKey": NotRequired[WrappedKeyTypeDef],
    },
)
EncryptDataInputRequestTypeDef = TypedDict(
    "EncryptDataInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "PlainText": str,
        "EncryptionAttributes": EncryptionDecryptionAttributesTypeDef,
        "WrappedKey": NotRequired[WrappedKeyTypeDef],
    },
)
GeneratePinDataInputRequestTypeDef = TypedDict(
    "GeneratePinDataInputRequestTypeDef",
    {
        "GenerationKeyIdentifier": str,
        "EncryptionKeyIdentifier": str,
        "GenerationAttributes": PinGenerationAttributesTypeDef,
        "PrimaryAccountNumber": str,
        "PinBlockFormat": PinBlockFormatForPinDataType,
        "PinDataLength": NotRequired[int],
        "EncryptionWrappedKey": NotRequired[WrappedKeyTypeDef],
    },
)
ReEncryptDataInputRequestTypeDef = TypedDict(
    "ReEncryptDataInputRequestTypeDef",
    {
        "IncomingKeyIdentifier": str,
        "OutgoingKeyIdentifier": str,
        "CipherText": str,
        "IncomingEncryptionAttributes": ReEncryptionAttributesTypeDef,
        "OutgoingEncryptionAttributes": ReEncryptionAttributesTypeDef,
        "IncomingWrappedKey": NotRequired[WrappedKeyTypeDef],
        "OutgoingWrappedKey": NotRequired[WrappedKeyTypeDef],
    },
)
TranslatePinDataInputRequestTypeDef = TypedDict(
    "TranslatePinDataInputRequestTypeDef",
    {
        "IncomingKeyIdentifier": str,
        "OutgoingKeyIdentifier": str,
        "IncomingTranslationAttributes": TranslationIsoFormatsTypeDef,
        "OutgoingTranslationAttributes": TranslationIsoFormatsTypeDef,
        "EncryptedPinBlock": str,
        "IncomingDukptAttributes": NotRequired[DukptDerivationAttributesTypeDef],
        "OutgoingDukptAttributes": NotRequired[DukptDerivationAttributesTypeDef],
        "IncomingWrappedKey": NotRequired[WrappedKeyTypeDef],
        "OutgoingWrappedKey": NotRequired[WrappedKeyTypeDef],
    },
)
VerifyPinDataInputRequestTypeDef = TypedDict(
    "VerifyPinDataInputRequestTypeDef",
    {
        "VerificationKeyIdentifier": str,
        "EncryptionKeyIdentifier": str,
        "VerificationAttributes": PinVerificationAttributesTypeDef,
        "EncryptedPinBlock": str,
        "PrimaryAccountNumber": str,
        "PinBlockFormat": PinBlockFormatForPinDataType,
        "PinDataLength": NotRequired[int],
        "DukptAttributes": NotRequired[DukptAttributesTypeDef],
        "EncryptionWrappedKey": NotRequired[WrappedKeyTypeDef],
    },
)
GenerateMacInputRequestTypeDef = TypedDict(
    "GenerateMacInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "MessageData": str,
        "GenerationAttributes": MacAttributesTypeDef,
        "MacLength": NotRequired[int],
    },
)
VerifyMacInputRequestTypeDef = TypedDict(
    "VerifyMacInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "MessageData": str,
        "Mac": str,
        "VerificationAttributes": MacAttributesTypeDef,
        "MacLength": NotRequired[int],
    },
)
